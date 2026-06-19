#Don't Remove Credit @VJ_Bots
#Subscribe YouTube Channel For Amazing Bot @Tech_VJ
#Ask Doubt on telegram @KingVJ01

from pyrogram import Client, filters
from info import CHANNELS
from database.ia_filterdb import save_file
import re

UPDATE_CHANNEL = -1003730484035

media_filter = filters.document | filters.video

@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
media = getattr(message, message.media.value, None)
media.caption = message.caption

await save_file(media)

try:
    caption = message.caption or ""

    year = re.search(r"(\d{4})", caption)
    year = year.group(1) if year else "N/A"

    audio = re.search(r"(.*?)", caption)
    audio = audio.group(1) if audio else "N/A"

    quality = re.search(r"(2160p|1440p|1080p|720p|480p)", caption, re.I)
    quality = quality.group(1) if quality else "N/A"

    fmt = re.search(r"(WEB-DL|WEBRip|HDRip|BluRay|HDTS)", caption, re.I)
    fmt = fmt.group(1) if fmt else "N/A"

    name = caption.split("(")[0].strip()

    text = f"""

🎬 {name} ✅

📅 Year - {year}
🎥 Genre - N/A
💿 Format - {fmt}
🔊 Audio - {audio}
📺 Quality - {quality}
"""

    await bot.send_message(
        UPDATE_CHANNEL,
        text
    )

except Exception as e:
    print(f"Movie Update Error: {e}")
