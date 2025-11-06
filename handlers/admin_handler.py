from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext
from states.admin_states import CategoryCreateState, CategoryDeleteState

from keyboards.inline.confirmation_kb import get_confirmation_kb
from keyboards.inline.category_deletion_kb import get_categories_menu
from loader import dp, ADMIN, baza
from states.admin_states import SendAdStates


@dp.message(F.text == "/add_category", F.from_user.id.in_([ADMIN]))
async def add_category(message: Message, state: FSMContext):
    await message.answer("category nomini kiriting:\nM-n: 🌯Lavash")
    await state.set_state(CategoryCreateState.name)


@dp.message(CategoryCreateState.name, F.from_user.id.in_([ADMIN]))
async def get_category_name_handler(message: Message, state: FSMContext):
    name = message.text
    await state.set_data({'name': name})
    await message.answer(f"name: {name}\nBazaga saqlaymi?", reply_markup=get_confirmation_kb())
    await state.set_state(CategoryCreateState.confirm)


@dp.callback_query(CategoryCreateState.confirm, F.data == 'no',  F.from_user.id.in_([ADMIN]))
async def denying_category_handler(call: CallbackQuery, state: FSMContext):
    await call.answer("Operation denied!")
    await call.message.delete()
    await state.clear()


@dp.callback_query(CategoryCreateState.confirm, F.data == 'yes',  F.from_user.id.in_([ADMIN]))
async def applying_category_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get('name')
    if name:
        baza.add_category(name)
        await call.answer("Category added successfully!")
    else:
        await call.answer("Something went wrong!")
    
    await call.message.delete()
    await state.clear()


# DELETE CATEGORIES
@dp.message(F.text == '/delete_category')
async def delete_category_command_handler(message: Message, state: FSMContext):
    await message.answer(
        "O'chirmoqchi bo'lgan kategoriyangizni tanglang!",
        reply_markup=get_categories_menu()
    )
    await state.set_state(CategoryDeleteState.deleting_category)


async def cancel_handler(call: CallbackQuery, state: FSMContext, *args, **kwargs):
    data = call.data
    if data == 'cancel':
        await call.message.delete()
        await state.clear()
        return 'ok'
    return


@dp.callback_query(CategoryDeleteState.deleting_category)
async def deleting_category_handler(call: CallbackQuery, state: FSMContext):
    if await cancel_handler(call, state):
        return


    category_id = call.data
    await state.update_data({"category_id": category_id})
    name = baza.select_category_by_id(int(category_id))
    name = name[0]
    await call.message.answer(
        f"{name} ni o'chirmoqchimisiz?", 
        reply_markup=get_confirmation_kb()
    )
    await call.message.delete()
    await state.set_state(CategoryDeleteState.confirm_deletion)


@dp.callback_query(CategoryDeleteState.confirm_deletion, F.data == 'no')
async def cancelling_deletion_handler(call: CallbackQuery, state: FSMContext):
    await call.answer("Operation cancelled")
    await call.message.delete()
    await state.clear()


@dp.callback_query(CategoryDeleteState.confirm_deletion, F.data == 'yes')
async def cancelling_deletion_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category_id = data.get('category_id')
    baza.delete_category(int(category_id))
    await call.answer("Category has been deleted successfully")
    await call.message.delete()
    await state.clear()


@dp.message(F.text == '/send_ad', F.from_user.id.in_([ADMIN]))
async def send_ad_handler(message: Message, state: FSMContext):
    await message.answer('Reklama xabaringizni yuboring')
    await state.set_state(SendAdStates.send_ad)


@dp.message(F.from_user.id.in_([ADMIN]), SendAdStates.send_ad)
async def getting_ad_handler(message: Message, state: FSMContext):
    pass
