from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from filters import IsAdmin
from loader import dp, bot
from states import NotifyState
from aiogram.utils.exceptions import BotBlocked
from utils.db_api import quick_commands as commands
from keyboards.inline.categories import res_markup
import asyncio
import aioschedule

@dp.message_handler(IsAdmin(), text='/notify')
async def notify_users(message: Message):
    await message.answer('Введите текст рассылки:')
    await NotifyState.text.set()


@dp.message_handler(IsAdmin() ,state=NotifyState.text)
async def notify_text(message:Message, state: FSMContext):

    users = await commands.select_all_users() #db.query('SELECT * FROM users')

    for user in users:
        try:
            await bot.send_message(user.user_id, message.text)
        except BotBlocked as e:
            await bot.send_message(message.from_user.id, 'Исключение: ', e)


    await state.finish()


async def notify_auto():

    products = await commands.select_n_products(5)

    for user in await commands.select_all_users():
        await bot.send_message(user.user_id, 'Здравствуйте, '+ user.username + '!\nУ Вас есть возможность взять займ под 0 % до 50 000 р.\n'
                               +'Мы подобрали самые надежные и проверенные компании специально для Вас !', reply_markup= await res_markup(products))


async def scheduler():
    aioschedule.every().friday.at('17:30').do(notify_auto)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)