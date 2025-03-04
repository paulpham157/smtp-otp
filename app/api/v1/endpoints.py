from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.core.config import get_settings, Settings
from app.services.email_service import EmailService, EmailData

router = APIRouter()


class EmailResponse(BaseModel):
    subject: str
    sender: str
    date: str
    otp: Optional[str]
    body: str

    class Config:
        from_attributes = True


@router.get("/email/otp/{to_email}", response_model=EmailResponse)
def get_email_otp(to_email: EmailStr, settings: Settings = Depends(get_settings)):
    """Lấy email chưa đọc mới nhất và trích xuất OTP."""
    try:
        with EmailService(
            gmail_user=settings.gmail_user,
            gmail_pass=settings.gmail_pass,
            gmail_tag=settings.gmail_tag,
        ) as email_service:
            email_data = email_service.get_latest_unread_email(to_email)
            if not email_data:
                raise HTTPException(
                    status_code=404, detail="No unread emails found for this address"
                )
            return email_data
    except ConnectionError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
