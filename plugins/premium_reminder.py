
import asyncio
from database.users_chats_db import db
from TechVJ.bot import TechVJBot

async def premium_reminder():
    while True:
        try:
            cursor = await db.get_expiring_premium_users()

            async for user in cursor:
                try:
                    await TechVJBot.send_message(
                        chat_id=user["id"],
                        text=(
                            "⚠️ **Premium Expiry Reminder**\n\n"
                            "Hello,\n\n"
                            "Your Premium Plan will expire in **3 days**.\n\n"
                            "To continue enjoying Premium features, please renew your plan before it expires.\n\n"
                            "📩 Contact Admin to renew your Premium.\n\n"
                            "Thank You ❤️"
                        )
                    )

                    await db.users.update_one(
                        {"id": user["id"]},
                        {"$set": {"reminder_sent": True}}
                    )

                except Exception as e:
                    print(f"Reminder Error: {e}")

            await asyncio.sleep(86400)

        except Exception as e:
            print(f"Premium Reminder Loop Error: {e}")
            await asyncio.sleep(300)
