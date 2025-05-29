# -*- coding: utf-8 -*-
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import re
import math

# Replace with your own token from @BotFather
API_TOKEN = '7936089645:AAE39dzyW3Y5oV4FzH_8m8WXQH_k7FFq56U'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Allowed functions and constants
allowed_names = {
    # Math functions
    'abs': abs,
    'acos': math.acos,
    'asin': math.asin,
    'atan': math.atan,
    'ceil': math.ceil,
    'cos': math.cos,
    'cosh': math.cosh,
    'degrees': math.degrees,
    'exp': math.exp,
    'factorial': math.factorial,
    'floor': math.floor,
    'log': math.log,
    'log10': math.log10,
    'radians': math.radians,
    'round': round,
    'sin': math.sin,
    'sinh': math.sinh,
    'sqrt': math.sqrt,
    'tan': math.tan,
    'tanh': math.tanh,

    # Constants
    'pi': math.pi,
    'e': math.e
}

def safe_eval(expression):
    """
    Safely evaluate a mathematical expression.
    Only allows specific functions and constants.
    """
    # Clean up the expression: remove all non-math characters
    expression = re.sub(r'[^0-9+\-*/().^%s]' % ''.join(allowed_names.keys()), '', expression)
    
    # Replace ^ with ** for exponentiation
    expression = expression.replace('^', '**')
    
    try:
        code = compile(expression, "<string>", "eval")
        for name in code.co_names:
            if name not in allowed_names:
                raise NameError(f"Use of {name} not allowed")
        result = eval(code, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply(
        "Welcome to the Advanced Calculator Bot!\n"
        "You can use:\n"
        "+ - * / ^\n"
        "Functions: sqrt(), sin(), cos(), tan(), etc.\n"
        "Constants: pi, e\n"
        "Example: 2 + 3 * (4 - 1), sqrt(16), sin(pi/2)"
    )

@dp.message()
async def calculate_expression(message: Message):
    expression = message.text.strip()
    if not expression:
        return

    result = safe_eval(expression)
    await message.reply(f"Result: {result}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())