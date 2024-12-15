from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard = True)
buttons_1 = KeyboardButton(text = 'Рассчитать')
buttons_2 = KeyboardButton(text = 'Информация')
kb.add(buttons_1)
kb.add(buttons_2)
ikb = InlineKeyboardMarkup()
buttons_3 = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data = 'calories')
buttons_4 = InlineKeyboardButton(text = 'Формула расчёта', callback_data = 'formulas')
ikb.add(buttons_3)
ikb.add(buttons_4)

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer(text = 'Выберите опцию', reply_markup= ikb)

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('Для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()
@dp.message_handler(commands= ['start'])
async def start_message(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(first = message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(second = message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(three = message.text)
    data = await state.get_data()
    calories = 10 * float(data["three"]) + 6.25 * float(data["second"]) - 5 * float(data["first"]) - 161
    await message.answer(f'Ваша норма калорий {calories}')
    await state.finish()

@dp.message_handler()
async def all_message(message):
    print("Введите команду /start, чтобы начать общение.")
    await message.answer("Введите команду /start, чтобы начать общение")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)
