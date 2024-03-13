import logging
import os
import random
import time
from pathlib import Path

from dotenv import load_dotenv
from telethon import types
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest

from src.classes.account_abc import ABCAccount

logger = logging.getLogger(__name__)
load_dotenv()


class TGAccountTelethon(ABCAccount):
    proxy = {
        "proxy_type": os.getenv("proxy_type"),  # (mandatory) protocol to use (see above)
        "addr": os.getenv("proxy_addr"),  # (mandatory) proxy IP address
        "port": int(os.getenv("proxy_port")),  # (mandatory) proxy port number
        "username": os.getenv("proxy_username"),  # (optional) username if the proxy requires auth
        "password": os.getenv("proxy_password"),  # (optional) password if the proxy requires auth
    }

    def __init__(self, number):
        self.number = number
        self.session = ""
        self.premium = False

    async def get_status_premium(self, client: TelegramClient) -> None:
        """
        Проверяет наличие премиум подписки
        :param client: TelegramClient
        :return: None
        """
        user_info = await client.get_me()
        self.premium = user_info.premium

    def get_client(self) -> TelegramClient:
        """
        Возвращает телеграм клиент
        :return: TelegramClient
        """
        session: str = str(Path(self.sessions_path, "for_telethon", self.number + ".session"))
        client = TelegramClient(
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
    async def check_subscribe(username_channel: str, client: TelegramClient) -> bool:
        """
        Проверяет, подписан ли аккаунт на канал
        :param username_channel: Ссылка или имя на telegram канал
        :param client: TelegramClient
        :return: True - если, аккаунт подписан, False - если нет
        """
        dialogs = await client.get_dialogs()
        channel = await client.get_entity(username_channel)
        for dialog in dialogs:
            if not isinstance(dialog.entity, types.Chat):
                if dialog.entity.id == channel.id:
                    return True
        return False

    async def subscribe(self, username_channel: str, client: TelegramClient) -> None:
        """
        Подписаться аккаунтом на канал
        :param username_channel: Ссылка или имя на telegram канал
        :param client: TelegramClient
        :return: None
        """
        sub = await self.check_subscribe(username_channel, client)
        if sub:
            print(f"Account {self.number} was subscribed to the channel {username_channel}")
            time.sleep(3)
        else:
            channel = await client.get_entity(username_channel)
            await client(JoinChannelRequest(types.InputChannel(channel.id, channel.access_hash)))
            print(f"Account {self.number} subscribed to the channel {username_channel}")
            time.sleep(3)

    async def unsubscribe(self, username_channel: str, client: TelegramClient) -> None:
        """
        Отписаться аккаунтом от канала
        :param username_channel: Ссылка или имя на telegram канал
        :param client: TelegramClient
        :return: None
        """
        sub = await self.check_subscribe(username_channel, client)
        if sub:
            channel = await client.get_entity(username_channel)
            await client(LeaveChannelRequest(types.InputChannel(channel.id, channel.access_hash)))
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
        client.loop.run_until_complete(action(*args, client))
