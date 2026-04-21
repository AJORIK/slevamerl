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
lang_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 RU", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇬🇧 ENG", callback_data="lang_eng")
        ]
    ]
)

# -------------------
# Главное меню
# -------------------
def main_menu(lang="ru") -> InlineKeyboardMarkup:
    if lang == "ru":
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💰 Тарифы", callback_data="tariffs")],
                [InlineKeyboardButton(text="📩 Оформить подписку", callback_data="subscribe")],
                [InlineKeyboardButton(text="🆘 Поддержка", callback_data="support")]
            ]
        )
    else:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💰 Tariffs", callback_data="tariffs")],
                [InlineKeyboardButton(text="📩 Subscribe", callback_data="subscribe")],
                [InlineKeyboardButton(text="🆘 Support", callback_data="support")]
            ]
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
# Кнопки подписки
# -------------------
subscribe_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="BRONZE 💎", url=ACCESS_LINK)],
        [InlineKeyboardButton(text="SILVER 💎", url=ACCESS_LINK)],
        [InlineKeyboardButton(text="GOLD 💎", url=ACCESS_LINK)]
    ]
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
        await bot.send_message(callback.from_user.id,
                               "Главное меню:" if lang=="ru" else "Main menu:",
                               reply_markup=main_menu(lang))
    elif data == "tariffs":
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
