from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path


class GmailService:
    """Service để gửi email qua Gmail API (Đang phát triển)."""

    SCOPES = [
        "https://www.googleapis.com/auth/gmail.send",
        "https://www.googleapis.com/auth/gmail.compose",
    ]

    def __init__(
        self,
        credentials_path: str = "credentials.json",
        token_path: str = "token.pickle",
    ):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None

    def authenticate(self):
        """Xác thực với Gmail API."""
        creds = None
        if os.path.exists(self.token_path):
            with open(self.token_path, "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(self.token_path, "wb") as token:
                pickle.dump(creds, token)

        self.service = build("gmail", "v1", credentials=creds)

    # TODO: Implement send_email method
    def send_email(self, to: str, subject: str, body: str):
        """
        Gửi email (Chưa implement).

        Args:
            to: Địa chỉ email người nhận
            subject: Tiêu đề email
            body: Nội dung email
        """
        pass
