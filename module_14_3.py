from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard = True)
button = KeyboardButton(text = 'Рассчитать')
button2 = KeyboardButton(text = 'Информация')
button3 = KeyboardButton(text = 'Купить')
kb.row(button, button2, button3)

ikb = InlineKeyboardMarkup()
inbutton = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data='calories')
inbutton2 = InlineKeyboardButton(text = 'Формулы расчёта', callback_data='formulas')
ikb.add(inbutton, inbutton2)

ikb2 = InlineKeyboardMarkup()
inbutton3 = InlineKeyboardButton(text = '1. Поливитамины', callback_data = "product_buying")
inbutton4 = InlineKeyboardButton(text = '2. Витамин С', callback_data = "product_buying")
inbutton5 = InlineKeyboardButton(text = '3. Витамин А', callback_data = "product_buying")
inbutton6 = InlineKeyboardButton(text = '4. Витамин D', callback_data = "product_buying")
ikb2.add(inbutton3, inbutton4, inbutton5, inbutton6)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start_massage(massage):
    await massage.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = ikb)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    await message.answer(f'Название: Поливитамины | Описание: описание 1 | Цена: {1 * 100}')
    with open('1.jpg', 'rb') as img:
        await message.answer_photo(img)
    await message.answer(f'Название: Витамин С | Описание: описание 2 | Цена: {2 * 100}')
    with open('2.jpg', 'rb') as img:
        await message.answer_photo(img)
    await message.answer(f'Название: Витамин А | Описание: описание 3 | Цена: {3 * 100}')
    with open('3.jpg', 'rb') as img:
        await message.answer_photo(img)
    await message.answer(f'Название: Витамин D | Описание: описание 4 | Цена: {4 * 100}')
    with open('4.jpg', 'rb') as img:
        await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup = ikb2)

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('Для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                              ' Для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.callback_query_handler(text = 'product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.message_handler(text = 'Информация')
async def inform_massages(message):
    await message.answer('Бот, рассчитывающий норму ккал по упрощенной формуле Миффлина-Сан Жеора.')

@dp.message_handler(state=UserState.age)
async def set_growth(massage, state):
    await state.update_data(age=massage.text)
    await massage.answer(f' Введите свой рост')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(massage, state):
    await state.update_data(growth=massage.text)
    await massage.answer(f' Введите свой вес')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(massage, state):
    await state.update_data(weight=massage.text)
    data = await state.get_data()

    men = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    women = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161

    await massage.answer(f' Ваша норма калорий в сутки: 1) Для женщин: {women} ккал, 2) Для мужчин: {men}')
    await UserState.weight.set()
    await state.finish()

@dp.message_handler()
async def all_massages(massage):
    await massage.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)