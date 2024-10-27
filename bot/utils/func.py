from aiogram.utils.deep_linking import decode_payload, get_start_link
from aiogram.types import Message
from aiogram import types
import main as m
import config
from bot.utils.cryptopay import get_balance, crypto
from bot.utils import text
from bot import keyboards
from settings import keywords, coefs
import base64, datetime, asyncio, main
from bot.keyboards import functional

def check_button_back(buttons) -> bool:
    for keyboard in buttons:
        for button in keyboard:
            if button.text == "Забрать":
                return False
    return True
   
def check_winning(id, buttons) -> bool:
    for keyboard in buttons:
        for button in keyboard:
            if button.callback_data != "finish" and "stop_" not in button.callback_data:
                i = int(button.callback_data.split('_')[2])
                if i not in m.db.get_bad_mines(id) and i != -1:
                    return False
    return True

def remaining_slots(buttons: list, id: int) -> int:
    i = 0
    for keyboard in buttons:
        for button in keyboard:
            if "stop_" not in button.callback_data:
                if button.callback_data != "ready_empty_-1" and int(button.callback_data.split('_')[2]) not in m.db.get_bad_mines(id):
                    i = i + 1
    return i

def contains(l, item) -> bool:
    for el in l:
        if el + " " in item:
            return True
    return False

import difflib

def similarity(s1, s2):
    if s1 == s2:
        return 1
    sim_l = []
    elemen = 0

    if type(s1) == list and type(s2) == list:
        for el in s1:
            if s2 not in keywords.EVEN and s2 not in keywords.ODD:
                for el2 in s2:
                    if " " in el:
                        el2 = s2
                    elif " " in el2:
                        el = s1

                    matcher = difflib.SequenceMatcher(None, el, el2)
                    sim = matcher.quick_ratio()
                    sim_l.append(sim)
                    elemen += 1
            else:
                for el1 in s1:
                    matcher = difflib.SequenceMatcher(None, el1, s2)
                    sim = matcher.quick_ratio()
                    sim_l.append(sim)
                    elemen += 1
        sim = max(sim_l)
    elif type(s2) == list and type(s1) == str:
        for el in s2:
            matcher = difflib.SequenceMatcher(None, s1, el)
            sim = matcher.quick_ratio()
            sim_l.append(sim)
            elemen += 1
        sim = max(sim_l)
    elif type(s1) == list and type(s2) == str:
        for el in s1:
            matcher = difflib.SequenceMatcher(None, el, s2)
            sim = matcher.quick_ratio()
            sim_l.append(sim)
            elemen += 1
        sim = max(sim_l)
    else:
        matcher = difflib.SequenceMatcher(None, s1, s2)
        sim = matcher.quick_ratio()
    return sim

def equals(l, item) -> bool:
    for el in l:
        if el==item:
            return True
    if similarity(l, item) > 0.95:
            return True
    return False

def remove_prefixes(l: list, item: str):
    for el in l:
        item = item.removeprefix(el + " ")
    return item


async def winner(message: Message, amount, asset, coef, user_id, username, a_text, photo = "win.jpg", type = 'def'):
        photo = "imgs\\" + photo
        asset = 'USDT'

        if amount*coef < dict(await get_balance())['USDT']:
            if amount*coef > 1:
                await crypto.transfer(user_id, asset, amount * coef, text.rnd_id())
                await main.bot.send_message(config.LOG_CHANNEL, f'{username}, {user_id}, выиграл {amount*coef}')
                await message.reply_photo(open(photo, 'rb'), text.get_win_text(round(amount * coef, 3), asset, type, a_text), 'html',reply_markup=keyboards.functional.create_url_button(config.CHECK_URL,"♠️Сделать Ставку"))


            else:
                check = await crypto.create_check(asset, amount * coef)
                m.db.add_check(user_id, check.check_id)
                await main.bot.send_message(config.LOG_CHANNEL, f'{username}, {user_id}, выиграл {amount * coef}')
                await message.reply_photo(open(photo, 'rb'),text.get_win_text(round(amount * coef, 3), asset, type, a_text, is_less_dol = True), 'html',
                                     reply_markup=keyboards.functional.create_url_button(await get_start_link(user_id, True), "🎁 Забрать чек"))
        else:
            await m.bot.send_message(config.LOG_CHANNEL, f"{username} ({user_id}) выиграл {round(amount * coef, 3)} {asset}. ЗАДОЛЖЕННОСТЬ!")
            boton = types.InlineKeyboardMarkup(text=f'️♠️Сделать ставку', url=config.CHECK_URL)
            kuiboard = types.InlineKeyboardMarkup()
            await message.reply_photo(open(photo, 'rb'),text.get_win_text(round(amount * coef, 3), asset, type, a_text, is_less=True), 'html', reply_markup=keyboards.functional.create_url_button(config.CHECK_URL, '♠️Сделать Ставку'))




async def invalid_syntax(message: Message, amount, asset, user_id, username, name):
    end_amount = amount - amount * 0.1
    main.db.edit_total(user_id, -1)
    main.db.edit_moneyback(user_id, -(amount*config.MONEYBACK))
    asset='USDT'
    if end_amount < dict(await get_balance())['USDT']:
        if end_amount > 1:
                await crypto.transfer(user_id, asset, end_amount, text.rnd_id())
                msg = await message.reply(text.get_invalid_text(name), 'html', disable_notification=True)
        else:
            try:
                check = await crypto.create_check(asset, end_amount)
                m.db.add_check(user_id, check.check_id)
                msg = await message.reply(text.get_invalid_text(name, 'button'), 'html', reply_markup=keyboards.functional.create_url_button(await get_start_link(user_id, True), "Вернуть💸"), disable_notification=True)
            except:
                await m.bot.send_message(config.LOG_CHANNEL, f"❗{username} ({user_id}) ошибся в синтаксесе. {round(end_amount, 3)} {asset.upper()}. ЗАДОЛЖЕННОСТЬ!")
                msg = await message.reply(text.get_invalid_text(name, 'admin'), 'html', disable_notification=True)
    else:
        await m.bot.send_message(config.LOG_CHANNEL, f"❗{username} ({user_id}) ошибся в синтаксесе. {round(end_amount, 3)} {asset.upper()}. ЗАДОЛЖЕННОСТЬ!")
        msg = await message.reply(text.get_invalid_text(name, 'admin'), 'html', disable_notification=True)