# Email OTP Service

## Tính năng

- Trích xuất mã OTP từ nội dung email mới
- API RESTful 

## Yêu cầu hệ thống

- Python 3.11
- Poetry (quản lý dependencies)
- Kết nối internet ổn định
- Tài khoản Gmail (với App Password đã được cấu hình)

## Cài đặt

1. Cài đặt dependencies:
```bash
poetry install
```

2. Cấu hình môi trường:
   - Copy file `.env.example` thành `.env`
   - Cập nhật các thông tin cần thiết:
```env
GMAIL_USER=your_email@gmail.com
GMAIL_PASS=your_app_password
GMAIL_TAG=INBOX
```

Dịch vụ sẽ chạy tại http://localhost:8000

## Testing

Chạy unit tests:
```bash
poetry run pytest
```

## Production

```bash
poetry run python src/main.py
```