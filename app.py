import asyncio
import logging
import sys

from loader import dp, bot, baza
from handlers import admin_handler
from handlers import admin_add_product_handler
from handlers import user_handler


async def main() -> None:
    await dp.start_polling(bot)

print('qarama')
def init_tables():
    baza.create_category_table()
    baza.create_products_table()
    baza.create_cart_table()
    baza.create_user_table()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    init_tables()
    asyncio.run(main())
