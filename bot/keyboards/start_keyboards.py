from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

profile_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("Вывод📤", callback_data='withdraw')]])

back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("Назад↩️", callback_data="back_to_menu")]])