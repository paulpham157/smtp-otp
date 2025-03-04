import random
import string
from dataclasses import dataclass
from typing import Dict


@dataclass
class RandomUser:
    first_name: str
    last_name: str
    email: str
    password: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
        }


class RandomUserService:
    FIRST_NAMES = [
        "Anh",
        "Binh",
        "Cuong",
        "Dung",
        "Ha",
        "Hai",
        "Huong",
        "Lan",
        "Linh",
        "Mai",
        "Minh",
        "Nam",
        "Nga",
        "Phuong",
        "Quang",
        "Thao",
        "Trang",
        "Tuan",
        "Viet",
        "Yen",
    ]

    LAST_NAMES = [
        "Nguyen",
        "Tran",
        "Le",
        "Pham",
        "Hoang",
        "Huynh",
        "Phan",
        "Vu",
        "Vo",
        "Dang",
        "Bui",
        "Do",
        "Ho",
        "Ngo",
        "Duong",
        "Ly",
    ]

    @classmethod
    def generate_random_name(cls) -> Dict[str, str]:
        """Tạo họ và tên ngẫu nhiên từ danh sách có sẵn."""
        return {
            "first_name": random.choice(cls.FIRST_NAMES),
            "last_name": random.choice(cls.LAST_NAMES),
        }

    @staticmethod
    def generate_random_password() -> str:
        """Tạo mật khẩu ngẫu nhiên từ 10-16 ký tự."""
        password_length = random.randint(10, 16)
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        return "".join(random.choices(characters, k=password_length))

    @staticmethod
    def generate_random_email(first_name: str, last_name: str) -> str:
        """Tạo địa chỉ email ngẫu nhiên."""
        random_prefix = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=10)
        )
        return f"{first_name.lower()}.{last_name.lower()}.{random_prefix}@paul157.site"

    @classmethod
    def generate_user(cls) -> RandomUser:
        """Tạo thông tin người dùng ngẫu nhiên."""
        name = cls.generate_random_name()
        email = cls.generate_random_email(name["first_name"], name["last_name"])
        password = cls.generate_random_password()

        return RandomUser(
            first_name=name["first_name"],
            last_name=name["last_name"],
            email=email,
            password=password,
        )
