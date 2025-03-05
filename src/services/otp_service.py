from typing import Dict, Optional
from src.core.config import Settings
from src.services.email_service import EmailService
from src.services.random_user_service import RandomUserService
import asyncio


class OtpService:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def get_reg_new_otp(self) -> Dict:
        """Tạo thông tin người dùng ngẫu nhiên và tìm OTP trong email."""
        random_user = RandomUserService.generate_user()
        user_info = random_user.to_dict()

        print("\nThông tin người dùng ngẫu nhiên:")
        print(f"Họ: {user_info['last_name']}")
        print(f"Tên: {user_info['first_name']}")
        print(f"Email: {user_info['email']}")
        print(f"Password: {user_info['password']}")

        wait_times = [3, 2, 1]
        total_wait_time = 0
        attempts = 0

        for wait_time in wait_times:
            attempts += 1
            await asyncio.sleep(wait_time)
            total_wait_time += wait_time

            try:
                with EmailService(
                    gmail_user=self.settings.gmail_user,
                    gmail_pass=self.settings.gmail_pass,
                    gmail_tag=self.settings.gmail_tag,
                ) as email_service:
                    email_data = email_service.get_latest_unread_email(
                        user_info["email"]
                    )

                    if email_data and email_data.otp:
                        return {
                            "user_info": user_info,
                            "otp": email_data.otp,
                            "email_date": email_data.date,
                            "attempts": attempts,
                            "total_wait_time": total_wait_time,
                        }

                    print(f"Lần {attempts}: Không tìm thấy email sau {wait_time} giây")

            except Exception as e:
                print(f"Lỗi khi tìm email lần {attempts}: {str(e)}")

        return {
            "user_info": user_info,
            "otp": None,
            "email_date": None,
            "attempts": attempts,
            "total_wait_time": total_wait_time,
        }

    async def get_all_unread_otps(self, email: str) -> Dict:
        """Truy vấn lấy danh sách các OTP chưa đọc của 1 email cụ thể."""
        with EmailService(
            gmail_user=self.settings.gmail_user,
            gmail_pass=self.settings.gmail_pass,
            gmail_tag=self.settings.gmail_tag,
        ) as email_service:
            emails = email_service.get_all_unread_emails(email)

            otp_list = []
            for email_data in emails:
                if email_data and email_data.otp:
                    otp_list.append({"otp": email_data.otp, "date": email_data.date})

            return {
                "email": email,
                "otp_list": otp_list,
                "total_otps": len(otp_list),
            }

    async def get_all_otps(self, email: str) -> Dict:
        """Truy vấn lấy tất cả OTP của 1 email cụ thể."""
        with EmailService(
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
