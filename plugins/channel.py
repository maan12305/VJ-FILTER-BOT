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
        
        filename = re.sub(r'\[@.*?\]', '', filename)      # [@ClipmateZone]
        filename = re.sub(r'\[.*?\]', '', filename)       # [Hindi]
        filename = re.sub(r'[_\.-]+', ' ', filename)
        # Remove S04E09
        filename = re.sub(r'\bS\d{1,2}E\d{1,2}\b','',filename,flags=re.IGNORECASE)
        # Remove Episode 09 / Episode-09
        filename = re.sub(r'\bEpisode\s*-?\s*\d+\b','',filename,flags=re.IGNORECASE)
        # Remove Season 4
        filename = re.sub(r'\bSeason\s*\d+\b','',filename,flags=re.IGNORECASE)
        # Remove S04 / E09
        filename = re.sub(r'\bS\d{1,2}\b','',filename,flags=re.IGNORECASE)
        filename = re.sub(r'\bE\d{1,2}\b','',filename,flags=re.IGNORECASE)
        # keep year but remove brackets
        filename = filename.replace("(", " ")
        filename = filename.replace(")", " ")
        filename = ' '.join(filename.split())

        # Remove common junk words
        filename = re.sub(r'\b(Movie|HDTC|HDTS|HDRip|HQS|Proper|Remux|Uncut|Extended|Complete|NF|AMZN|DSNP|SonyLIV|ZEE5|JioHotstar|WEBRip|WEB-DL|BluRay|BRRip|DVDRip|ORG|Hindi|English|Tamil|Telugu|Malayalam|Marathi|Gujarati|Japnese|Punjabi|Kannada|Bengali|Gujarati|Dual|Multi|AAC|DDP|HEVC|x264|x265|ESub|ESubs|HC|HQ|CAM|TS|TC|Cin|Cinevood|720p|1080p|2160p|4K)\b','',filename,flags=re.IGNORECASE
                         )

        filename = ' '.join(filename.split())

        match = re.search(r'^(.*?)\b(19\d{2}|20\d{2})\b',filename,flags=re.IGNORECASE
       )

        if match:
            title = re.sub(r'[^a-zA-Z0-9 ]', '', match.group(1)).strip()
            year = match.group(2)
            search = f"{title} {year}"
        else:
            title = filename
            search = filename

        print("CLEANED FILENAME:", filename)
        print("TITLE:", title)
        print("YEAR:", year if match else "Not Found")

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

        filename_lower = filename.lower()

        quality = "Unknown"
        if "hdtc" in filename_lower:
            quality = "HDTC"
        elif "hdts" in filename_lower:
            quality = "HDTS"
        elif "camrip" in filename_lower or "cam" in filename_lower:
            quality = "CAMRip"
        elif "web-dl" in filename_lower or "webdl" in filename_lower:
            quality = "WEB-DL"
        elif "webrip" in filename_lower:
            quality = "WEBRip"
        elif "hdrip" in filename_lower:
            quality = "HDRip"
        elif "bluray" in filename_lower:
            quality = "BluRay"
        elif "brrip" in filename_lower:
            quality = "BRRip"
        elif "dvdrip" in filename_lower:
            quality = "DVDRip"
        elif "predvd" in filename_lower:
            quality = "PreDVD"
        elif "hd" in filename_lower:
            quality = "HDRip"
            
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
**📀 Quality - {quality}**
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

        poster = imdb.get("poster")
        if poster:
            await bot.send_photo(
                chat_id=MOVIE_UPDATE_CHANNEL,
                photo=poster,
                caption=caption,
                reply_markup=buttons
            )
        else:
            await bot.send_message(
                chat_id=MOVIE_UPDATE_CHANNEL,
                text=caption,
                reply_markup=buttons
            )
        
    except Exception:
        import traceback
        traceback.print_exc()
