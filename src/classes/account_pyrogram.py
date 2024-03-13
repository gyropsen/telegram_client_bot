import os
import random
import time
from pathlib import Path

from dotenv import load_dotenv
from pyrogram import Client as PyrogramClient

from src.classes.account_abc import ABCAccount

load_dotenv()


class TGAccountPyrogram(ABCAccount):
    proxy = {
        "scheme": os.getenv("proxy_type"),  # (mandatory) protocol to use (see above)
        "hostname": os.getenv("proxy_addr"),  # (mandatory) proxy IP address
        "port": int(os.getenv("proxy_port")),  # (mandatory) proxy port number
        "username": os.getenv("proxy_username"),  # (optional) username if the proxy requires auth
        "password": os.getenv("proxy_password"),  # (optional) password if the proxy requires auth
    }

    def __init__(self, number: str):
        self.number = number
        self.session = ""
        self.premium = False

    async def get_status_premium(self, client: PyrogramClient) -> None:
        """
        Проверяет наличие премиум подписки
        :param client: PyrogramClient
        :return: None
        """
        user_info = await client.get_me()
        self.premium = user_info.is_premium

    def get_client(self) -> PyrogramClient:
        """
        Возвращает телеграм клиент
        :return: PyrogramClient
        """
        session: str = str(Path(self.sessions_path, "for_pyrogram", self.number))
        client = PyrogramClient(
            session,
            self.api_id,
            self.api_hash,
            device_model=random.choice(self.device_model),
            system_version=random.choice(self.system_version),
            app_version=random.choice(self.app_version),
            proxy=self.proxy,
        )
        return client

    @staticmethod
    async def check_subscribe(link_channel: str, client: PyrogramClient) -> bool:
        """
        Проверяет, подписан ли аккаунт на канал
        :param link_channel: Ссылка или имя на telegram канал
        :param client: PyrogramClient
        :return: True - если, аккаунт подписан, False - если нет
        """
        username_channel = link_channel.split("/")[-1]
        channel = await client.get_chat(username_channel)
        async for dialog in client.get_dialogs():
            if dialog.chat.username:
                if str(dialog.chat.username).lower() == str(channel.username).lower():
                    return True
        return False

    async def subscribe(self, link_channel: str, client: PyrogramClient) -> None:
        """
        Подписаться аккаунтом на канал
        :param link_channel: Ссылка или имя на telegram канал
        :param client: PyrogramClient
        :return: None
        """
        username_channel = link_channel.split("/")[-1]
        sub = await self.check_subscribe(username_channel, client)
        if sub:
            print(f"Account {self.number} was subscribed to the channel {link_channel}")
            time.sleep(3)
        else:
            await client.join_chat(username_channel)
            print(f"Account {self.number} subscribed to the channel {username_channel}")
            time.sleep(3)

    async def unsubscribe(self, link_channel: str, client: PyrogramClient) -> None:
        """
        Отписаться аккаунтом от канала
        :param link_channel: Ссылка или имя на telegram канал
        :param client: PyrogramClient
        :return: None
        """
        username_channel = link_channel.split("/")[-1]
        sub = await self.check_subscribe(username_channel, client)
        if sub:
            await client.leave_chat(username_channel)
            print(f"Account {self.number} unsubscribed from the channel {username_channel}")
            time.sleep(3)

        else:
            print(f"Account {self.number} is not subscribed to the channel {username_channel}")
            time.sleep(3)

    @staticmethod
    def run(client, action, *args) -> None:
        """
        Запуск в асинхронном режиме необходимые фунции
        :param client: Client_Pyrogram
        :param action: необходимая функция
        :param args: позиционные аргументы
        :return: None
        """
        client.run(action(*args, client))
