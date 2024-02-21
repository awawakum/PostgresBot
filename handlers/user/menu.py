from aiogram.types import Message, ReplyKeyboardMarkup, CallbackQuery
from loader import dp
from filters import IsAdmin, IsUser

loans = 'Займы'
creditsHistory = 'Кредистория'
bankruptcy = 'Банкротство'
OSAGO = 'ОСАГО'
settings = '⚙️ Настройка'

@dp.message_handler(IsAdmin(), commands='menu')
async def admin_menu(message: Message):
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(settings)

    await message.answer('Меню', reply_markup=markup)

@dp.message_handler(IsUser(), commands='menu')
async def user_menu(message: Message):
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(loans)
    markup.add(creditsHistory, bankruptcy, OSAGO)

    await message.answer('Меню', reply_markup=markup)


async def get_user_menu():
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(loans)
    markup.add(creditsHistory, bankruptcy, OSAGO)

    return markup
