import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# -------------------
# Переменные окружения
# -------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
ACCESS_LINK = os.getenv("ACCESS_LINK")  # ссылка на личку Telegram

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# -------------------
# Словарь для хранения языка пользователя
# -------------------
user_lang = {}  # user_id: "ru" / "en"

# -------------------
# Клавиатура выбора языка
# -------------------
lang_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇷🇺 RU", callback_data="lang_ru"),
     InlineKeyboardButton(text="🇬🇧 ENG", callback_data="lang_en")]
])

# -------------------
# Главное меню
# -------------------
def main_menu(lang="ru"):
    if lang == "ru":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💰 Тарифы", callback_data="tariffs")],
            [InlineKeyboardButton(text="📩 Оформить подписку", callback_data="subscribe")],
            [InlineKeyboardButton(text="🆘 Поддержка", callback_data="support")]
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💰 Tariffs", callback_data="tariffs")],
            [InlineKeyboardButton(text="📩 Subscribe", callback_data="subscribe")],
            [InlineKeyboardButton(text="🆘 Support", callback_data="support")]
        ])

# -------------------
# Тарифы с оформлением
# -------------------
tariffs_text = {
    "ru": """
💎 **Тариф BRONZE**  
📅 Подписка на мой приватный канал на 1 месяц.

💬 **Тариф SILVER**  
Личное общение со мной: разговоры о жизни и других темах (формат и длительность по договорённости).

💎💬 **Тариф GOLD**  
📅 Подписка на приватный канал на 1 месяц + личное общение со мной.
""",
    "en": """
💎 **Plan BRONZE**  
📅 Subscription to my private channel for 1 month.

💬 **Plan SILVER**  
Personal communication with me: talks about life and other topics (format and duration by agreement).

💎💬 **Plan GOLD**  
📅 Subscription to private channel for 1 month + personal communication with me.
"""
}

# -------------------
# Кнопка подписки
# -------------------
def subscribe_kb(lang="ru"):
    text = "ОФОРМИТЬ ПОДПИСКУ 💳" if lang=="ru" else "SUBSCRIBE 💳"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, url=ACCESS_LINK)],
        [InlineKeyboardButton(text="⬅ Назад" if lang=="ru" else "⬅ Back", callback_data="main")]
    ])

# -------------------
# Кнопка назад для тарифов
# -------------------
def back_kb(lang="ru"):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅ Назад" if lang=="ru" else "⬅ Back", callback_data="main")]
    ])

# -------------------
# Хендлеры
# -------------------
@dp.message()
async def handle_start(message: types.Message):
    if message.text == "/start":
        await message.answer("Выберите язык / Choose language:", reply_markup=lang_kb)

@dp.callback_query()
async def handle_callbacks(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data

    # Выбор языка
    if data in ["lang_ru", "lang_en"]:
        lang = "ru" if data=="lang_ru" else "en"
        user_lang[user_id] = lang
        await callback.message.edit_text("Главное меню:" if lang=="ru" else "Main menu:",
                                         reply_markup=main_menu(lang))
        return

    # Получаем язык пользователя, по умолчанию русский
    lang = user_lang.get(user_id, "ru")

    # Главное меню
    if data == "main":
        await callback.message.edit_text("Главное меню:" if lang=="ru" else "Main menu:",
                                         reply_markup=main_menu(lang))
        return

    # Тарифы
    if data == "tariffs":
        await callback.message.edit_text(tariffs_text[lang], parse_mode="Markdown",
                                         reply_markup=back_kb(lang))
        return

    # Подписка
    if data == "subscribe":
        msg_text = "Нажмите, чтобы оформить подписку:" if lang=="ru" else "Click to subscribe:"
        await callback.message.edit_text(msg_text, reply_markup=subscribe_kb(lang))
        return

    # Поддержка
    if data == "support":
        msg_text = f"Для поддержки напишите сюда: {ACCESS_LINK}" if lang=="ru" else f"For support contact: {ACCESS_LINK}"
        await callback.message.edit_text(msg_text, reply_markup=back_kb(lang))
        return

# -------------------
# Запуск бота
# -------------------
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
