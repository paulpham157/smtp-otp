# Email OTP Service

Dịch vụ tự động xử lý và trích xuất mã OTP từ email sử dụng IMAP. Hỗ trợ đa dạng các nhà cung cấp email và tích hợp dễ dàng vào các ứng dụng khác.

## Tính năng chính

- 📧 Tự động đọc và xử lý email mới
- 🔑 Trích xuất mã OTP từ nội dung email
- 🔄 Hỗ trợ nhiều định dạng email và mã OTP
- 🚀 API RESTful đơn giản và dễ sử dụng
- 📦 Có thể sử dụng như một package độc lập
- 🔒 Bảo mật với xác thực Gmail App Password

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