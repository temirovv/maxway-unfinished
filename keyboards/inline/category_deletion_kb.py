from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import baza


def get_categories_menu():
    data = baza.select_categories()    
    menu = InlineKeyboardBuilder()
    menu.max_width = 2
    for category in data:
        menu.button(
            text=category[-1],
            callback_data=str(category[0])
        )
    menu.button(
        text="cancel",
        callback_data='cancel'
    )
    return menu.as_markup()