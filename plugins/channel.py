# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from info import CHANNELS
from database.ia_filterdb import save_file

media_filter = filters.document | filters.video

@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
    media = getattr(message, message.media.value, None)
    media.caption = message.caption
    await save_file(media)

    caption = message.caption or "New Movie Uploaded ✅"

    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("📂 Get File", url="https://t.me/maan_file_store_BOT?start=start")]]
    )

    await bot.send_message(
        chat_id=-1003730484035,
        text=caption,
        reply_markup=buttons,
        disable_web_page_preview=True
    )
