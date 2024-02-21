from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils.db_api import quick_commands as commands

category_cb = CallbackData('category', 'id', 'action')


async def categories_markup():

    global category_cb
    
    markup = InlineKeyboardMarkup()
    for category in await commands.select_all_categories():
        markup.add(InlineKeyboardButton(category.category_title, callback_data=category_cb.new(id=category.category_id, action='view')))

    markup.add(InlineKeyboardButton(text='Назад', callback_data='start'))
    return markup


res_cb = CallbackData('res', 'id', 'action')


async def res_markup(products):
    global res_cb

    markup = InlineKeyboardMarkup()
    
    buttons = []

    product_count = await commands.count_products()

    if product_count == 0:
        pass
    elif product_count > 0:
        for product in products:
            button = InlineKeyboardButton(product.product_title, callback_data=res_cb.new(id=product.product_id, action='view'))
            buttons.append(button)

    for i in range(0, len(buttons), 3): 
        if i + 2 < len(buttons):
            markup.add(buttons[i], buttons[i+1], buttons[i+2])
        elif i + 1 < len(buttons):
            markup.add(buttons[i], buttons[i+1])
        elif i < len(buttons):
            markup.add(buttons[i])

    markup.add(InlineKeyboardButton(text='Назад', callback_data='Loans'))

    return markup


async def link_markup(name: str, link: str, user_id:str):
    global res_cb
    
    await commands.add_view(link, user_id, 'telegram')

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=name, url=link))
    markup.add(InlineKeyboardButton(text='Назад', callback_data='country'))
    
    return markup


def menu_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Займы', callback_data='Loans'))
    markup.add(InlineKeyboardButton(text='Кредистория', callback_data='CreditHistory'), InlineKeyboardButton(text='Банкротство', callback_data='Bankruptcy'))
    markup.add(InlineKeyboardButton(text='Осаго', callback_data='OSAGO'))

    return markup