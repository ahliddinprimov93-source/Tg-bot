from telethon import TelegramClient, events
from telethon.sessions import StringSession
from pytz import timezone
from datetime import datetime
import asyncio
import random

api_id    = 21716532       # o'zingizning api_id
api_hash  = "4a9ea732220e7d827166f5b0780426c4"
session   = "1ApWapzMBu565tRLfq_pGXB1VyoV2vN6gjm0M_SUF9fy8ywDVejybs_iiIlJ_SJokKznQWTHIKlK1ON_NZpEjHNcM-Q0AjlxzPnHo0So_PDNZjoXhlXkx8QVvxNH4VkbmHj350HaXkD3KWXkcwnLKqfBwWv785XbZpgr9qRg1GBNEl-dlokg_vJDUGi56Mh__NyqLgl8HN-XKGEiIn-jLtL-qQn1O-ST6LCuoVAn81L29hS056TTl0ijVA-lh3LEpi2-NRW_6uUGO-KXTzvyEyDiYjTV5j4mdYAmD8LFjdK8PRsvSYt96pGtlW6vpIxsGViZA-uZN5Qme6mEa9iMwhdIVCj3cRe0="   # yangi StringSession kiriting

client = TelegramClient(StringSession(session), api_id, api_hash)

# 25 ta uslub – raqamli + rim
styles = [
    # 15 ta raqamli uslub
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

    # 10 ta Rim uslubi – funksiya orqali
    "ROMAN", "BOLD_ROMAN", "ITALIC_ROMAN", "FULLWIDTH_ROMAN",
    "SCRIPT_ROMAN", "FRAKTUR_ROMAN", "DOUBLESTRUCK_ROMAN",
    "SUP_ROMAN", "SUB_ROMAN", "CIRCLED_ROMAN"
]

# Raqam -> rim konvert
roman_map = [
    (1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),
    (100,"C"),(90,"XC"),(50,"L"),(40,"XL"),
    (10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")
]
def int_to_roman(num):
    res=""
    for val,rom in roman_map:
        while num>=val:
            res+=rom
            num-=val
    return res

# Rim uslublarini bezash
def decorate_roman(h, m, style):
    h_r, m_r = int_to_roman(int(h)), int_to_roman(int(m))
    if style=="BOLD_ROMAN":
        return f"𝗛𝗛:{m_r}".replace("HH",h_r)
    if style=="ITALIC_ROMAN":
        return f"𝑯𝑯:{m_r}".replace("HH",h_r)
    if style=="FULLWIDTH_ROMAN":
        return f"ＨＨ:{m_r}".replace("HH",h_r)
    if style=="SCRIPT_ROMAN":
        return f"𝓗𝓗:{m_r}".replace("HH",h_r)
    if style=="FRAKTUR_ROMAN":
        return f"𝔥𝔥:{m_r}".replace("hh",h_r.lower())
    if style=="DOUBLESTRUCK_ROMAN":
        return f"𝕳𝕳:{m_r}".replace("HH",h_r)
    if style=="SUP_ROMAN":
        return f"{h_r}:{m_r}".translate(str.maketrans(
            "IVXLCDM","ᴵⱽˣᴸᶜᴰᴹ"))
    if style=="SUB_ROMAN":
        return f"{h_r}:{m_r}".translate(str.maketrans(
            "IVXLCDM","ᵢᵥₓₗ꜀ᵈₘ"))
    if style=="CIRCLED_ROMAN":
        return f"Ⓡ{h_r} : {m_r}"
    return f"{h_r}:{m_r}"

async def updater():
    while True:
        now = datetime.now(timezone('Asia/Tashkent'))
        h, m = now.strftime("%H"), now.strftime("%M")
        style = random.choice(styles)
        if isinstance(style, dict):     # oddiy raqamli
            new_name = f"{h.translate(style)}:{m.translate(style)}"
        elif isinstance(style, str) and style.endswith("_ROMAN") or style=="ROMAN":
            new_name = decorate_roman(h, m, style)
        else:
            # default fallback
            new_name = f"{h}:{m}"
        try:
            await client(functions.account.UpdateProfileRequest(last_name=new_name))
        except Exception as e:
            print("Update error:", e)
        await asyncio.sleep(60)  # 1 daqiqada bir marta

@client.on(events.NewMessage(pattern="^/start$"))
async def start_msg(event):
    await event.reply("Soat yangilash boshlandi ✅")

async def main():
    await client.start()
    asyncio.create_task(updater())
    print("Bot ishga tushdi…")
    await client.run_until_disconnected()

asyncio.run(main())
