import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users_chats_db import db
from TechVJ.bot import TechVJBot


async def premium_reminder():
    while True:
        try:
            # =========================
            # 3 Days Before Expiry
            # =========================
            cursor = await db.get_expiring_premium_users()

            async for user in cursor:
                try:
                    await TechVJBot.send_message(
                        chat_id=user["id"],
                        text=(
                            f"⚠️ **𝙋𝙍𝙀𝙈𝙄𝙐𝙈 𝙀𝙓𝙋𝙄𝙍𝙔 𝙍𝙀𝙈𝙄𝙉𝘿𝙀𝙍** ⚠️\n\n"
                            f"**𝙃𝙚𝙮 👋 {user.get('name', 'User')},**\n\n"
                            "**ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ɪꜱ ɢᴏɪɴɢ ᴛᴏ ᴇxᴘɪʀᴇ ɪɴ 𝟯 ᴅᴀʏꜱ. ʀᴇɴᴇᴡ ꜱᴏᴏɴ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ ᴇɴᴊᴏʏɪɴɢ ᴀʟʟ ᴘʀᴇᴍɪᴜᴍ ꜰᴇᴀᴛᴜʀᴇꜱ.**\n\n"
                            "**📌 𝘾𝙡𝙞𝙘𝙠 /plan 𝙁𝙤𝙧 𝙋𝙧𝙞𝙘𝙚𝙨.**"
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "💎 Contact Admin",
                                        url="https://t.me/YOUR_USERNAME"
                                    )
                                ]
                            ]
                        )
                    )

                    await db.users.update_one(
                        {"id": user["id"]},
                        {"$set": {"reminder_3days_sent": True}}
                    )

                except Exception as e:
                    print(f"3 Days Reminder Error: {e}")

            # =========================
            # Premium Expired
            # =========================
            cursor = await db.get_expired_today_users()

            async for user in cursor:
                try:
                    await TechVJBot.send_message(
                        chat_id=user["id"],
                        text=(
                            f"❌ **𝙋𝙍𝙀𝙈𝙄𝙐𝙈 𝙀𝙓𝙋𝙄𝙍𝙀𝘿** ❌\n\n"
                            f"**𝙃𝙚𝙮 👋 {user.get('name', 'User')},**\n\n"
                            "**ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ʜᴀꜱ ᴇxᴘɪʀᴇᴅ. ʀᴇɴᴇᴡ ɴᴏᴡ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ ᴇɴᴊᴏʏɪɴɢ ᴀʟʟ ᴘʀᴇᴍɪᴜᴍ ꜰᴇᴀᴛᴜʀᴇꜱ.**\n\n"
                            "**📌 𝘾𝙡𝙞𝙘𝙠 /plan 𝙁𝙤𝙧 𝙋𝙧𝙞𝙘𝙚𝙨.**"
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "💎 Contact Admin",
                                        url="https://t.me/YOUR_USERNAME"
                                    )
                                ]
                            ]
                        )
                    )

                    await db.users.update_one(
                        {"id": user["id"]},
                        {"$set": {"expiry_reminder_sent": True}}
                    )

                except Exception as e:
                    print(f"Expiry Reminder Error: {e}")

            # Check every 1 hour
            await asyncio.sleep(3600)

        except Exception as e:
            print(f"Premium Reminder Loop Error: {e}")
            await asyncio.sleep(300)
