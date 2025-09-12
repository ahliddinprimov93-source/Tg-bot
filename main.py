from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession
from pytz import timezone
from datetime import datetime
import asyncio, random, os
from aiohttp import web   # ★ NEW

api_id    = 21716532             # o'zingizning api_id
api_hash  = "4a9ea732220e7d827166f5b0780426c4"
session   = "1ApWapzMBu565tRLfq_pGXB1VyoV2vN6gjm0M_SUF9fy8ywDVejybs_iiIlJ_SJokKznQWTHIKlK1ON_NZpEjHNcM-Q0AjlxzPnHo0So_PDNZjoXhlXkx8QVvxNH4VkbmHj350HaXkD3KWXkcwnLKqfBwWv785XbZpgr9qRg1GBNEl-dlokg_vJDUGi56Mh__NyqLgl8HN-XKGEiIn-jLtL-qQn1O-ST6LCuoVAn81L29hS056TTl0ijVA-lh3LEpi2-NRW_6uUGO-KXTzvyEyDiYjTV5j4mdYAmD8LFjdK8PRsvSYt96pGtlW6vpIxsGViZA-uZN5Qme6mEa9iMwhdIVCj3cRe0="

client = TelegramClient(StringSession(session), api_id, api_hash)

# --- 25 ta uslub: 15 raqamli + 10 rim ---
styles = [
    str.maketrans("0123456789", "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"),
    str.maketrans("0123456789", "⓿①②③④⑤⑥⑦⑧⑨"),
    str.maketrans("0123456789", "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"),
    str.maketrans("0123456789", "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡"),
    str.maketrans("0123456789", "０１２３４５６７８９"),
    str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"),
    str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"),
    str.maketrans("0123456789", "𝔬𝔫𝔱𝔥𝔣𝔦𝔰𝔢𝔫𝔷"),
    str.maketrans("0123456789", "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳"),
    str.maketrans("0123456789", "𝗼𝗻𝘁𝗵𝗳𝗶𝘀𝗲𝗻𝘇"),
    str.maketrans("0123456789", "🄌①②③④⑤⑥⑦⑧⑨"),
    str.maketrans("0123456789", "➀➁➂➃➄➅➆➇➈➉"),
    str.maketrans("0123456789", "❶❷❸❹❺❻❼❽❾⓿"),
    str.maketrans("0123456789", "𝙊𝙉𝙏𝙃𝙁𝙄𝙎𝙀𝙉𝙕"),
    str.maketrans("0123456789", "𝘖𝘕𝘛𝘏𝘍𝘐𝘚𝘌𝘕𝘡"),
    # Rim uslublari
    "ROMAN","BOLD_ROMAN","ITALIC_ROMAN","FULLWIDTH_ROMAN",
    "SCRIPT_ROMAN","FRAKTUR_ROMAN","DOUBLESTRUCK_ROMAN",
    "SUP_ROMAN","SUB_ROMAN","CIRCLED_ROMAN"
]

roman_map = [
    (1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),
    (100,"C"),(90,"XC"),(50,"L"),(40,"XL"),
    (10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")
]
def int_to_roman(num):
    res=""
    for v,r in roman_map:
        while num>=v:
            res+=r; num-=v
    return res

def decorate_roman(h, m, style):
    h_r, m_r = int_to_roman(int(h)), int_to_roman(int(m))
    mapping = {
        "BOLD_ROMAN":       f"𝗛𝗛:{m_r}",
        "ITALIC_ROMAN":     f"𝑯𝑯:{m_r}",
        "FULLWIDTH_ROMAN":  f"ＨＨ:{m_r}",
        "SCRIPT_ROMAN":     f"𝓗𝓗:{m_r}",
        "FRAKTUR_ROMAN":    f"𝔥𝔥:{m_r}".replace("hh", h_r.lower()),
        "DOUBLESTRUCK_ROMAN": f"𝕳𝕳:{m_r}",
        "SUP_ROMAN": f"{h_r}:{m_r}".translate(str.maketrans("IVXLCDM","ᴵⱽˣᴸᶜᴰᴹ")),
        "SUB_ROMAN": f"{h_r}:{m_r}".translate(str.maketrans("IVXLCDM","ᵢᵥₓₗ꜀ᵈₘ")),
        "CIRCLED_ROMAN":    f"Ⓡ{h_r} : {m_r}"
    }
    return mapping.get(style, f"{h_r}:{m_r}").replace("HH", h_r)

async def updater():
    while True:
        now = datetime.now(timezone('Asia/Tashkent'))
        h, m = now.strftime("%H"), now.strftime("%M")
        style = random.choice(styles)
        if isinstance(style, dict):
            new_name = f"{h.translate(style)}:{m.translate(style)}"
        else:
            new_name = decorate_roman(h, m, style) if isinstance(style,str) else f"{h}:{m}"
        try:
            await client(functions.account.UpdateProfileRequest(last_name=new_name))
        except Exception as e:
            print("Update error:", e)
        await asyncio.sleep(60)

@client.on(events.NewMessage(pattern="^/start$"))
async def start_msg(event):
    await event.reply("Soat yangilash boshlandi ✅")

# --- ★ NEW: health-check web-server ---
async def start_webserver():
    async def ok(_): return web.Response(text="OK")
    app = web.Application()
    app.router.add_get("/", ok)
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Health-check server listening on port {port}")

async def main():
    await client.start()
    asyncio.create_task(updater())
    asyncio.create_task(start_webserver())   # ★ qo‘shildi
    print("Bot ishga tushdi…")
    await client.run_until_disconnected()

asyncio.run(main())
