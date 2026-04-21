import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
ACCESS_LINK = os.getenv("ACCESS_LINK")  # ссылка на личку Telegram

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ======= Клавиатура выбора языка =======
lang_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 RU", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇬🇧 ENG", callback_data="lang_en")
        ]
    ]
)

# ======= Главное меню =======
def main_menu(lang="ru") -> InlineKeyboardMarkup:
    if lang == "ru":
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💰 Тарифы", callback_data="tariffs")],
                [InlineKeyboardButton(text="📩 Оформить подписку", callback_data="subscribe")],
                [InlineKeyboardButton(text="🆘 Поддержка", callback_data="support")]
            ]
        )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💰 Tariffs", callback_data="tariffs")],
                [InlineKeyboardButton(text="📩 Subscribe", callback_data="subscribe")],
                [InlineKeyboardButton(text="🆘 Support", callback_data="support")]
            ]
        )

# ======= Тарифы с оформлением =======
tariffs_text = {
    "ru": """
💎 **Тариф BRONZE**  
📅 Подписка на мой приватный канал на 1 месяц.

💬 **Тариф SILVER**  
Личное общение со мной: разговоры о жизни и других темах (формат и длительность по договорённости).

💎💬 **Тариф GOLD**  
📅 Подписка на приватный канал на 1 месяц + личное общение со мной.
""",
    "eng": """
💎 **Plan BRONZE**  
📅 Subscription to my private channel for 1 month.

💬 **Plan SILVER**  
Personal communication with me: talks about life and other topics (format and duration by agreement).

💎💬 **Plan GOLD**  
📅 Subscription to private channel for 1 month + personal communication with me.
"""
}

# ======= Кнопка подписки (одна кнопка) =======
def get_subscribe_kb(lang="ru") -> InlineKeyboardMarkup:
    text = "ОФОРМИТЬ ПОДПИСКУ 💳" if lang=="ru" else "SUBSCRIBE 💳"
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, url=ACCESS_LINK)],
            [InlineKeyboardButton(text="⬅ Назад" if lang=="ru" else "⬅ Back", callback_data="main")]
        ]
    )
    return kb

# ======= Кнопка назад для тарифов =======
def get_back_kb(lang="ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅ Назад" if lang=="ru" else "⬅ Back", callback_data="main")]
        ]
    )

# ======= Хендлеры =======
@dp.message()
async def handle_start(message: types.Message):
    if message.text == "/start":
        await message.answer("Выберите язык / Choose language:", reply_markup=lang_kb)

@dp.callback_query()
async def handle_callbacks(callback: types.CallbackQuery):
    data = callback.data
    # Выбор языка
    if data in ["lang_ru", "lang_en"]:
        lang = "ru" if data == "lang_ru" else "en"
        await bot.send_message(
            callback.from_user.id,
            "Главное меню:" if lang=="ru" else "Main menu:",
            reply_markup=main_menu(lang)
        )
    # Главное меню
    elif data == "main":
        # определяем язык по тексту предыдущего сообщения
        lang = "ru" if "Главное меню" in callback.message.text else "en"
        await bot.send_message(callback.from_user.id,
                               "Главное меню:" if lang=="ru" else "Main menu:",
                               reply_markup=main_menu(lang))
    # Тарифы
    elif data == "tariffs":
        lang = "ru" if "Главное" in callback.message.text else "en"
        await bot.send_message(callback.from_user.id, tariffs_text[lang], parse_mode="Markdown",
                               reply_markup=get_back_kb(lang))
    # Подписка
    elif data == "subscribe":
        lang = "ru" if "Главное" in callback.message.text else "en"
        msg_text = "Нажмите, чтобы оформить подписку:" if lang=="ru" else "Click to subscribe:"
        await bot.send_message(callback.from_user.id, msg_text, reply_markup=get_subscribe_kb(lang))
    # Поддержка
    elif data == "support":
        lang = "ru" if "Главное" in callback.message.text else "en"
        msg_text = f"Для поддержки напишите сюда: {ACCESS_LINK}" if lang=="ru" else f"For support contact: {ACCESS_LINK}"
        await bot.send_message(callback.from_user.id, msg_text)

# ======= Запуск бота =======
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
