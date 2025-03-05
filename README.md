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

1. Clone repository:
```bash
git clone https://github.com/yourusername/email-otp-service.git
cd email-otp-service
```

2. Cài đặt Poetry (nếu chưa có):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Cài đặt dependencies:
```bash
poetry install
```

4. Cấu hình môi trường:
   - Copy file `.env.example` thành `.env`
   - Cập nhật các thông tin cần thiết:
```env
GMAIL_USER=your_email@gmail.com
GMAIL_PASS=your_app_password
GMAIL_TAG=INBOX
```

## Khởi động dịch vụ

```bash
poetry run python src/main.py
```

Dịch vụ sẽ chạy tại http://localhost:8000

## API Endpoints

### GET /api/v1/email/otp/{to_email}

Lấy và xử lý email mới nhất gửi đến địa chỉ email được chỉ định.

**Parameters:**
- to_email: Địa chỉ email đích (required)

**Response:**
```json
{
    "status": "success",
    "data": {
        "subject": "Email subject",
        "sender": "sender@example.com",
        "date": "2024-03-04T12:00:00Z",
        "otp": "123456",
        "body": "Email content"
    }
}
```

## Sử dụng như Package

```python
from src.services.email_service import EmailService

with EmailService() as service:
    email_data = service.get_latest_unread_email("target@example.com")
    if email_data and email_data.otp:
        print(f"Mã OTP: {email_data.otp}")
```

## Testing

Chạy unit tests:
```bash
poetry run pytest
```

## Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## License

Dự án được phân phối dưới giấy phép MIT. Xem `LICENSE` để biết thêm thông tin.