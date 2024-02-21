from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, bot
from utils.db_api import quick_commands as commands
from filters import IsUser, IsAdmin


@dp.message_handler(IsUser(), text='Кредистория')
async def credit_history(message: Message):
    photo = open('media/og.jpg', 'rb')
    await message.answer_photo(photo=photo, caption='''Кредистория 
https://my.saleads.pro/s/6zJn8''')


@dp.callback_query_handler(lambda c: c.data == 'CreditHistory')
async def process_catalog(query: CallbackQuery):
    photo = open('media/og.jpg', 'rb')
    
    await commands.add_view('CreditHistory', str(query.from_user.id), 'telegram')

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Кредистория', url='https://my.saleads.pro/s/6zJn8'))
    markup.add(InlineKeyboardButton(text='Назад', callback_data='country'))

    await bot.send_photo(photo=photo, caption='''Кредитная история''', chat_id=query.message.chat.id, 
    reply_markup=markup)