from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, Dict
from pydantic import BaseModel

from src.core.config import get_settings, Settings
from src.services.otp_service import OtpService

router = APIRouter()


class UserInfo(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class RegNewCursorResponse(BaseModel):
    user_info: UserInfo


class RegNewOtpRequest(BaseModel):
    email: str


class RegNewOtpResponse(BaseModel):
    otp: Optional[str] = None
    email_date: Optional[str] = None
    attempts: int
    total_wait_time: float


class EmailRequest(BaseModel):
    email: str


@router.post("/reg-new-cursor", response_model=RegNewCursorResponse)
async def reg_new_cursor(settings: Settings = Depends(get_settings)):
    """Tạo thông tin người dùng ngẫu nhiên."""
    try:
        otp_service = OtpService(settings)
        result = await otp_service.get_reg_new_cursor()
        return RegNewCursorResponse(user_info=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reg-new-otp", response_model=RegNewOtpResponse)
async def reg_new_otp(
    request: RegNewOtpRequest, settings: Settings = Depends(get_settings)
):
    """Tìm OTP trong email dựa trên email đã tạo."""
    try:
        otp_service = OtpService(settings)
        result = await otp_service.get_reg_new_otp_only(request.email)
        return RegNewOtpResponse(**result)
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
