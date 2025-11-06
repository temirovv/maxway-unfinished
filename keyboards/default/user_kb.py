from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, KeyboardButton
from loader import baza


def make_categories_menu():
    data = baza.select_categories()
    menu = ReplyKeyboardBuilder()
    menu.max_width = 2
    for category in data:
        menu.button(
            text=category[-1]
        )

    return menu.as_markup(resize_keyboard = True)


def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Menyu")],
            [KeyboardButton(text='Savatcha')],
            [
                KeyboardButton(text="Sozlamalar"),
                KeyboardButton(text="Buyurtmalarim")
            ]
        ],
        resize_keyboard=True
    )


def make_products_menu(category: str):
    menu = ReplyKeyboardBuilder()
    products = baza.select_products_by_category(category)
    menu.max_width = 2
    for product in products:
        menu.button(
            text=product[-1]
        )

    return menu.as_markup(resize_keyboard = True)


def get_plus_minus_menu(count: int = 1):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="-", callback_data='minus'),
                InlineKeyboardButton(text=f'{count}', callback_data='count'),
                InlineKeyboardButton(text="+", callback_data='plus'),
            ],
            [
                InlineKeyboardButton(text='Savatga qo\'shish', callback_data='add_to_cart')
            ]
        ]
    )
