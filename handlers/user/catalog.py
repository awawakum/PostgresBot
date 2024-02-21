import imghdr
import logging
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.categories import categories_markup, category_cb, res_markup, res_cb, link_markup
from keyboards.inline.products_from_catalog import product_cb, product_markup
from aiogram.utils.callback_data import CallbackData
from aiogram.types.chat import ChatActions
from aiogram.types.input_media import InputMedia
from loader import dp, bot
from .menu import loans
from filters import IsUser, IsAdmin
import json
import base64
from utils.db_api import quick_commands as commands

@dp.message_handler(IsUser(), text=loans)
async def process_catalog(message: Message):
    await message.answer('Выберите страну:',
                         reply_markup=await categories_markup())

@dp.callback_query_handler(lambda c: c.data == 'country')
async def process_catalog(query: CallbackQuery):
    await bot.delete_message(message_id=query.message.message_id, chat_id=query.message.chat.id)

@dp.callback_query_handler(lambda c: c.data == 'Loans')
async def process_catalog(query: CallbackQuery):
    await bot.edit_message_text(text='Выберите страну:', chat_id=query.message.chat.id, message_id=query.message.message_id,
                           reply_markup=await categories_markup())

@dp.callback_query_handler(IsUser(), category_cb.filter(action='view'))
async def category_callback_handler(query: CallbackQuery, callback_data: dict):

    products = await commands.select_where_product_tag(callback_data['id'])

    #products = db.fetchall('''SELECT * FROM products product
    #WHERE product.tag = (SELECT title FROM categories WHERE idx=?)''',
    #                       [callback_data['id']])

    await query.answer('Все доступные ресурсы.')
    await get_res_buttons(query.message, products)


async def get_res_buttons(m, products):

    if await commands.count_products() == 0:
        await m.answer('Здесь ничего нет 😢')
        await process_catalog(m)

    else:

        await bot.send_chat_action(m.chat.id, ChatActions.TYPING)
        await bot.edit_message_text(message_id=m.message_id, chat_id=m.chat.id, text='Доступные ресурсы: ')
        r_markup = await res_markup(products)
        await bot.edit_message_reply_markup(message_id=m.message_id, chat_id=m.chat.id, reply_markup=r_markup)


@dp.callback_query_handler(IsUser(), res_cb.filter(action='view'))
async def res_callback_handler(query: CallbackQuery, callback_data: dict):
    resources = await commands.select_product(callback_data['id'])

    await commands.add_view(str(callback_data['id']), str(query.from_user.id), 'telegram')
    
    l_markup = await link_markup(resources.product_title, resources.product_body, str(query.from_user.id))

    #resources = db.fetchall('''SELECT * FROM products WHERE idx =?''', (callback_data['id'], ))
    await bot.send_photo(chat_id=query.message.chat.id, photo=resources.product_photo, caption=str(resources.product_title), reply_markup=l_markup)