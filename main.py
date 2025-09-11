import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
from datetime import datetime
import pytz
import itertools

API_ID = 21716532
API_HASH = "4a9ea732220e7d827166f5b0780426c4"
STRING_SESSION = "YANGI_STRING_SESSIONINGIZNI_BU_YERGA_QOYING"

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
uzb_tz = pytz.timezone("Asia/Tashkent")

# --- Turli fontlarda soat (faqat raqam va :) ---
def style_times(hhmm):
    return [
        hhmm,
        ''.join({'0':'𝟶','1':'𝟷','2':'𝟸','3':'𝟹','4':'𝟺','5':'𝟻','6':'𝟼','7':'𝟽','8':'𝟾','9':'𝟿',':':':'}.get(c,c) for c in hhmm),
        ''.join({'0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵',':':':'}.get(c,c) for c in hhmm),
        ''.join({'0':'𝟘','1':'𝟙','2':'𝟚','3':'𝟛','4':'𝟜','5':'𝟝','6':'𝟞','7':'𝟟','8':'𝟠','9':'𝟡',':':':'}.get(c,c) for c in hhmm),
        ''.join({'0':'⓿','1':'①','2':'②','3':'③','4':'④','5':'⑤','6':'⑥','7':'⑦','8':'⑧','9':'⑨',':':':'}.get(c,c) for c in hhmm),
    ]

async def update_time():
    while True:
        now = datetime.now(uzb_tz).strftime("%H:%M")
        for s in style_times(now):
            await client(UpdateProfileRequest(last_name=s))
            await asyncio.sleep(60)
            now = datetime.now(uzb_tz).strftime("%H:%M")

# === Avto-javob faqat lichkaga, foydalanuvchiga bir marta ===
answered_users = set()

@client.on(events.NewMessage)
async def handler(event):
    if event.is_private:
        user_id = event.sender_id
        if user_id not in answered_users:
            await event.respond("Salom! Javobingizni ko‘rib chiqaman 😊")
            answered_users.add(user_id)

async def main():
    await client.start()
    print("🤖 Bot ishga tushdi!")
    await update_time()

with client:
    client.loop.run_until_complete(main())
