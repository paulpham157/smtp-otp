from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path

# Định nghĩa phạm vi quyền truy cập
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def read_gmail():
    creds = None
    # Kiểm tra nếu đã có token
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # Nếu không có token hoặc token hết hạn, xác thực lại
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Lưu token để sử dụng sau
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)

    # Lấy danh sách email
    results = service.users().messages().list(userId="me", labelIds=["INBOX"]).execute()
    messages = results.get("messages", [])

    if not messages:
        print("Không có email nào.")
    else:
        print("Danh sách email:")
        for message in messages:
            msg = (
                service.users().messages().get(userId="me", id=message["id"]).execute()
            )
            print(f"Tiêu đề: {get_header(msg, 'Subject')}")
            print(f"Từ: {get_header(msg, 'From')}")
            print(f"Nội dung: {msg['snippet']}\n")


def get_header(message, header_name):
    headers = message["payload"]["headers"]
    for header in headers:
        if header["name"] == header_name:
            return header["value"]
    return ""


if __name__ == "__main__":
    read_gmail()
