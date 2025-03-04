import random
import string

# Danh sách họ và tên phổ biến tiếng Việt
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


def generate_random_name():
    """Tạo họ và tên ngẫu nhiên từ danh sách có sẵn"""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    return {"first_name": first_name, "last_name": last_name}


def generate_random_password():
    """Tạo mật khẩu ngẫu nhiên từ 10-16 ký tự bao gồm chữ, số và ký tự đặc biệt"""
    password_length = random.randint(10, 16)
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = "".join(random.choices(characters, k=password_length))
    return password


def generate_random_email(first_name, last_name):
    """Tạo địa chỉ email ngẫu nhiên với domain @paul157.site và thêm prefix ngẫu nhiên"""
    random_prefix = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=10)
    )
    email = f"{first_name.lower()}.{last_name.lower()}.{random_prefix}@paul157.site"
    return email


def generate_random_user():
    """Tạo thông tin người dùng ngẫu nhiên bao gồm họ tên, email và password"""
    name = generate_random_name()
    email = generate_random_email(name["first_name"], name["last_name"])
    password = generate_random_password()

    return {
        "first_name": name["first_name"],
        "last_name": name["last_name"],
        "email": email,
        "password": password,
    }


if __name__ == "__main__":
    user = generate_random_user()
    print("Thông tin người dùng ngẫu nhiên:")
    print(f"Họ: {user['last_name']}")
    print(f"Tên: {user['first_name']}")
    print(f"Email: {user['email']}")
    print(f"Password: {user['password']}")
