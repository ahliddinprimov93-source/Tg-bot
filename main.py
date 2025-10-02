# stay_online.py
from telethon import TelegramClient
import asyncio
import os

API_ID = int(os.environ.get("API_ID", "id"))
API_HASH = os.environ.get("API_HASH", "hash")
PHONE = os.environ.get("PHONE", "+79011142534")
SESSION_NAME = "stay_online_session"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def main():
    await client.start(phone=PHONE)
    print("Connected. Staying online…")
    # event loopni to‘xtatmasdan ishlatish
    await client.run_until_disconnected()

if name == "main":
    asyncio.run(main())
