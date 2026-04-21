import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

# Получаем токен и ссылку из переменных среды
BOT_TOKEN = os.getenv("BOT_TOKEN")
ACCESS_LINK = os.getenv("ACCESS_LINK")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Языковые кнопки
lang_kb = InlineKeyboardMarkup(row_width=2)
lang_kb.add(
    InlineKeyboardButton("🇷🇺 RU", callback_data="lang_ru"),
    InlineKeyboardButton("🇬🇧 ENG", callback_data="lang_eng")
)

# Основное меню
def main_menu(lang="ru"):
    if lang == "ru":
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(
            InlineKeyboardButton("💰 Тарифы", callback_data="tariffs"),
            InlineKeyboardButton("📩 Оформить подписку", callback_data="subscribe"),
            InlineKeyboardButton("🆘 Поддержка", callback_data="support")
        )
    else:
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(
            InlineKeyboardButton("💰 Tariffs", callback_data="tariffs"),
            InlineKeyboardButton("📩 Subscribe", callback_data="subscribe"),
            InlineKeyboardButton("🆘 Support", callback_data="support")
        )
    return kb

# Тарифы
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

# Кнопки для подписки
subscribe_kb = InlineKeyboardMarkup(row_width=1)
subscribe_kb.add(
    InlineKeyboardButton("BRONZE 💎", url=ACCESS_LINK),
    InlineKeyboardButton("SILVER 💎", url=ACCESS_LINK),
    InlineKeyboardButton("GOLD 💎", url=ACCESS_LINK)
)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Выберите язык / Choose language:", reply_markup=lang_kb)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("lang_"))
async def choose_lang(callback_query: types.CallbackQuery):
    lang = "ru" if callback_query.data == "lang_ru" else "eng"
    await bot.send_message(callback_query.from_user.id, "Главное меню:" if lang=="ru" else "Main menu:", reply_markup=main_menu(lang))

@dp.callback_query_handler(lambda c: c.data == "tariffs")
async def show_tariffs(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, tariffs_text["ru"])

@dp.callback_query_handler(lambda c: c.data == "subscribe")
async def show_subscribe(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Выберите тариф:", reply_markup=subscribe_kb)

@dp.callback_query_handler(lambda c: c.data == "support")
async def show_support(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, f"Для поддержки напишите сюда: {ACCESS_LINK}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
