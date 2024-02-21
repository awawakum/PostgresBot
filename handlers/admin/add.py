from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ContentType, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData
from keyboards.default.markups import *
from states import ProductState, CategoryState
from aiogram.types.chat import ChatActions
from handlers.user.menu import settings
from loader import dp, bot
from filters import IsAdmin
from hashlib import md5
from utils.db_api import quick_commands as commands


category_cb = CallbackData('category', 'id', 'action')
product_cb = CallbackData('product', 'id', 'action')

add_product = '➕ Добавить сервис'
delete_category = '🗑️ Удалить страну'


@dp.message_handler(IsAdmin(), text=settings)
async def process_settings(message: Message):

    markup = InlineKeyboardMarkup()

    categories = await commands.select_all_categories()

    print(categories)

    if categories:
        for category in categories:
            markup.add(InlineKeyboardButton(
                category.category_title, callback_data=category_cb.new(id=category.category_id, action='view')))

    markup.add(InlineKeyboardButton(
        '+ Добавить страну', callback_data='add_category'))

    await message.answer('Настройка стран:', reply_markup=markup)


@dp.callback_query_handler(IsAdmin(), category_cb.filter(action='view'))
async def category_callback_handler(query: CallbackQuery, callback_data: dict, state: FSMContext):

    category_idx = callback_data['id']

    #products = db.fetchall('''SELECT * FROM products product
    #WHERE product.tag = (SELECT title FROM categories WHERE idx=?)''',
    #                       (category_idx,))

    products = await commands.select_where_product_tag(category_idx)

    await query.message.delete()
    await query.answer('Все добавленные страны в эту категорию.')
    await state.update_data(category_index=category_idx)
    await show_products(query.message, products, category_idx)


# category


@dp.callback_query_handler(IsAdmin(), text='add_category')
async def add_category_callback_handler(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer('Название страны?')
    await CategoryState.title.set()


@dp.message_handler(IsAdmin(), state=CategoryState.title)
async def set_category_title_handler(message: Message, state: FSMContext):

    category = message.text
    idx = md5(category.encode('utf-8')).hexdigest()

    category = await commands.add_category(idx, category)
    #db.query('INSERT INTO categories VALUES (?, ?)', (idx, category))

    await state.finish()
    await process_settings(message)


@dp.message_handler(IsAdmin(), text=delete_category)
async def delete_category_handler(message: Message, state: FSMContext):

    async with state.proxy() as data:

        if 'category_index' in data.keys():

            idx = data['category_index']

            #db.query(
            #    'DELETE FROM products WHERE tag IN (SELECT title FROM categories WHERE idx=?)', (idx,))
            #db.query('DELETE FROM categories WHERE idx=?', (idx,))

            await commands.delete_product_in_category(idx)
            
            await commands.delete_category(idx)

            await message.answer('Готово!', reply_markup=ReplyKeyboardRemove())
            await process_settings(message)


# add product


@dp.message_handler(IsAdmin(), text=add_product)
async def process_add_product(message: Message):

    await ProductState.title.set()

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(cancel_message)

    await message.answer('Название?', reply_markup=markup)


@dp.message_handler(IsAdmin(), text=cancel_message, state=ProductState.title)
async def process_cancel(message: Message, state: FSMContext):

    await message.answer('Ок, отменено!', reply_markup=ReplyKeyboardRemove())
    await state.finish()

    await process_settings(message)


@dp.message_handler(IsAdmin(), text=back_message, state=ProductState.title)
async def process_title_back(message: Message, state: FSMContext):
    await process_add_product(message)


@dp.message_handler(IsAdmin(), state=ProductState.title)
async def process_title(message: Message, state: FSMContext):

    async with state.proxy() as data:
        data['title'] = message.text

    await ProductState.next()
    await message.answer('Ссылка?', reply_markup=back_markup())


@dp.message_handler(IsAdmin(), text=back_message, state=ProductState.body)
async def process_body_back(message: Message, state: FSMContext):

    await ProductState.title.set()

    async with state.proxy() as data:

        await message.answer(f"Изменить название с <b>{data['title']}</b>?", reply_markup=back_markup())


@dp.message_handler(IsAdmin(), state=ProductState.body)
async def process_body(message: Message, state: FSMContext):

    async with state.proxy() as data:
        data['body'] = message.text

    await ProductState.next()
    await message.answer('Фото?', reply_markup=back_markup())


@dp.message_handler(IsAdmin(), content_types=ContentType.PHOTO, state=ProductState.image)
async def process_image_photo(message: Message, state: FSMContext):

    fileID = message.photo[-1].file_id
    file_info = await bot.get_file(fileID)
    downloaded_file = (await bot.download_file(file_info.file_path)).read()

    async with state.proxy() as data:
        data['image'] = downloaded_file

    await ProductState.confirm.set()
    await message.answer('Всё верно?', reply_markup=submit_markup())


@dp.message_handler(IsAdmin(), content_types=ContentType.TEXT, state=ProductState.image)
async def process_image_url(message: Message, state: FSMContext):

    if message.text == back_message:

        await ProductState.body.set()

        async with state.proxy() as data:

            await message.answer(f"Изменить url с <b>{data['body']}</b>?", reply_markup=back_markup())

    else:

        await message.answer('Вам нужно прислать фото товара.')


@dp.message_handler(IsAdmin(), text=cancel_message, state=ProductState.confirm)
async def process_cancel(message: Message, state: FSMContext):

    await message.answer('Ок, отменено!', reply_markup=ReplyKeyboardRemove())
    await state.finish()

    await process_settings(message)


@dp.message_handler(IsAdmin(), lambda message: message.text not in [cancel_message, all_right_message], state=ProductState.confirm)
async def process_confirm_invalid(message: Message, state: FSMContext):
    await message.answer('Такого варианта не было.')


@dp.message_handler(IsAdmin(), text=all_right_message, state=ProductState.confirm)
async def process_confirm(message: Message, state: FSMContext):

    async with state.proxy() as data:

        title = data['title']
        body = data['body']
        image = data['image']

        #tag = db.fetchone(
        #    'SELECT title FROM categories WHERE idx=?', (data['category_index'],))[0]
        
        tag = await commands.select_category(data['category_index'])
        
        idx = md5(' '.join([title, body, tag.category_title]
                           ).encode('utf-8')).hexdigest()

        await commands.add_product(idx, title, body, image, tag.category_title)

        #db.query('INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?)',
        #         (idx, title, body, image, price, cnt, tag))

    await state.finish()
    await message.answer('Готово!', reply_markup=ReplyKeyboardRemove())
    await process_settings(message)


# delete product


@dp.callback_query_handler(IsAdmin(), product_cb.filter(action='delete'))
async def delete_product_callback_handler(query: CallbackQuery, callback_data: dict):

    product_idx = callback_data['id']
    #db.query('DELETE FROM products WHERE idx=?', (product_idx,))
    await commands.delete_product(product_idx)
    await query.answer('Удалено!')
    await query.message.delete()


async def show_products(m, products, category_idx):

    await bot.send_chat_action(m.chat.id, ChatActions.TYPING) 
    
    for product in products:

        markup = InlineKeyboardMarkup()

        text = f'<b>{product.product_title}</b>\n\n{product.product_body}\n\n'

        markup.add(InlineKeyboardButton(
            '🗑️ Удалить', callback_data=product_cb.new(id=category_idx, action='delete')))

        await m.answer_photo(photo=product.product_photo,
                            caption=text,
                            reply_markup=markup)

    markup = ReplyKeyboardMarkup()
    markup.add(add_product)
    
    markup.add(delete_category)

    await m.answer('Хотите что-нибудь добавить или удалить?\nВ начало - /start', reply_markup=markup)
