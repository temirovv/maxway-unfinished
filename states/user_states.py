from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    choose_category = State()
    choose_product = State()


class OrderStates(StatesGroup):
    name = State()
    phone_number = State()
    pickup_type = State()
    pickup_location = State()
    location = State()
    payment_type = State()
    detail = State()
