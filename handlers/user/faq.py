from aiogram.types import Message, CallbackQuery
from loader import dp, bot

from filters import IsUser, IsAdmin


@dp.message_handler(IsUser() and IsAdmin(), text='👥 Контакты')
async def faq(message: Message):
    await message.answer('''
<b>Номер телефона:</b> 
<b>ТГ:</b> 
<b>Комната:</b> 
<b>Номер банковской карты:</b> ''')