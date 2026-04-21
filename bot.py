import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
ACCESS_LINK = os.getenv("ACCESS_LINK")  # ссылка на личку

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# -------------------
# Языковые кнопки
# -------------------
lang_kb = InlineKeyboardMarkup()
lang_kb.row(
    InlineKeyboardButton("🇷🇺 RU", callback_data="lang_ru"),
    InlineKeyboardButton("🇬🇧 ENG", callback_data="lang_eng")
)

# -------------------
# Главное меню
# -------------------
def main_menu(lang="ru"):
    kb = InlineKeyboardMarkup()
    if lang == "ru":
        kb.add(
            InlineKeyboardButton("💰 Тарифы", callback_data="tariffs"),
            InlineKeyboardButton("📩 Оформить подписку", callback_data="subscribe"),
            InlineKeyboardButton("🆘 Поддержка", callback_data="support")
        )
    else:
        kb.add(
            InlineKeyboardButton("💰 Tariffs", callback_data="tariffs"),
            InlineKeyboardButton("📩 Subscribe", callback_data="subscribe"),
            InlineKeyboardButton("🆘 Support", callback_data="support")
        )
    return kb

# -------------------
# Тарифы
# -------------------
tariffs_text = {
    "ru": """
Тариф BRONZE
Подписка на мой приватный канал на 1 месяц.

Тариф SILVER
Личное общение со мной: разговоры о жизни и других темах.

Тариф GOLD
Подписка на приватный канал на 1 месяц + личное общение со мной.
""",
    "eng": """
Plan BRONZE
Subscription to my private channel for 1 month.

Plan SILVER
Personal communication with me: talks about life and other topics.

Plan GOLD
Subscription to private channel for 1 month + personal communication with me.
"""
}

# -------------------
# Подписка кнопки
# -------------------
subscribe_kb = InlineKeyboardMarkup()
subscribe_kb.add(
    InlineKeyboardButton("BRONZE 💎", url=ACCESS_LINK),
    InlineKeyboardButton("SILVER 💎", url=ACCESS_LINK),
    InlineKeyboardButton("GOLD 💎", url=ACCESS_LINK)
)

# -------------------
# Хендлеры
# -------------------
@dp.message()
async def handle_start(message: types.Message):
    if message.text == "/start":
        await message.answer("Выберите язык / Choose language:", reply_markup=lang_kb)

@dp.callback_query()
async def handle_callbacks(callback: types.CallbackQuery):
    data = callback.data
    if data in ["lang_ru", "lang_eng"]:
        lang = "ru" if data == "lang_ru" else "eng"
        await bot.send_message(callback.from_user.id, "Главное меню:" if lang=="ru" else "Main menu:", reply_markup=main_menu(lang))
    elif data == "tariffs":
        # Для простоты покажем русский
        await bot.send_message(callback.from_user.id, tariffs_text["ru"])
    elif data == "subscribe":
        await bot.send_message(callback.from_user.id, "Выберите тариф:", reply_markup=subscribe_kb)
    elif data == "support":
        await bot.send_message(callback.from_user.id, f"Для поддержки напишите сюда: {ACCESS_LINK}")

# -------------------
# Запуск бота
# -------------------
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
