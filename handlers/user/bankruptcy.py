from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, bot
from utils.db_api import quick_commands as commands
from filters import IsUser, IsAdmin


@dp.message_handler(IsUser(), text='Банкротство')
async def credit_history(message: Message):
    photo = open('media/history.jpeg', 'rb')
    await message.answer_photo(photo=photo, caption='''ВАШИ ДОЛГИ МОЖНО ЗАКОННО СПИСАТЬ. 
РАЗ И НАВСЕГДА 
🟢Поможем списать все кредиты и займы 
🟢Защитим от коллекторов 
🟢Сохраним ваше имущество 
🟢Поможем очистить кредитную историю
https://my.saleads.pro/s/kdzs0''')
    
@dp.callback_query_handler(lambda c: c.data == 'Bankruptcy')
async def process_catalog(query: CallbackQuery):
    photo = open('media/history.jpeg', 'rb')
    
    await commands.add_view('Bankruptcy', str(query.from_user.id), 'telegram')

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Банкротство', url='https://my.saleads.pro/s/kdzs0'))
    markup.add(InlineKeyboardButton(text='Назад', callback_data='country'))
    
    await bot.send_photo(photo=photo, caption='''ВАШИ ДОЛГИ МОЖНО ЗАКОННО СПИСАТЬ. 
    РАЗ И НАВСЕГДА 
    🟢Поможем списать все кредиты и займы 
    🟢Защитим от коллекторов 
    🟢Сохраним ваше имущество 
    🟢Поможем очистить кредитную историю
    ''', chat_id=query.message.chat.id, 
    reply_markup=markup)