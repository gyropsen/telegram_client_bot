import asyncio
from pyrogram import Client
from dotenv import load_dotenv
import os

load_dotenv()

# from telethon import TelegramClient
# # Use your own values from my.telegram.org
# api_id = os.getenv("api_id")
# api_hash = os.getenv("api_hash")
#
#
# async def main():
#     info = await client.get_dialogs()
#     for i in info:
#         print(i.entity.id)
#
#
# # The first parameter is the .session file name (absolute paths allowed)
# with TelegramClient('anon', api_id, api_hash) as client:
#     client.loop.run_until_complete(main())


api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")


async def main():
    async with Client("my_account", api_id, api_hash) as app:
        async for dialog in app.get_dialogs():
            print(dialog)


asyncio.run(main())

#  is not callable
# 'coroutine' object is not callable
# /home/egor/PycharmProjects/telegram_client_bot/src/utils/utils.py:119: RuntimeWarning: coroutine 'TGAccountTelethon.subscribe' was never awaited
#   print(error)
# RuntimeWarning: Enable tracemalloc to get the object allocation traceback

