from app.handlers.router import router
import asyncio
import logging
import random
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram import F
from aiogram.fsm.context import FSMContext
from app.keyboards import inline as inline_keyboards
from app.states.states import Game
from app.requests.get_cat_error import get_cat_error_async as get_cat_error

MAX_ATTEMPTS = 7


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Game.Idle)
    await message.reply("Привет! 👋")
    await message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply(text="Этот бот — учебный проект 📚\n\nОн может выполнять несколько интересных функций, связанных с отдыхом и продуктивностью.\n\nЕсли остались вопросы, пиши ему: @dianabol_metandienon_enjoyer", reply_markup=inline_keyboards.home)

@router.message(Command("contacts"))
async def cmd_contacts(message: Message):
    text = "Связь с разрабом: 📞\n\n\\@dianabol\\_metandienon\\_enjoyer 🤝\n\n[GitHub](https://github.com/Segun228)"
    await message.reply(text=text, reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')

@router.callback_query(F.data == "contacts")
async def contacts_callback(callback:CallbackQuery):
    text = "Связь с разрабом: 📞\n\n\\@dianabol\\_metandienon\\_enjoyer 🤝\n\n[GitHub](https://github.com/Segun228)"
    await callback.message.edit_text(text=text, reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')
    await callback.answer()

@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback:CallbackQuery):
    await callback.message.edit_text("Я много что умею 👇", reply_markup=inline_keyboards.main)
    await callback.answer()

@router.callback_query(F.data == "start_game_menu")
async def game_start_menu_callback(callback:CallbackQuery):
    await callback.message.edit_text(f"Я загадаю число от 1 до 100 🔢. У тебя будет {MAX_ATTEMPTS} попыток угадать его! Готов? 🤔", reply_markup=inline_keyboards.ready)
    await callback.answer()

@router.callback_query(F.data == "start_game")
async def start_game_handler(callback:CallbackQuery, state: FSMContext):
    await state.set_state(Game.Playing)
    await state.update_data(attempts=0, number=random.randint(1, 100))
    await callback.message.edit_text("Я загадал число! 🎲 Угадывай!")
    await callback.answer()

@router.message(Game.Playing)
async def game_playing_func(message: Message, state: FSMContext):
    data = await state.get_data()
    current_attempts = data.get("attempts")
    number = data.get("number")

    if current_attempts is None or number is None:
        await state.set_state(Game.Idle)
        await message.answer("Извини, я забыл, какое число загадал 😔. Начни игру заново.", reply_markup=inline_keyboards.finish)
        return

    if current_attempts >= MAX_ATTEMPTS:
        await state.clear()
        await state.set_state(Game.Idle)
        await message.answer(f"Ты проиграл!!! 😢 Мое число было {number}.")
        return

    user_guess_text = message.text
    if not user_guess_text or not user_guess_text.isdigit():
        await message.answer("Неверный формат числа. Ты знаешь что такое цифра? 🤨")
        return

    user_guess = int(user_guess_text)
    await state.update_data(attempts=current_attempts + 1)

    if user_guess == number:
        await state.clear()
        await state.set_state(Game.Idle)
        await message.answer(f"Вот черт!!! 🎉 Ты угадал! Мое число было {number}!", reply_markup=inline_keyboards.finish)
    elif user_guess > number:
        await message.answer("Мое число меньше 👇")
    elif user_guess < number:
        await message.answer("Мое число больше 👆")

@router.message()
async def all_other_messages(message: Message):
    await message.answer("Неизвестная команда 🧐")
    photo_data = await get_cat_error()
    if photo_data:
        photo_to_send = BufferedInputFile(photo_data, filename="cat_error.jpg")
        await message.bot.send_photo(chat_id=message.chat.id, photo=photo_to_send)