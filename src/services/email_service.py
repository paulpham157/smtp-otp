import imaplib
import email
from email.header import decode_header
import re
from typing import List, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class EmailData:
    subject: str
    sender: str
    date: str
    otp: Optional[str]
    body: str


class EmailService:
    def __init__(self, gmail_user: str, gmail_pass: str, gmail_tag: str = "INBOX"):
        self.gmail_user = gmail_user
        self.gmail_pass = gmail_pass
        self.gmail_tag = gmail_tag
        self.mail = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        """Kết nối tới Gmail qua IMAP SSL."""
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        self.mail.login(self.gmail_user, self.gmail_pass)
        self.mail.select(self.gmail_tag)

    def disconnect(self):
        """Đóng kết nối IMAP."""
        if self.mail:
            try:
                self.mail.close()
                self.mail.logout()
            except:
                pass

    @staticmethod
    def decode_subject(subject: Optional[str]) -> str:
        """Giải mã tiêu đề email với xử lý encoding."""
        if subject is None:
            return "No Subject"
        decoded_list = decode_header(subject)
        decoded_parts = []
        for content, encoding in decoded_list:
            if isinstance(content, bytes):
                try:
                    decoded_parts.append(content.decode(encoding or "utf-8"))
                except:
                    decoded_parts.append(content.decode("utf-8", errors="replace"))
            else:
                decoded_parts.append(content)
        return " ".join(decoded_parts)

    @staticmethod
    def get_email_body(email_message: email.message.Message) -> str:
        """Trích xuất nội dung email từ message."""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        else:
            return email_message.get_payload(decode=True).decode()
        return ""

    @staticmethod
    def extract_otp(body: str) -> Optional[str]:
        """Trích xuất mã OTP từ nội dung email."""
        otp_pattern = r"\b\d{6}\b"
        match = re.search(otp_pattern, body)
        return match.group(0) if match else None

    def get_latest_unread_email(self, to_email: str) -> Optional[EmailData]:
        """Lấy email chưa đọc mới nhất gửi đến địa chỉ email cụ thể."""
        if not self.mail:
            raise ConnectionError("Not connected to IMAP server")

        search_criteria = f'(UNSEEN TO "{to_email}")'
        status, messages = self.mail.search(None, search_criteria)

        if status != "OK":
            return None

        message_numbers = messages[0].split()
        if not message_numbers:
            return None

        # Lấy email mới nhất
        msg_id = message_numbers[-1]
        status, msg_data = self.mail.fetch(msg_id, "(RFC822)")

        if status != "OK":
            return None

        email_body = msg_data[0][1]
        email_message = email.message_from_bytes(email_body)

        body = self.get_email_body(email_message)

        return EmailData(
            subject=self.decode_subject(email_message["subject"]),
            sender=email.utils.parseaddr(email_message["from"])[1],
            date=email_message["date"],
            otp=self.extract_otp(body),
            body=body,
        )

    def get_all_unread_emails(self, to_email: str) -> List[EmailData]:
        """Lấy tất cả email chưa đọc gửi đến địa chỉ email cụ thể."""
        if not self.mail:
            raise ConnectionError("Chưa kết nối đến máy chủ IMAP")

        search_criteria = f'(UNSEEN TO "{to_email}")'
        status, messages = self.mail.search(None, search_criteria)

        if status != "OK":
            return []

        message_numbers = messages[0].split()
        if not message_numbers:
            return []

        email_list = []
        for msg_id in message_numbers:
            status, msg_data = self.mail.fetch(msg_id, "(RFC822)")

            if status != "OK":
                continue

            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)

            body = self.get_email_body(email_message)

            email_data = EmailData(
                subject=self.decode_subject(email_message["subject"]),
                sender=email.utils.parseaddr(email_message["from"])[1],
                date=email_message["date"],
                otp=self.extract_otp(body),
                body=body,
            )
            email_list.append(email_data)

        return email_list

    def get_all_emails(self, to_email: str) -> List[EmailData]:
        """Lấy tất cả email (đã đọc và chưa đọc) gửi đến địa chỉ email cụ thể."""
        if not self.mail:
            raise ConnectionError("Chưa kết nối đến máy chủ IMAP")

        search_criteria = f'(TO "{to_email}")'
        status, messages = self.mail.search(None, search_criteria)

        if status != "OK":
            return []

        message_numbers = messages[0].split()
        if not message_numbers:
            return []

        email_list = []
        for msg_id in message_numbers:
            status, msg_data = self.mail.fetch(msg_id, "(RFC822)")

            if status != "OK":
                continue

            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)

            body = self.get_email_body(email_message)

            email_data = EmailData(
                subject=self.decode_subject(email_message["subject"]),
                sender=email.utils.parseaddr(email_message["from"])[1],
                date=email_message["date"],
                otp=self.extract_otp(body),
                body=body,
            )
            email_list.append(email_data)

        return email_list
