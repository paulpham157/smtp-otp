import os
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import sys
import re
import argparse


def decode_subject(subject):
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


def get_email_body(email_message):
    """Trích xuất nội dung email từ message."""
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode()
    else:
        return email_message.get_payload(decode=True).decode()
    return ""


def extract_otp(body):
    """Trích xuất mã OTP từ nội dung email."""
    # Tìm số có 6 chữ số liên tiếp - pattern phổ biến cho OTP
    otp_pattern = r"\b\d{6}\b"
    match = re.search(otp_pattern, body)
    if match:
        return match.group(0)
    return None


def main():
    parser = argparse.ArgumentParser(description="Tìm email và trích xuất OTP.")
    parser.add_argument("--to_email", required=True, help="Địa chỉ email nhận cần tìm")
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    # Get credentials from .env
    gmail_email = os.getenv("GMAIL_USER")
    gmail_pass = os.getenv("GMAIL_PASS")
    gmail_tag = os.getenv("GMAIL_TAG", "INBOX")

    print(f"Connecting to gmail as {gmail_email}...", file=sys.stderr)

    try:
        # Create an IMAP4 class with SSL
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)

        # Authenticate
        mail.login(gmail_email, gmail_pass)
        print("Successfully logged in!", file=sys.stderr)

        status, messages = mail.select(gmail_tag)
        if status == "OK":
            print(f"Successfully selected mailbox: {gmail_tag}", file=sys.stderr)

            # Tìm email chưa đọc và gửi đến địa chỉ cụ thể
            search_criteria = f'(UNSEEN TO "{args.to_email}")'
            status, messages = mail.search(None, search_criteria)

            if status == "OK":
                message_numbers = messages[0].split()
                messages_count = len(message_numbers)
                print(
                    f"Found {messages_count} unread messages to {args.to_email}",
                    file=sys.stderr,
                )

                if messages_count > 0:
                    # Chỉ xem email mới nhất
                    msg_id = message_numbers[-1]
                    status, msg_data = mail.fetch(msg_id, "(RFC822)")

                    if status == "OK":
                        email_body = msg_data[0][1]
                        email_message = email.message_from_bytes(email_body)

                        # Get subject and sender
                        subject = decode_subject(email_message["subject"])
                        sender = email.utils.parseaddr(email_message["from"])[1]
                        date = email_message["date"]

                        # Get body and extract OTP
                        body = get_email_body(email_message)
                        otp = extract_otp(body)

                        print(f"\nLatest matching message:")
                        print(f"From: {sender}")
                        print(f"Subject: {subject}")
                        print(f"Date: {date}")
                        if otp:
                            print(f"OTP: {otp}")
                        else:
                            print("No OTP found in email content")
                else:
                    print(f"No messages found sent to {args.to_email}")

        # Close the connection
        mail.close()
        mail.logout()
        print("\nConnection closed.", file=sys.stderr)

    except imaplib.IMAP4.error as e:
        print(f"IMAP error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
