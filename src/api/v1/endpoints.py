from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, Dict
from pydantic import BaseModel
import asyncio

from src.core.config import get_settings, Settings
from src.services.email_service import EmailService
from src.services.random_user_service import RandomUserService

router = APIRouter()


class RandomUserResponse(BaseModel):
    user_info: Dict[str, str]
    otp: Optional[str] = None
    email_date: Optional[str] = None
    attempts: int
    total_wait_time: float


class EmailRequest(BaseModel):
    email: str


@router.get("/reg-new-otp", response_model=RandomUserResponse)
async def get_reg_new_otp(settings: Settings = Depends(get_settings)):
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


@router.post("/all-unread-otps")
async def get_all_unread_otps(
    request: EmailRequest, settings: Settings = Depends(get_settings)
):
    """Truy vấn lấy danh sách các OTP cũ của 1 email cụ thể."""
    try:
        with EmailService(
            gmail_user=settings.gmail_user,
            gmail_pass=settings.gmail_pass,
            gmail_tag=settings.gmail_tag,
        ) as email_service:
            # Lấy tất cả email chưa đọc của địa chỉ email này
            emails = email_service.get_all_unread_emails(request.email)

            # Tạo danh sách các OTP và thời gian
            otp_list = []
            for email_data in emails:
                if email_data and email_data.otp:
                    otp_list.append({"otp": email_data.otp, "date": email_data.date})

            return {
                "email": request.email,
                "otp_list": otp_list,
                "total_otps": len(otp_list),
            }

    except Exception as e:
        print(f"Lỗi khi truy vấn email: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Không thể truy vấn email: {str(e)}"
        )


@router.post("/all-otps")
async def get_all_otps(
    request: EmailRequest,
    settings: Settings = Depends(get_settings),
):
    """Truy vấn lấy tất cả OTP của 1 email cụ thể (bao gồm cả đã đọc và chưa đọc)."""
    try:
        with EmailService(
            gmail_user=settings.gmail_user,
            gmail_pass=settings.gmail_pass,
            gmail_tag=settings.gmail_tag,
        ) as email_service:
            # Lấy tất cả email của địa chỉ email này
            emails = email_service.get_all_emails(request.email)

            # Tạo danh sách các OTP và thời gian
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
                "email": request.email,
                "otp_list": otp_list,
                "total_otps": len(otp_list),
            }

    except Exception as e:
        print(f"Lỗi khi truy vấn email: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Không thể truy vấn email: {str(e)}"
        )
