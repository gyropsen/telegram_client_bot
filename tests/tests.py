# from telethon import TelegramClient
#
# # Use your own values from my.telegram.org
# api_id = 24351455
# api_hash = '4a48e819a4d21a3187b378988c97c256'
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


import asyncio
from pyrogram import Client

api_id = 24351455
api_hash = "4a48e819a4d21a3187b378988c97c256"


async def main():
    async with Client("my_account", api_id, api_hash) as app:
        async for dialog in app.get_dialogs():
            print(dialog)


asyncio.run(main())
