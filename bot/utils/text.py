from bot.utils import cryptopay

import string, random, main
from settings import coefs

links = """ """
async def get_admin_menu_text():
    return f"""Админское меню:
CryptoBot
USDT 
Доступно: {round(dict(await cryptopay.get_balance())['USDT'], 3)}
В ожидании: {round(dict(await cryptopay.get_hold())['USDT'], 3)}
TON
Доступно: {round(dict(await cryptopay.get_balance())['TON'], 3)}
В ожидании: {round(dict(await cryptopay.get_hold())['TON'], 3)}
    """

def get_admin_given(amount, asset):
    return f"""<blockquote>🚀Выш выигрыш будет зачислена администрацией вручную!\n🔥Желаем удачи в следующих ставках!</blockquote>
"""

def get_button_given(amount, asset):
    return f"""<blockquote>🚀Заберите выигрыш по кнопке ниже!\n🔥Желаем удачи в следующих ставках!</blockquote>
"""

def get_transfer_given(amount, asset):
    return f"""<blockquote>🚀Выигрыш был успешно зачислен на кошелек победителя!\n🔥Желаем удачи в следующих ставках!</blockquote>
"""

def rnd_id():
    al = string.ascii_letters
    txt = ""
    for i in range(1, 10):
        txt += random.choice(al)
    return txt

def get_stake(amount, asset, comment, name):
    return f"""
<blockquote><b>✅Ваша ставка принята</b></blockquote>
    
🔑Имя игрока: <b>{name}</b>
💵 Сумма ставки: <b>{amount}$ </b>
💬Коментарий: <b>{comment}</b>
"""

def get_win_text(amount, asset, type, additional_comment = None, is_less_dol = False, is_less = False):
    if type != 'def':
        eth, gram, trx, btc, notcoin, ton, ltc, my, bnb, usdc, rub = coefs.update_prices()
        start = f"<b> 🎉Поздравляем, вы выигрыли {round(amount, 2)} USDT ({round(amount/rub, 2)} RUB)!</b>"
    else:
        eth, gram, trx, btc, notcoin, ton, ltc, my, bnb, usdc, rub = coefs.update_prices()
        start = f"<b> 🎉Поздравляем, вы выигрыли {round(amount, 2)} USDT ({round(amount/rub, 2)} RUB)!</b>"
    if is_less:
        return start + "\n\n" + get_admin_given(amount, asset='USDT') + f"\n\n{links}"
    
    if is_less_dol:
        return start + "\n\n" + get_button_given(amount, asset='USDT') + f"\n\n{links}"
    else:
        return start + "\n\n" + get_transfer_given(amount, asset='USDT') + f"\n\n{links}"
    


def get_invalid_text(name, type = 'default'):
    if type == 'admin': addiction = "Возврат денежных средств будет выполнен администрацией вручную."
    elif type == "button": addiction = "Заберите деньги по кнопке ниже."
    else: addiction = "Был совершён возврат денежных средств."
    return f"""<b>[❌] Ошибка!</b>

<b>{name} - Вы</b> <i>забыли дописать комментарий к оплате или ошиблись при его написании.</i>
<i><b><u>{addiction}</u></b></i>

<blockquote>Комиссия составляет: 10%.</blockquote>
"""

def get_bowling_text(v):
    if v == 6: return "боулинг страйк"
    elif v == 5: return "боулинг 1"
    elif v == 4: return "боулинг 2"
    elif v == 3: return "боулинг 3"
    elif v == 2: return "боулинг 5"
    elif v == 1: return "боулинг 6"

def get_profile(id, name):
    return f"""<b>👤 Личный кабинет</b>

<b>UN:</b> {name}
<b>ID:</b> <code>{id}</code>
<b>Всего игр</b>: {main.db.get_total(id)}
<b>Баланс:</b> {round(main.db.get_moneyback(id), 2)} USDT

<a href="https://t.me/+w14pbT7sVvVjOWY6">BindingBet</a> - лучшие в телеграм"""

