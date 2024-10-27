from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import random
from config import CHECK_URL
import main

def create_double_button(url, text="Забрать🎁"):
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text, url)], [InlineKeyboardButton("♠️Сделать Ставку", CHECK_URL)]])

def create_url_button(url, text="Забрать🎁"):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text, url)]])

def create_mine_keyboards(num: int, id: int, amount: float, asset: str, username: str):
    markup = InlineKeyboardMarkup(5)
    mines = random.sample(range(0, 25), num)
    main.db.add_mines(id, mines, amount, asset, username)
    for i in range(25):
        markup.insert(InlineKeyboardButton('⬜️', callback_data=f"mines_{id}_{i}"))
    return markup