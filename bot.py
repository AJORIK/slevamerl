import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

# Получаем токен из переменных окружения Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")
WALLET = "TAbriJG56DUcVFzW8jik3jPvwNtUrntda5"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ======= Клавиатура выбора языка =======
lang_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇷🇺 RU", callback_data="lang_ru"),
     InlineKeyboardButton(text="🇬🇧 ENG", callback_data="lang_en")]
])

# ======= Главное меню =======
def main_menu(lang="ru"):
    if lang == "ru":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📜 Тарифы", callback_data="tariffs")],
            [InlineKeyboardButton(text="💳 Получить доступ", callback_data="subscribe")],
            [InlineKeyboardButton(text="🛠 Поддержка", url="https://t.me/your_support")]  # замени на свою ссылку поддержки
        ])
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📜 Tariffs", callback_data="tariffs")],
            [InlineKeyboardButton(text="💳 Get Access", callback_data="subscribe")],
            [InlineKeyboardButton(text="🛠 Support", url="https://t.me/your_support")]
        ])
    return kb

# ======= Клавиатура тарифов =======
tariffs_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="BRONZE - 5000", url=f"https://t.me/{WALLET}")],
    [InlineKeyboardButton(text="SILVER - 5000", url=f"https://t.me/{WALLET}")],
    [InlineKeyboardButton(text="GOLD - 7500", url=f"https://t.me/{WALLET}")]
])

# ======= Обработчики =======
@dp.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer("Выберите язык / Choose language:", reply_markup=lang_kb)

@dp.callback_query(lambda c: c.data in ["lang_ru", "lang_en"])
async def lang_callback_handler(callback: CallbackQuery, state: FSMContext):
    lang = "ru" if callback.data == "lang_ru" else "en"
    await callback.message.edit_text(
        "Главное меню:" if lang == "ru" else "Main menu:", 
        reply_markup=main_menu(lang)
    )

@dp.callback_query(lambda c: c.data == "tariffs")
async def tariffs_handler(callback: CallbackQuery):
    await callback.message.answer("Тарифы и цены:", reply_markup=tariffs_kb)

@dp.callback_query(lambda c: c.data == "subscribe")
async def subscribe_handler(callback: CallbackQuery):
    await callback.message.answer("Выберите тариф для получения доступа:", reply_markup=tariffs_kb)

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
