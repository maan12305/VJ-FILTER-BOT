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
                            "⚠️ **Premium Expiry Reminder** ⚠️\n\n"
                            "👋 Hello,\n\n"
                            "Your **Premium Membership** will expire in **3 days**.\n\n"
                            "✨ Renew now to continue enjoying:\n"
                            "• Unlimited Access\n"
                            "• Premium Features\n"
                            "• Fast Service\n\n"
                            "⏳ Don't wait until your premium expires.\n\n"
                            "👇 Click the button below to contact the Admin."
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "📩 Contact Admin",
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
            # Expiry Day Reminder
            # =========================
            cursor = await db.get_expired_today_users()

            async for user in cursor:
                try:
                    await TechVJBot.send_message(
                        chat_id=user["id"],
                        text=(
                            "❌ **Premium Expired** ❌\n\n"
                            "👋 Hello,\n\n"
                            "Your **Premium Membership** has expired.\n\n"
                            "🚫 Premium features are no longer available.\n\n"
                            "💎 Renew your Premium now to continue enjoying all Premium benefits.\n\n"
                            "👇 Click the button below to renew."
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "💎 Renew Premium",
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

            # Check every hour
            await asyncio.sleep(3600)

        except Exception as e:
            print(f"Premium Reminder Loop Error: {e}")
            await asyncio.sleep(300)
