from aiogram.fsm.state import State, StatesGroup


class CategoryCreateState(StatesGroup):
    name = State()
    confirm = State()


class CategoryDeleteState(StatesGroup):
    deleting_category = State()
    confirm_deletion = State()


class AddProductsStates(StatesGroup):
    category_id = State()
    name = State()
    weight = State()
    ingredients = State()
    price = State()
    image = State()
    create_confirm = State()


class SendAdStates(StatesGroup):
    send_ad = State()
    confirm_ad = State()
