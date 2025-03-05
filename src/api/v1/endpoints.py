from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, Dict
from pydantic import BaseModel

from src.core.config import get_settings, Settings
from src.services.otp_service import OtpService

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
    try:
        otp_service = OtpService(settings)
        result = await otp_service.get_reg_new_otp()
        return RandomUserResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/all-unread-otps")
async def get_all_unread_otps(
    request: EmailRequest, settings: Settings = Depends(get_settings)
):
    """Truy vấn lấy danh sách các OTP cũ của 1 email cụ thể."""
    try:
        otp_service = OtpService(settings)
        return await otp_service.get_all_unread_otps(request.email)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Không thể truy vấn email: {str(e)}"
        )


@router.post("/all-otps")
async def get_all_otps(
    request: EmailRequest, settings: Settings = Depends(get_settings)
):
    """Truy vấn lấy tất cả OTP của 1 email cụ thể (bao gồm cả đã đọc và chưa đọc)."""
    try:
        otp_service = OtpService(settings)
        return await otp_service.get_all_otps(request.email)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Không thể truy vấn email: {str(e)}"
        )
