from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
import asyncio, datetime, random

# 🔑 API ma'lumotlari
API_ID = 21716532
API_HASH = "4a9ea732220e7d827166f5b0780426c4"
STRING_SESSION = "1ApWapzMBuxoGsjidD01xlWyimQjv4WhFZKNk9crjVxK5iJLJgosY_2QyvqhD2NEn4UQgjTdpX_qljuKZhCyfKy1QMhUzd9Hi5fNmZm7G8LtnqA67XSG-cB3NIn8QxaPV8MErhtV1YJQcETIckNJk8LUkDrQrxPk2fKjaY6qcSTJZwtTWn2rDZZUg6ztNocSPwPNNo0nWCiiFSJIlnHDz0Dyr1zHyHeq-cDFhoktSelSJyEEdsbPG2WdXxJS9Zzp2GztEZC7Jd0eMoamCGYoJuLcy8F0uJYZd4JfX39Alf5ymidMDWcK7it-JFa1GoUhR9glVZkcRnVP5wkEpUhsM2Jk10zSL09c="

# Har xil fontlar
FONTS = [
    str.maketrans("0123456789:", "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿:"),
    str.maketrans("0123456789:", "⓿①②③④⑤⑥⑦⑧⑨:"),
    str.maketrans("0123456789:", "０１２３４５６７８９:"),
    str.maketrans("0123456789:", "❶❷❸❹❺❻❼❽❾⓿:"),
]

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

# 🕒 Nickname har daqiqada soat bilan yangilanadi
async def update_name():
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        style = random.choice(FONTS)
        fancy_time = now.translate(style)
        try:
            await client(UpdateProfileRequest(first_name=fancy_time))
        except Exception as e:
            print("Xato:", e)
        await asyncio.sleep(60)

# 📩 Har qanday xabarga avtomatik javob
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    await event.reply("Salom yozganingizdan hursandman 🙂 tez orada javob yozaman.")

async def main():
    asyncio.create_task(update_name())
    print("✅ Bot ishga tushdi (Render 24/7)")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
