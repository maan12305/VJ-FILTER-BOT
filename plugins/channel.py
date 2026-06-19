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

    year_match = re.search(r"(\d{4})", caption)
    year = year_match.group(1) if year_match else "N/A"

    audio_match = re.search(r"(.*?)", caption)
    audio = audio_match.group(1) if audio_match else "N/A"

    quality_match = re.search(
        r"(2160p|1440p|1080p|720p|480p)",
        caption,
        re.IGNORECASE
    )
    quality = quality_match.group(1) if quality_match else "N/A"

    format_match = re.search(
        r"(WEB-DL|WEBRip|HDRip|BluRay|HDTS)",
        caption,
        re.IGNORECASE
    )
    format_type = format_match.group(1) if format_match else "N/A"

    name = caption.split("(")[0].strip()

    text = f"""🎬 {name} ✅

📅 Year - {year}
🎥 Genre - N/A
💿 Format - {format_type}
🔊 Audio - {audio}
📺 Quality - {quality}"""

    await bot.send_message(
        UPDATE_CHANNEL,
        text
    )

except Exception as e:
    print(f"Movie Update Error: {e}")
