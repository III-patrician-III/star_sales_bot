from telethon import TelegramClient
import os

wallet_client = None

async def wallet_client_init(cfg):
    global wallet_client
    wallet_client = TelegramClient("wallet_session", cfg["API_ID"], cfg["API_HASH"])
    await wallet_client.start()

async def send_stars(to_user_id: int, amount: int):
    # Sending XTR via Telethon by username
    entity = await wallet_client.get_entity(to_user_id)
    await wallet_client.send_message(entity, f"Отправляю вам {amount} ⭐️ (XTR)")
    # Here implement actual XTR transfer logic when API is available
