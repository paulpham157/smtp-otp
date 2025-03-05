from typing import Dict, Optional
from src.core.config import Settings
from src.services.imap_service import IMAPService
from src.services.random_user_service import RandomUserService
import asyncio


class OtpService:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def get_reg_new_cursor(self) -> Dict:
        """Tạo thông tin người dùng ngẫu nhiên."""
        random_user = RandomUserService.generate_user()
        return random_user.to_dict()

    async def get_reg_new_otp_only(self, email: str) -> Dict:
        """Tìm OTP trong email dựa trên email đã tạo."""
        print(f"\nĐang tìm OTP cho email: {email}")

        wait_times = [3, 2, 1]
        total_wait_time = 0
        attempts = 0

        for wait_time in wait_times:
            attempts += 1
            await asyncio.sleep(wait_time)
            total_wait_time += wait_time

            try:
                with IMAPService(
                    gmail_user=self.settings.gmail_user,
                    gmail_pass=self.settings.gmail_pass,
                    gmail_tag=self.settings.gmail_tag,
                ) as email_service:
                    email_data = email_service.get_latest_unread_email(email)

                    if email_data and email_data.otp:
                        return {
                            "otp": email_data.otp,
                            "email_date": email_data.date,
                            "attempts": attempts,
                            "total_wait_time": total_wait_time,
                        }

                    print(f"Lần {attempts}: Không tìm thấy email sau {wait_time} giây")

            except Exception as e:
                print(f"Lỗi khi tìm email lần {attempts}: {str(e)}")

        return {
            "otp": None,
            "email_date": None,
            "attempts": attempts,
            "total_wait_time": total_wait_time,
        }

    async def get_all_unread_otps(self, email: str) -> Dict:
        """Truy vấn lấy danh sách các OTP chưa đọc của 1 email cụ thể."""
        with IMAPService(
            gmail_user=self.settings.gmail_user,
            gmail_pass=self.settings.gmail_pass,
            gmail_tag=self.settings.gmail_tag,
        ) as email_service:
            emails = email_service.get_all_unread_emails(email)

            otp_list = []
            for email_data in emails:
                if email_data and email_data.otp:
                    otp_list.append(
                        {
                            "otp": email_data.otp,
                            "date": email_data.date,
                            "subject": email_data.subject,
                            "sender": email_data.sender,
                        }
                    )

            return {
                "email": email,
                "otp_list": otp_list,
                "total_otps": len(otp_list),
            }

    async def get_all_otps(self, email: str) -> Dict:
        """Truy vấn lấy tất cả OTP của 1 email cụ thể."""
        with IMAPService(
            gmail_user=self.settings.gmail_user,
            gmail_pass=self.settings.gmail_pass,
            gmail_tag=self.settings.gmail_tag,
        ) as email_service:
            emails = email_service.get_all_emails(email)

            otp_list = []
            for email_data in emails:
                if email_data.otp:
                    otp_list.append(
                        {
                            "otp": email_data.otp,
                            "date": email_data.date,
                            "subject": email_data.subject,
                            "sender": email_data.sender,
                        }
                    )

            return {
                "email": email,
                "otp_list": otp_list,
                "total_otps": len(otp_list),
            }
