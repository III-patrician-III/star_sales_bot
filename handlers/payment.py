from aiogram import Router, types
from handlers.crypto import create_invoice

def register_payment_handlers(dp: Router, config):
    router = Router()

    @router.callback_query(lambda c: c.data.startswith("buy_"))
    async def handle_buy(call: types.CallbackQuery):
        _, stars, price = call.data.split("_")
        user_id = call.from_user.id
        pay_url = create_invoice(user_id, int(stars), int(price))
        await call.message.answer(f"Перейдите по ссылке и оплатите:
{pay_url}")

    dp.include_router(router)
