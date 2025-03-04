from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, Dict
from pydantic import BaseModel
import asyncio

from app.core.config import get_settings, Settings
from app.services.email_service import EmailService
from app.services.random_user_service import RandomUserService

router = APIRouter()


class RandomUserResponse(BaseModel):
    user_info: Dict[str, str]
    otp: Optional[str] = None
    email_date: Optional[str] = None
    attempts: int
    total_wait_time: float


@router.get("/random-email-otp", response_model=RandomUserResponse)
async def get_random_email_otp(settings: Settings = Depends(get_settings)):
    """Tạo thông tin người dùng ngẫu nhiên và tìm OTP trong email."""
    # Tạo thông tin người dùng ngẫu nhiên
    random_user = RandomUserService.generate_user()
    user_info = random_user.to_dict()

    print("\nThông tin người dùng ngẫu nhiên:")
    print(f"Họ: {user_info['last_name']}")
    print(f"Tên: {user_info['first_name']}")
    print(f"Email: {user_info['email']}")
    print(f"Password: {user_info['password']}")

    # Danh sách thời gian chờ
    wait_times = [3, 2, 1]
    total_wait_time = 0
    attempts = 0

    # Thử tìm email với các lần retry
    for wait_time in wait_times:
        attempts += 1
        await asyncio.sleep(wait_time)
        total_wait_time += wait_time

        try:
            with EmailService(
                gmail_user=settings.gmail_user,
                gmail_pass=settings.gmail_pass,
                gmail_tag=settings.gmail_tag,
            ) as email_service:
                email_data = email_service.get_latest_unread_email(user_info["email"])

                if email_data and email_data.otp:
                    return RandomUserResponse(
                        user_info=user_info,
                        otp=email_data.otp,
                        email_date=email_data.date,
                        attempts=attempts,
                        total_wait_time=total_wait_time,
                    )

                print(f"Lần {attempts}: Không tìm thấy email sau {wait_time} giây")

        except Exception as e:
            print(f"Lỗi khi tìm email lần {attempts}: {str(e)}")

    # Nếu không tìm thấy sau tất cả các lần thử
    return RandomUserResponse(
        user_info=user_info,
        otp=None,
        email_date=None,
        attempts=attempts,
        total_wait_time=total_wait_time,
    )
