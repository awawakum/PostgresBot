from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, bot
from utils.db_api import quick_commands as commands

from filters import IsUser, IsAdmin


@dp.message_handler(IsUser(), text='ОСАГО')
async def OSAGO(message: Message):
    photo = open('media/osago.png', 'rb')
    await message.answer_photo(photo=photo, caption='''ОСАГО\n
Тинькофф банк https://my.saleads.pro/s/2Jiig
Страховой дом ВСК https://my.saleads.pro/s/b9qqj
Cherehapa ОСАГО https://my.saleads.pro/s/Jm882''')
    

@dp.callback_query_handler(lambda c: c.data == 'OSAGO')
async def process_catalog(query: CallbackQuery):
    photo = open('media/osago.png', 'rb')
    
    await commands.add_view('OSAGO', str(query.from_user.id), 'telegram')

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Тинькофф банк', url='https://my.saleads.pro/s/2Jiig'))
    markup.add(InlineKeyboardButton(text='Страховой дом ВСК', url='https://my.saleads.pro/s/b9qqj'))
    markup.add(InlineKeyboardButton(text='Cherehapa ОСАГО', url='https://my.saleads.pro/s/Jm882'))
    markup.add(InlineKeyboardButton(text='Назад', callback_data='country'))

    await bot.send_photo(photo=photo, caption='''ОСАГО''', chat_id=query.message.chat.id, 
    reply_markup=markup)