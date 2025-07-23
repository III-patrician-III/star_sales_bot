from aiogram import Router, types
from aiogram.filters import CommandStart, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from handlers.crypto import create_invoice

def register_start_handlers(dp: Router):
    router = Router()

    @router.message(CommandStart(deep_link=True))
    async def cmd_start(message: types.Message, command: CommandObject):
        payload = command.args or "none"
        await message.answer(f"Добро пожаловать! Ваш реферальный код: <b>{payload}</b>")
        builder = InlineKeyboardBuilder()
        packages = [
            (50, 70), (75, 105), (100, 135), (150, 202),
            (250, 337), (350, 472), (500, 675), (750, 1012),
            (1000, 1350), (1500, 2025)
        ]
        for stars, price in packages:
            builder.button(
                text=f"{stars} ⭐ за {price} ₽",
                callback_data=f"buy_{stars}_{price}"
            )
        builder.adjust(1)
        await message.answer("Выберите пакет:", reply_markup=builder.as_markup())

    dp.include_router(router)
