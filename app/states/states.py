from aiogram.fsm.state import StatesGroup, State



class Game(StatesGroup):
    Idle = State()
    Playing = State()
    