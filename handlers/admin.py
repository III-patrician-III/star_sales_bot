from aiogram import Router
from aiogram.filters import Command
import json
from utils.config import load_config

def register_admin_handlers(dp: Router):
    router = Router()
    cfg = load_config(".env")

    @router.message(Command("orders"))
    async def view_orders(message):
        if message.from_user.id not in cfg["ADMIN_IDS"]:
            return await message.answer("⛔ Доступ запрещен.")
        try:
            orders = json.load(open("data/orders.json", encoding="utf-8"))
        except FileNotFoundError:
            orders = []
        if not orders:
            return await message.answer("📭 Нет заказов.")
        text = "📦 Список заказов:"

        for i, o in enumerate(orders, 1):
            text += f"{i}. @{message.from_user.username} — {o['stars']} ⭐\n"
        await message.answer(text)

    dp.include_router(router)
