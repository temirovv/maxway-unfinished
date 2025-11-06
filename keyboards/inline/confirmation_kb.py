from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_confirmation_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Yes", callback_data='yes'),
                InlineKeyboardButton(text='No', callback_data='no')
            ]
        ]
    )
