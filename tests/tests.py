import asyncio
import os

from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()

api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")


async def main():
    async with Client("my_account", api_id, api_hash) as app:
        async for dialog in app.get_dialogs():
            print(dialog)


asyncio.run(main())
