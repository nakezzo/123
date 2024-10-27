
import requests

DICE = 1.8 #ЧЕТ НЕЧЕТ КУБ
DICE_MORE_LESS = 1.8#БОЛЬШЕ МЕНЬШЕ
DICE_NUMBER = 4 #ЧИСЛО
DUEL = 1.8 #ДУЭЛЬ
DARTS = 4 #ДАРТС
DARTS_COLOR = 1.8 #ДАРТС КРАСН/БЕЛ
BASKET = 1.8 #БАСКЕТ
BASKET_MISS = 1.3 #БАСКЕТ МИМО
FOOTBALL = 1.3 #ФУТБОЛ
FOOTBALL_MISS = 1.8#ФУТБОЛ МИМО
BOWLING = 4 #БОУЛИНГ
SLOTS_777 = 13 #СЛОТЫ 777
SLOTS_GRAPE = 7 #СЛОТЫ ВИНОГРАД
SLOTS_BAR = 5 #СЛОТЫ БАР
SLOTS_LEMON = 3 #СЛОТЫ ЛИМОН
KNB = 1.8 #КАМЕНЬ НОЖНИЦЫ БУМАГА
MAX_STAKE = 0.2
pl2 = 0.3
pl3 = 0.9
pl4 = 1.1
pl5 = 1.3
pl6 = 1.9
zone = 2.5
DUELN = 3.6
dice2 = 3



API_KEY = "205452:AAmoxR1pPtMwmch7ojLk0yYIN71Ah2MAKEB"
url = "https://pay.crypt.bot/api/getExchangeRates"
headers = {
    "Crypto-Pay-API-Token": API_KEY
}


def update_prices():
    eth = 0
    gram = 0
    trx = 0
    btc = 0
    notcoin = 0
    ton = 0
    ltc = 0
    my = 0
    bnb = 0
    usdc = 0
    rub = 0



    response = requests.post(url, headers=headers)
    r = response.json()

    if 'result' in r:
        exchange_rates = r['result']
        for rate in exchange_rates:
            if rate['source'] == 'ETH' and rate['target'] == 'USD':
                eth = float(rate['rate'])
            elif rate['source'] == 'GRAM' and rate['target'] == 'USD':
                gram = float(rate['rate'])
            elif rate['source'] == 'TRX' and rate['target'] == 'USD':
                trx = float(rate['rate'])
            elif rate['source'] == 'BTC' and rate['target'] == 'USD':
                btc = float(rate['rate'])
            elif rate['source'] == 'NOT' and rate['target'] == 'USD':
                notcoin = float(rate['rate'])
            elif rate['source'] == 'TON' and rate['target'] == 'USD':
                ton = float(rate['rate'])
            elif rate['source'] == 'LTC' and rate['target'] == 'USD':
                ltc = float(rate['rate'])
            elif rate['source'] == 'MY' and rate['target'] == 'USD':
                my = float(rate['rate'])
            elif rate['source'] == 'BNB' and rate['target'] == 'USD':
                bnb = float(rate['rate'])
            elif rate['source'] == 'USDC' and rate['target'] == 'USD':
                usdc = float(rate['rate'])
            elif rate['source'] == 'RUB' and rate['target'] == 'USD':
                rub = float(rate['rate'])

    return eth, gram, trx, btc, notcoin, ton, ltc, my, bnb, usdc,rub





