import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
from datetime import datetime
import pytz
import itertools

# 🔑 O'zingizning ma'lumotlaringizni kiriting
API_ID = 21716532
API_HASH = "4a9ea732220e7d827166f5b0780426c4"
STRING_SESSION = "1ApWapzMBu2aSZ2JY9LBc92awATHivnYj7i_0dnfetj1UpZsOSWbK9721JmaLkKxaSyFZxbJC9k6qmxcqyLN3jFxf-iSoO9sXFM0tgZrvJwxPBphsfS9RY4nax1LDJ7OIUKHHynKoVESgH3haCJf81ThHYcATWMavKvIOZstJ8iLedbbGDVh1IKLpsJSMh3tSYKqhQAlRiz7cbpNXuL9pYkui_DEriTXQKlVajhoHW6VnZw_faL0Psp5KlMIP8sXYmypwC-CF8r_mmkrY3GAfnBGCwFzVGx4QPVdO7t4tE3TG95QkXgU0FxOK0ijFCwQal88xuLSGt9HshtTv-ykWrGSi7OOQMhg="

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

# 🇺🇿 Uzbekistan vaqti
uzb_tz = pytz.timezone("Asia/Tashkent")

# ⏰ Soatni turli toza uslublarda chiqarish
def time_styles(time_str):
    return [
        f"{time_str}",                 # Default 22:55
        f"```{time_str}```",           # Monospace
        f"**{time_str}**",             # Bold
        f"__{time_str}__",             # Bold+Underline
        f"*{time_str}*",               # Italic
        f"~{time_str}~",               # Strike-Through
        f"^{time_str}^",               # Superscript-style
        f"_{time_str}_",               # Subscript-style
        f"𝙱𝚘𝚕𝚍 {time_str}",           # Bold Serif
        f"𝔻𝕊 {time_str}",              # Double Struck
    ]

# ⏳ Familiyaga har daqiqa soat qo‘yish
async def update_time():
    styles_cycle = itertools.cycle(time_styles("22:55"))
    while True:
        now = datetime.now(uzb_tz).strftime("%H:%M")
        style_time = next(styles_cycle).replace("22:55", now)
        try:
            await client(UpdateProfileRequest(
                last_name=style_time  # familiya joyida soat
            ))
        except Exception as e:
            print("Xato:", e)
        await asyncio.sleep(60)  # 1 daqiqada yangilash

# 🤖 Avto-javob faqat lichka (bitta xabarga bitta javob)
@client.on(events.NewMessage)
async def handler(event):
    if event.is_private:
        # reply o‘rniga respond ishlatamiz, Telethon bitta javobni ta’minlaydi
        await event.respond("Salom! Javobingizni ko‘rib chiqaman 😊")

async def main():
    await client.start()
    print("🤖 Bot ishga tushdi!")
    await update_time()

with client:
    client.loop.run_until_complete(main())
