from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload
from aiogram import types
import bot.utils.text
from bot import keyboards
from bot.utils import text
from bot.utils.cryptopay import crypto
import main
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from main import dp, db
from bot.utils import text

async def cmd_start(message: Message):
    """Обработчик команды start"""
    if not main.db.users_exists(message.from_user.id):
        main.db.add_user(message.from_user.id)
    main.db.set_active(message.from_user.id)
    args = message.get_args() #получаем некие args с сообщения
    if args is not None and args != "": #проверяем есть ли они ваще
        id = decode_payload(args) #расшифровываем айди
        if int(id) == message.from_user.id: #сравниваем 
            if main.db.have_check(message.from_user.id):
                check_id = main.db.get_check_id(message.from_user.id)
                check = await crypto.get_checks(check_ids=check_id)
                await message.answer("Получите ваши средства", reply_markup=keyboards.functional.create_url_button(check.bot_check_url))
                main.db.remove_check(check_id)
            else:
                await message.answer('У вас нет выигрышных чеков')
        else:
            await message.answer("Это не для вас")
    else:
        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buton = KeyboardButton(text='🎲Играть')
        bton = KeyboardButton(text='👤Профиль')
        murkup.add(buton)
        murkup.add(bton)
        await message.answer(f'Привет👋', reply_markup=murkup)
async def text(message: Message):
    murk = types.InlineKeyboardMarkup()
    murk.add(types.InlineKeyboardButton("♠️Сделать Ставку", url='https://t.me/+_cMeCYzgF_c4ZmJi'))
    await message.answer('<b>🔥Хочешь испытать удачу?</b>\n\n<b><u>Переходи в игровой канал, чтобы сделать ставку и получить множество незабываемых эмоций!</u></b>',parse_mode='html',reply_markup=murk)

async def text1(message: Message):
    ids = message.from_user.id
    us = message.from_user.first_name
    texts = f'<b>👤Профиль</b>\n\nИмя: <b>{us}</b>\nВсего игр: <b>{main.db.get_total(ids)}</b>\nБаланс: <b>{round(main.db.get_moneyback(ids), 2)} USDT</b>'
    await message.answer(texts, parse_mode='html')


def register_handlers(dp: Dispatcher):

    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(text, text=['🎲Играть'])
    dp.register_message_handler(text1, text=['👤Профиль'])










