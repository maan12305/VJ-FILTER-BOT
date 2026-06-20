from pyrogram import Client, filters
from info import CHANNELS, MOVIE_UPDATE_CHANNEL
from database.ia_filterdb import save_file
from utils import get_poster
import re

media_filter = filters.document | filters.video

@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
    media = getattr(message, message.media.value, None)
    media.caption = message.caption

    await save_file(media)
    print("MOVIE UPDATE CODE TRIGGERED")

    try:
        imdb = await get_poster(media.file_name)

        if not imdb:
            return

        filename = media.file_name

        quality = "Unknown"
        if "2160p" in filename.lower() or "4k" in filename.lower():
            quality = "4K"
        elif "1080p" in filename.lower():
            quality = "1080p"
        elif "720p" in filename.lower():
            quality = "720p"
        elif "480p" in filename.lower():
            quality = "480p"

        langs = re.findall(
            r'(Hindi|Tamil|Telugu|Malayalam|English|Kannada|Bengali|Punjabi)',
            filename,
            re.IGNORECASE
        )

        language = ", ".join(
            sorted(set(x.title() for x in langs))
        ) if langs else "Unknown"

        caption = f"""
<code>{imdb.get('title', 'Unknown')}</code> ✅

📆 Year - {imdb.get('year', 'N/A')}
🎥 Genre - {imdb.get('genres', 'N/A')}
📀 Format - {quality}
🔊 Audio - {language}
"""

        await bot.send_photo(
            chat_id=MOVIE_UPDATE_CHANNEL,
            photo=imdb.get("poster"),
            caption=caption
        )

    except Exception as e:
        print(f"Movie Update Error: {e}")
