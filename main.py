import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
from datetime import datetime, timedelta
import pytz
import itertools

API_ID = 21716532
API_HASH = "4a9ea732220e7d827166f5b0780426c4"
STRING_SESSION = "1ApWapzMBu2aSZ2JY9LBc92awATHivnYj7i_0dnfetj1UpZsOSWbK9721JmaLkKxaSyFZxbJC9k6qmxcqyLN3jFxf-iSoO9sXFM0tgZrvJwxPBphsfS9RY4nax1LDJ7OIUKHHynKoVESgH3haCJf81ThHYcATWMavKvIOZstJ8iLedbbGDVh1IKLpsJSMh3tSYKqhQAlRiz7cbpNXuL9pYkui_DEriTXQKlVajhoHW6VnZw_faL0Psp5KlMIP8sXYmypwC-CF8r_mmkrY3GAfnBGCwFzVGx4QPVdO7t4tE3TG95QkXgU0FxOK0ijFCwQal88xuLSGt9HshtTv-ykWrGSi7OOQMhg="

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
uzb_tz = pytz.timezone("Asia/Tashkent")

# --- faqat vaqtning o‘zi turli yozilishlarda ---
def time_styles(t):
    return [
        t,                                   # Default
        f"```{t}```",                         # Monospace
        ''.join(ch + '\u0336' for ch in t),   # Strike-Through
        ''.join(ch + '\u2070' for ch in t),   # SuperScript
        ''.join(ch + '\u2080' for ch in t),   # SubScript
        f"**{t}**",                           # Bold
        ''.join({'2':'𝟚','3':'𝟛','4':'𝟜','5':'𝟝','6':'𝟞','7':'𝟟','8':'𝟠','9':'𝟡','0':'𝟘',':':':'}[c] for c in t),  # Bold Serif digits
        ''.join({'0':'𝟘','1':'𝟙','2':'𝟚','3':'𝟛','4':'𝟜','5':'𝟝','6':'𝟞','7':'𝟟','8':'𝟠','9':'𝟡',':':':'}[c] for c in t), # Double Struck digits
        ''.join({'0':'⓪','1':'①','2':'②','3':'③','4':'④','5':'⑤','6':'⑥','7':'⑦','8':'⑧','9':'⑨',':':':'}[c] for c in t), # Circle digits
        ''.join({'0':'🄌','1':'①','2':'②','3':'③','4':'④','5':'⑤','6':'⑥','7':'⑦','8':'⑧','9':'⑨',':':':'}[c] for c in t), # Double Circle-ish
        ''.join({'0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8','9':'9',':':':'}[c] for c in t),    # Dark (simple)
        f"~{t}~"                              # Crazify
    ]

async def update_time():
    cycle = itertools.cycle(range(len(time_styles("22:55"))))
    while True:
        now = datetime.now(uzb_tz).strftime("%H:%M")
        idx = next(cycle)
        style_time = time_styles(now)[idx]
        try:
            await client(UpdateProfileRequest(last_name=style_time))
        except Exception as e:
            print("Xato:", e)
        await asyncio.sleep(60)

# ➜ Avto-javob: faqat lichkaga, foydalanuvchiga 1 daqiqada 1 marta
last_reply = {}

@client.on(events.NewMessage)
async def auto_reply(event):
    if not event.is_private:
        return
    uid = event.sender_id
    now = datetime.now()
    if uid not in last_reply or now - last_reply[uid] > timedelta(seconds=60):
        await event.respond("Salom yozganingizdan hursandman 😊 Tez orada javob yozaman!")
        last_reply[uid] = now

async def main():
    await client.start()
    print("✅ Bot ishga tushdi")
    await update_time()

with client:
    client.loop.run_until_complete(main())
