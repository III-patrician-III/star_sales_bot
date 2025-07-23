import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.start import register_start_handlers
from handlers.payment import register_payment_handlers
from handlers.admin import register_admin_handlers
from handlers.crypto import crypto_webhook
from utils.config import load_config
from utils.wallet_client import wallet_client_init

async def start_webhook():
    app = web.Application()
    app.router.add_post("/crypto_webhook", crypto_webhook)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

async def main():
    cfg = load_config(".env")
    await wallet_client_init(cfg)

    bot = Bot(token=cfg["BOT_TOKEN"], parse_mode="HTML")
    dp  = Dispatcher(storage=MemoryStorage())

    register_start_handlers(dp)
    register_payment_handlers(dp, cfg)
    register_admin_handlers(dp)

    # Run both polling and webhook
    await asyncio.gather(
        dp.start_polling(bot),
        start_webhook()
    )

if __name__ == "__main__":
    asyncio.run(main())
