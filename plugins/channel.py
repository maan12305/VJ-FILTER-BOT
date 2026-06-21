
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
        
        search = media.file_name.replace(".", " ")
        import re

        search = re.sub(
        r'[_\.-]+',
        ' ',
        search
       )
        search = re.sub(
        r'\b(480p|720p|1080p|2160p|WEB[- ]DL|WEBRip|HDRip|BluRay|AMZN|NF|Hindi|Dual|AAC2 0|AAC|H 265|HEVC|x264|x265|The Punisher)\b',
        '',
        search,
        flags=re.IGNORECASE
       )
        
        search = re.sub(r'\[@.*?\]', '', search)
        search = re.sub(r'\(.*?\)', '', search)
        search = re.sub(r'\bS\d+\b', '', search, flags=re.IGNORECASE)
        search = re.sub(r'\bHi\b', '', search, flags=re.IGNORECASE)
        search = re.sub(r'\bmkv\b', '', search, flags=re.IGNORECASE)
        search = re.sub(r'\b10bit\b', '', search, flags=re.IGNORECASE)
        search = re.sub(r'\bORG\b', '', search, flags=re.IGNORECASE)
        search = re.sub(r'\[.*?\]', '', search)
        search = re.sub(r'\bHDTS\b', '', search, flags=re.IGNORECASE)
        search = re.sub(r'\bEnglish\b', '', search, flags=re.IGNORECASE)
        search = re.sub(r'\bx264\b', '', search, flags=re.IGNORECASE)

        search = ' '.join(search.split())

        print("SEARCH NAME:", search)
        
        print("FINAL SEARCH:", search)
        
        imdb = await get_poster(search)
        
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

    except Exception:
        import traceback
        traceback.print_exc()
