import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

# Получаем токен бота и ссылку на личку из переменных окружения Railway
API_TOKEN = os.environ.get("BOT_TOKEN")
ACCESS_LINK = os.environ.get("ACCESS_LINK")  # ссылка на личку для общения

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# -----------------------------
# Описание тарифов
# -----------------------------
PLAN_DESCRIPTIONS = {
    "bronze": "Тариф BRONZE\n\nПодписка на мой приватный канал на 1 месяц.",
    "silver": "Тариф SILVER\n\nЛичное общение со мной: разговоры о жизни и других темах (формат и длительность по договорённости).",
    "gold": "Тариф GOLD\n\nПодписка на приватный канал на 1 месяц + личное общение со мной (всё из тарифов BRONZE и SILVER)."
}

# -----------------------------
# Главное меню
# -----------------------------
def main_menu(lang="RU"):
    if lang == "RU":
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("📊 Тарифы")],
                [KeyboardButton("🛠 Поддержка")]
            ],
            resize_keyboard=True
        )
    else:
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("📊 Tariffs")],
                [KeyboardButton("🛠 Support")]
            ],
            resize_keyboard=True
        )
    return kb

# -----------------------------
# Старт
# -----------------------------
@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton("🇷🇺 RU"), KeyboardButton("🇬🇧 ENG")]],
        resize_keyboard=True
    )
    await message.answer("Выберите язык / Choose language:", reply_markup=kb)
    message.from_user.language = "RU"

# -----------------------------
# Выбор языка
# -----------------------------
@dp.message(F.text.in_({"🇷🇺 RU", "🇬🇧 ENG"}))
async def select_language(message: types.Message):
    lang = "RU" if "RU" in message.text else "ENG"
    await message.answer("Главное меню:" if lang == "RU" else "Main Menu:", reply_markup=main_menu(lang))
    message.from_user.language = lang

# -----------------------------
# Показ тарифов
# -----------------------------
@dp.message(F.text.in_({"📊 Тарифы", "📊 Tariffs"}))
async def show_tariffs(message: types.Message):
    lang = "RU" if "Тарифы" in message.text else "ENG"

    for plan in ["bronze", "silver", "gold"]:
        description = PLAN_DESCRIPTIONS[plan]
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("ПОЛУЧИТЬ ДОСТУП" if lang=="RU" else "GET ACCESS", url=ACCESS_LINK)]
        ])
        await message.answer(f"{description}", reply_markup=kb)

# -----------------------------
# Поддержка
# -----------------------------
@dp.message(F.text.in_({"🛠 Поддержка", "🛠 Support"}))
async def support(message: types.Message):
    await message.answer(
        "Связь с поддержкой: @YourSupportUsername" if "Поддержка" in message.text else "Contact support: @YourSupportUsername"
    )

# -----------------------------
# Запуск бота
# -----------------------------
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
