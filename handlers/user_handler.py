from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from aiogram import F


from loader import bot, dp, baza
from keyboards.default.user_kb import make_categories_menu, \
    make_products_menu, \
    get_plus_minus_menu, get_main_menu
from states.user_states import UserStates
from keyboards.inline.cart_menu import get_cart_menu


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Xush kelibsiz!",
        reply_markup=get_main_menu()
    )

    tg_id = message.from_user.id
    if not baza.check_user(tg_id):
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        username = message.from_user.username
        baza.add_user(tg_id, username, first_name, last_name)

@dp.message(F.text == 'Menyu')
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Kategoriyani tanlang!",
        reply_markup=make_categories_menu()
    )
    await state.set_state(UserStates.choose_category)


@dp.message(UserStates.choose_category)
async def choose_category_handler(message: Message, state: FSMContext):
    text = message.text
    result = baza.check_category(text)
    if result:
        await message.answer(
            f"{text} dan fastfoodlarni tanlang",
            reply_markup=make_products_menu(text)
        )
        await state.set_state(UserStates.choose_product)
    else:
        await message.answer("tugmalardan birini bosing!")


@dp.message(UserStates.choose_product)
async def choose_product_handler(message: Message, state: FSMContext):
    text = message.text
    result = baza.check_product(text)
    if result:
        product = baza.select_product_by_name(text)
        p_id, name, weight, ingredients, price, image, category_id = product
        mtext = f"""{name}\nvazni: {weight}\ntarkibi: {ingredients}\nnarxi: {price}"""
        file = FSInputFile(path=image)
        await message.answer_photo(photo=file, caption=mtext, reply_markup=get_plus_minus_menu())
        data = {
            'count': 1,
            'price': price,
            'p_id': p_id
        }
        user_id = message.from_user.id
        await state.update_data(
            {user_id: data}
        )
        
    else:
        await message.answer("tugmalardan birini bosing!")


@dp.callback_query(UserStates.choose_product, F.data == 'plus')
async def product_plus_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = call.from_user.id
    user_data = data.get(user_id)
    count = user_data.get('count')

    count += 1
    user_data.update({'count': count})
    await state.update_data({user_id: user_data})

    await call.message.edit_reply_markup(reply_markup=get_plus_minus_menu(count))


@dp.callback_query(UserStates.choose_product, F.data == 'add_to_cart')
async def add_to_cart_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = call.from_user.id
    user_data = data.get(user_id)
    p_id = user_data.get('p_id')
    price = user_data.get('price')
    count = user_data.get('count')
    total_price = count * price
    baza.add_to_cart(user_id, p_id, count, total_price)

    await state.clear()
    await call.answer("Savatchaga qo'shildi")
    await call.message.delete()


@dp.message(F.text == 'Savatcha')
async def savatcha_handler(message: Message):
    user_id = message.from_user.id
    menu, exists = get_cart_menu(user_id)
    if exists:
        await message.answer("Savatingizda ...", reply_markup=menu)
    else:
        await message.answer("Savatingiz hozircha bo'm bo'sh")


@dp.callback_query(F.data.startswith('cart_item_delete'))
async def cart_item_delete_handler(call: CallbackQuery):
    data = call.data.split('.')
    cart_id = int(data[-1])
    baza.delete_cart_item(cart_id)
    user_id = call.from_user.id

    menu, exists = get_cart_menu(user_id)
    if exists:
        await call.message.edit_reply_markup(reply_markup=menu)    
    else: 
        await call.message.answer("Savatingizda hech narsa qolmadi")
        await call.message.delete()


@dp.callback_query(F.data == 'clear_cart')
async def clear_cart_handler(call: CallbackQuery):
    user_id = call.from_user.id
    baza.clear_user_cart(user_id)

    await call.answer("Savatingiz tozalandi")
    await call.message.delete()
    
