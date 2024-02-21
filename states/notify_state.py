from aiogram.dispatcher.filters.state import StatesGroup, State

class NotifyState(StatesGroup):
    text = State()