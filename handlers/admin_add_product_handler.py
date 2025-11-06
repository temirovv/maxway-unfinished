from pathlib import Path

from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext

from keyboards.inline.confirmation_kb import get_confirmation_kb
from keyboards.inline.category_deletion_kb import get_categories_menu
from states.admin_states import AddProductsStates
from loader import dp, ADMIN, baza, bot


@dp.message(F.text == "/add_product", F.from_user.id.in_([ADMIN]))
async def add_product_handler(message: Message, state: FSMContext):
    await message.answer(
        "Qaysi kategoriyaga FastFood qo'shmoqchisiz",
        reply_markup=get_categories_menu()
    )
    await state.set_state(AddProductsStates.category_id)


@dp.callback_query(AddProductsStates.category_id, F.from_user.id.in_([ADMIN]))
async def category_id_callback_query_handler(
    call: CallbackQuery,
    state: FSMContext):
    
    category_id = call.data
    # malumotni statega saqlash
    await state.update_data({'category_id': category_id})
    # keyingi qadam name
    await call.message.answer("FastFood nomini kiriting: ")
    # keyingi statega o'tkazish
    await state.set_state(AddProductsStates.name)
    await call.answer("Done!", cache_time=60)
    # eski xabarni o'chirish
    await call.message.delete()


@dp.message(AddProductsStates.name, F.from_user.id.in_([ADMIN]))
async def product_name_handler(message: Message, state: FSMContext):
    product_name = message.text
    # statega saqlash
    await state.update_data({"product_name": product_name})
    await message.answer("Og'irligini kiriting: (gramda)")
    await state.set_state(AddProductsStates.weight)


@dp.message(AddProductsStates.weight, F.from_user.id.in_([ADMIN]))
async def product_weight_handler(message: Message, state: FSMContext):
    weight = message.text
    # statega saqlash
    await state.update_data({'weight': weight})
    await message.answer("Ingredientlarni kiriting: m-n (Toster non, tovuq shnitseli, yangi bodring, pomidor, klab sousi, Xoxland pishloq)")
    
    # keyingi statega o'tkazamiz
    await state.set_state(AddProductsStates.ingredients)


@dp.message(AddProductsStates.ingredients, F.from_user.id.in_([ADMIN]))
async def product_ingredients_handler(message: Message, state: FSMContext):
    ingredients = message.text
    # statega saqlash
    await state.update_data({'ingredients': ingredients})
    await message.answer("Narxini kiriting")
    
    # keyingi statega o'tkazamiz
    await state.set_state(AddProductsStates.price)


@dp.message(AddProductsStates.price, F.from_user.id.in_([ADMIN]))
async def product_price_handler(message: Message, state: FSMContext):
    price = message.text
    # statega saqlash
    await state.update_data({'price': price})
    await message.answer("Rasmini yuboring!")
    
    # keyingi statega o'tkazamiz
    await state.set_state(AddProductsStates.image)


@dp.message(
        AddProductsStates.image, 
        F.from_user.id.in_([ADMIN]),
        F.content_type.in_({'photo',})
        )
async def product_name_handler(message: Message, state: FSMContext):
    base_dir = Path(__file__).resolve().parents[1]      
    upload_dir = base_dir / "downloads" / "images" 
    upload_dir.mkdir(parents=True, exist_ok=True)

    # 2) Telegram faylini olish
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)

    # 3) Faqat fayl nomini oling (masalan: "file_1.jpg")
    filename = Path(file.file_path).name
    dest_path = upload_dir / filename

    # 4) Yuklab saqlash
    await bot.download(file, destination=dest_path)

    # 5) Holatga saqlash (xohlasangiz nisbiy yo‘lni)
    await state.update_data(photo=str(dest_path.relative_to(base_dir)))
    await message.answer("✅ Rasm saqlandi.")
    await message.answer(
        "Barcha ma'lumotlar to'g'rimi",
        reply_markup=get_confirmation_kb()
    )

    await state.set_state(AddProductsStates.create_confirm)


@dp.callback_query(
        AddProductsStates.create_confirm, 
        F.from_user.id.in_([ADMIN]),
        F.data == 'no'
)
async def cancelling_confirm(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer("Operation has been cancelled!")
    await call.message.delete()


@dp.callback_query(
        AddProductsStates.create_confirm, 
        F.from_user.id.in_([ADMIN]),
        F.data == 'yes'
)
async def cancelling_confirm(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print(f"{data=}")
    category_id = data.get("category_id")
    weight = data.get("weight")
    product_name = data.get("product_name")
    ingredients = data.get("ingredients")
    price = data.get("price")
    photo = data.get("photo")
    baza.add_product(
        name=product_name,
        weight=int(weight),
        ingredients=ingredients,
        price=float(price),
        image=photo,
        category_id=int(category_id)
    )

    await call.answer("Product has been saved successfully!")
    await state.clear()
    await call.message.delete()
