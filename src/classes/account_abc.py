import os
from abc import ABC, abstractmethod
from pathlib import Path

from dotenv import load_dotenv
from pyrogram import Client as PyrogramClient
from telethon.sync import TelegramClient

load_dotenv()


class ABCAccount(ABC):
    sessions_path = str(Path(Path(__file__).parent.parent.parent, "sessions"))
    device_model = [
        "Redmi Redmi Note 9",
        "Redmi Redmi Note 11",
        "Redmi Redmi 10",
        "Redmi Redmi Note 10S",
        "Redmi Redmi 6A",
        "Redmi Redmi 10A",
        "POCO X3 NFC",
        "POCO M2 PRO",
        "Mi 9",
        "Redmi Redmi K50",
    ]
    system_version = [
        "Android 11 Q (30)",
        "Android 6 M (29)",
        "Android 7 N (30)",
        "Android 8 O (30)",
        "Android 13 T (29)",
        "Android 12 S (30)",
        "Android 11 R (29)",
        "Android 9 P (29)",
    ]
    app_version = ["Telegram Android 10.6.1", "Telegram Android 10.6.0", "Telegram Android 10.5.9"]

    proxy = {
        "proxy_type": os.getenv("proxy_type"),  # (mandatory) protocol to use (see above)
        "addr": os.getenv("proxy_addr"),  # (mandatory) proxy IP address
        "port": os.getenv("proxy_port"),  # (mandatory) proxy port number
        "username": os.getenv("proxy_username"),  # (optional) username if the proxy requires auth
        "password": os.getenv("proxy_password"),  # (optional) password if the proxy requires auth
    }
    api_id = os.getenv("api_id")
    api_hash = os.getenv("api_hash")

    @abstractmethod
    def __init__(self, number):
        self.number = number
        self.session = ""
        self.premium = False

    @abstractmethod
    def get_status_premium(self, client: TelegramClient | PyrogramClient) -> None:
        pass

    @abstractmethod
    def get_client(self) -> TelegramClient | PyrogramClient:
        pass

    @staticmethod
    @abstractmethod
    def check_subscribe(username_channel: str, client: TelegramClient | PyrogramClient) -> bool:
        pass

    def check_session(self) -> None:
        """
        Рекурсивный поиск файла
        """
        for root, dirs, files in os.walk(self.sessions_path):
            for file in files:
                if self.number in file:
                    self.session = str(Path(root, file))

    @abstractmethod
    def subscribe(self, username_channel: str, client: TelegramClient | PyrogramClient):
        pass

    @abstractmethod
    def unsubscribe(self, username_channel: str, client: TelegramClient | PyrogramClient):
        pass
