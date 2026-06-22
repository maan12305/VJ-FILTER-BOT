from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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
        print("FILE NAME:", media.file_name)

        import re
        
        filename = media.file_name.rsplit(".", 1)[0]
        
        filename = re.sub(r'[_\.-]+', ' ', filename)
        filename = ' '.join(filename.split())

        # Remove common junk words
        filename = re.sub(r'\b(Movie|HDTC|HDTS|HDRip|WEBRip|WEB-DL|BluRay|Hindi|English|Tamil|Telugu|Malayalam|Marathi|Punjabi|AAC|x264|x265|HEVC|ESub|HC)\b','',filename,flags=re.IGNORECASE
       )

        filename = ' '.join(filename.split())

        match = re.search(r'^(.*?)\b(19\d{2}|20\d{2})\b',filename,flags=re.IGNORECASE
       )

        if match:
            title = match.group(1).strip()
            year = match.group(2)
            search = f"{title} {year}"
        else:
            title = filename
            search = filename

        print("SEARCH NAME:", search)
        print("FINAL SEARCH:", search)

        imdb = await get_poster(search)

        if not imdb and match:
            print("TRYING TITLE ONLY SEARCH:", title)
            imdb = await get_poster(title)

        print("IMDB RESULT:", imdb)
                     
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

**📆 Year - {imdb.get('year', 'N/A')}** 
**🎥 Genre - {imdb.get('genres', 'N/A')}**
**📀 Format - {quality}**
**🔊 Audio - {language}**
"""
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Get File 📂",
                        url=f"https://t.me/maan_file_store_BOT?start=search_{imdb.get('title').replace(' ', '_')}"
                    )
                ]
            ]
        )

        await bot.send_photo(
            chat_id=MOVIE_UPDATE_CHANNEL,
            photo=imdb.get("poster"),
            caption=caption,
            reply_markup=buttons
        )

    except Exception:
        import traceback
        traceback.print_exc()
