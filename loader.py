from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from database.db_api import Database


TOKEN = "7596603800:AAHzVxeSJc4U_sl32K4ECh91z1l48HCY5bc"
ADMIN = 1058730773
dp = Dispatcher()
baza = Database('database/main.db')
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


