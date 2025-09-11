import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
from datetime import datetime
import pytz
import itertools

# 🔑 O'zingizning ma'lumotlaringiz
API_ID = 21716532
API_HASH = "4a9ea732220e7d827166f5b0780426c4"
STRING_SESSION = "1ApWapzMBuxoGsjidD01xlWyimQjv4WhFZKNk9crjVxK5iJLJgosY_2QyvqhD2NEn4UQgjTdpX_qljuKZhCyfKy1QMhUzd9Hi5fNmZm7G8LtnqA67XSG-cB3NIn8QxaPV8MErhtV1YJQcETIckNJk8LUkDrQrxPk2fKjaY6qcSTJZwtTWn2rDZZUg6ztNocSPwPNNo0nWCiiFSJIlnHDz0Dyr1zHyHeq-cDFhoktSelSJyEEdsbPG2WdXxJS9Zzp2GztEZC7Jd0eMoamCGYoJuLcy8F0uJYZd4JfX39Alf5ymidMDWcK7it-JFa1GoUhR9glVZkcRnVP5wkEpUhsM2Jk10zSL09c="

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

# ⏰ Uzbekistan vaqti zonasi
uzb_tz = pytz.timezone("Asia/Tashkent")

# Soatni turli stilda ko‘rsatish funksiyalari
def format_time_styles(time_str):
    styles = {
        "Default": time_str,
        "Monospace": f"```{time_str}```",
        "Strike-Through": "".join([ch + "\u0336" for ch in time_str]),
        "SuperScript": "".join([ch + "\u2070" for ch in time_str]),
        "SubScript": "".join([ch + "\u2080" for ch in time_str]),
        "Bold": f"**{time_str}**",
        "Bold Serif": f"𝙱𝚘𝚕𝚍 {time_str}",
        "Double Struck": f"𝔻𝕊 {time_str}",
        "Circle": f"ⓒ {time_str} ⓣ",
        "Double Circle": f"🅞 {time_str} 🅞",
        "Dark Circle": f"⬤ {time_str} ⬤",
        "Crazify": f"~{time_str}~"
    }
    return styles

# Har minutda familiyaga soat qo‘yish
async def update_time():
    styles_cycle = itertools.cycle(list(format_time_styles("22:55").values()))
    while True:
        now = datetime.now(uzb_tz).strftime("%H:%M")
        style_time = next(styles_cycle).replace("22:55", now)
        try:
            await client(UpdateProfileRequest(
                last_name=style_time  # familiya joyida soat bo‘ladi
            ))
        except Exception as e:
            print("Xato:", e)
        await asyncio.sleep(60)  # 1 minutdan keyin yangilash

# Avto javob faqat lichkaga
@client.on(events.NewMessage)
async def handler(event):
    if event.is_private:  # faqat lichka uchun
        await event.respond(
            "Salom yozganingizdan hursandman 😊 Tez orada javob yozaman!"
        )

async def main():
    await client.start()
    print("🤖 Bot ishga tushdi!")
    await update_time()

# <<< Shu satr bilan tugatish kerak edi
with client:
    client.loop.run_until_complete(main())
