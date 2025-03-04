# Email OTP Service

Service để đọc email và trích xuất mã OTP từ Gmail sử dụng IMAP.

## Cài đặt

1. Clone repository
2. Cài đặt dependencies:
```bash
poetry install
```

3. Tạo file `.env` với nội dung:
```
GMAIL_USER=your_email@gmail.com
GMAIL_PASS=your_app_password
GMAIL_TAG=INBOX
```

Lưu ý: Bạn cần tạo App Password cho Gmail. [Hướng dẫn tạo App Password](https://support.google.com/accounts/answer/185833?hl=en)

## Chạy service

```bash
uvicorn app.main:app --reload
```

Service sẽ chạy tại http://localhost:8000

## API Endpoints

### GET /api/v1/email/otp/{to_email}

Lấy email chưa đọc mới nhất gửi đến địa chỉ email cụ thể và trích xuất mã OTP.

**Parameters:**
- to_email: Địa chỉ email cần tìm

**Response:**
```json
{
    "subject": "Email subject",
    "sender": "sender@example.com",
    "date": "Thu, 1 Jan 2023 00:00:00 +0000",
    "otp": "123456",
    "body": "Email content"
}
```

## Sử dụng như một package

```python
from app.services.email_service import EmailService

with EmailService(gmail_user="your_email@gmail.com", 
                 gmail_pass="your_app_password") as service:
    email_data = service.get_latest_unread_email("target@example.com")
    if email_data:
        print(f"Found OTP: {email_data.otp}")
```