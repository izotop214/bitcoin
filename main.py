import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiohttp
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Вставьте ваш токен бота, полученный от @BotFather
API_TOKEN = '7866326387:AAGrYhD3JJ0h5a7KXOpj49tVuliteY2a1m0'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Создание клавиатуры
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Получить цену BTC")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Я бот, который показывает текущую цену биткоина (BTC). Нажми на кнопку ниже или используй команду /price.",
        reply_markup=get_main_keyboard()
    )

# Обработчик команды /price и кнопки
@dp.message(lambda message: message.text == "📊 Получить цену BTC" or message.text == "/price")
async def get_btc_price(message: types.Message):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd') as response:
                if response.status == 200:
                    data = await response.json()
                    btc_price = data['bitcoin']['usd']
                    await message.reply(f"📈 Текущая цена биткоина (BTC): ${btc_price:,.2f}", reply_markup=get_main_keyboard())
                else:
                    await message.reply("❌ Не удалось получить данные о цене. Попробуйте позже.", reply_markup=get_main_keyboard())
        except Exception as e:
            await message.reply(f"❌ Произошла ошибка: {str(e)}", reply_markup=get_main_keyboard())

# Обработчик неизвестных команд
@dp.message()
async def unknown_command(message: types.Message):
    await message.reply("❓ Неизвестная команда. Используйте /start или /price.", reply_markup=get_main_keyboard())

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


