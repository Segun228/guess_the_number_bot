from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Угадай число 🎲", callback_data="start_game_menu")],
        [InlineKeyboardButton(text="📞 Контакты", callback_data="contacts")]
    ]
)


home = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)


ready = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Погнали! 🚀", callback_data="start_game")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)


finish = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Давай еще раз! 🎮", callback_data="start_game")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)

