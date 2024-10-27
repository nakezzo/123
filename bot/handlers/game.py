import re

from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram import Dispatcher, types
from aiogram.utils.deep_linking import decode_payload, get_start_link

from settings import keywords, coefs
from settings.constants import knb
from bot.utils import func, text, game_process
from bot.utils.cryptopay import get_balance, crypto
import asyncio, config, main, random
from bot import keyboards



#ОСТОРОЖНО ВНИЗУ ГАВНОКОД ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
#Это блядский кусок кода, который я не могу перенести в отдельный файл, потому что там не работает импорт
#Я искренне ненавижу программиста, который писал этот код
#Я ненавижу его за то, что он не сделал нормальный импорт, код и так уже говно, а он ещё и импорт не сделал
#Я желаю ему поебаться в жопу, и чтобы у него были дети, которые будут писать код так же, как он
#Умри нахуй, программист, который писал этот код
#Я надеюсь, что ты умрёшь в страшных муках, и тебя будут ебать в жопу в аду каждый день те кто придумал блять правила PEP8
#Мудазвон ебаный
#Это писал не я

async def getter(msg_query: Message):
    """Пиздец"""
    if msg_query.chat.id == config.CHANNEL_BROKER: #проверка чтобы сообщение было в канале посреднике
        if msg_query.entities: #проверяем на наличие entities
            amounta = float(msg_query.text.split("отправил(а)")[1].split()[1].replace(',', "")) #получаем сумму ставки
            name = msg_query.text.split("отправил(а)")[0]
            asset = msg_query.text.removeprefix(name).split("отправил(а)")[1].split()[2]#получаем имя чела
            if msg_query.entities[0].user: #проверяем есть ли ссылка на чела
                user = msg_query.entities[0].user
                username = f"@{user.username}" if user.username else user.full_name
                name = user.full_name #снова получаем имя более надежным способом
                msg_text = msg_query.text.removeprefix(name) #удаляем имя из сообщения от греха подальше
                user_id = int(user.id)
                asset = msg_text.split("отправил(а)")[1].split()[2]

                amounta = float(msg_text.split("отправил(а)")[1].split()[1].replace(',', ""))
                eth, gram, trx, btc, notcoin, ton, ltc, my, bnb, usdc, rub = coefs.update_prices()
                if asset == 'GRAM':
                    amounta = amounta * gram
                elif asset == 'ETH':
                    amount = amounta * eth
                elif asset == 'TRX':
                    amount = amounta * trx
                elif asset == 'BTC':
                    amount = amounta * btc
                elif asset == 'NOT':
                    amount = amounta * notcoin
                elif asset == 'TON':
                    amount = amounta * ton
                elif asset == 'LTC':
                    amount = amounta * ltc
                elif asset == 'BNB':
                    amount = amounta * bnb
                elif asset == 'MY':
                    amount = amounta * my
                elif asset == 'USDC':
                    amount = amounta * usdc
                else:
                    amount = amounta

                if user_id not in main.db.get_bannned(): #провека чтобы чел не был в бане
                    if amount == 'flkgdj': #проверка на максимальную ставку
                        await main.bot.send_message(config.CHANNEL_BROKER,f"❗{username}({user_id}) отправил(а) слишком большую ставку {amount} {asset}!\n\n❌Максимальная ставка: {coefs.MAX_STAKE} {asset}!\n\n⚠️Комиссия 10% от суммы ставки!")
                        return await main.bot.send_message(config.CHANNEL_BROKER,
                                                    f"❗{name} сделал(a) слишком большую ставку {amount} USDT!\n\n❌Максимальная ставка: {coefs.MAX_STAKE} {asset}!\n\n⚠️Комиссия 10% от суммы ставки!\n\nСумма в размере {amount-amount*0.1} будет зачислена администрацией вручную")
                    if "💬 " in msg_query.text: #проверяме на наличие комента
                        coef = 0
                        old_comment = msg_query.text.split("💬 ")[1]
                        comment = old_comment.lower()
                        comment = comment.replace('ё', 'е') 
                        await asyncio.sleep(3)
                        name = name.replace("🎲", "").replace("🎯", "").replace("🏀", "").replace("⚽", "").replace("🎳","").replace("🎰", "").replace("✂️", "").replace("📄", "").replace("<", "").replace(">", "").replace(";", "")
                        boton = types.InlineKeyboardMarkup(text=f'️♠️Сделать ставку', url = config.CHECK_URL)
                        kuiboard = types.InlineKeyboardMarkup()
                        kuiboard.add(boton)
                        message = await main.bot.send_message(config.MAIN_CHANNEL, text.get_stake(amount, asset, comment, name), 'html', reply_markup=kuiboard)
                        gp = game_process.GameProcess(amount, asset, coef, user_id, username)
                        if not main.db.users_exists(user_id):
                            main.db.add_user(user_id)
                            main.db.set_active(user_id, 0)
                        main.db.edit_total(user_id, 1)
                        amount_for_moneyback = amount
                        main.db.edit_moneyback(user_id, amount_for_moneyback*config.MONEYBACK)
                        new_com = comment
                        if func.contains(keywords.DICE, comment):
                            new_com = func.remove_prefixes(keywords.DICE, comment)
                            if new_com.isdigit() and new_com != "456" and new_com != "123" and new_com != "321" and new_com != "654" and new_com != "246" and new_com != "135":
                                    coef += coefs.DICE_NUMBER
                                    n = int(new_com)
                                    if 0 < n < 7:
                                       await gp.dice_procces(message, 'number', n)
                                    else:
                                        await func.invalid_syntax(message, amount, asset, user_id, username, name)
                            elif func.equals(keywords.EVEN, new_com):
                                await gp.dice_procces(message, 'even')
                            elif func.equals(keywords.ODD, new_com):
                                await gp.dice_procces(message, 'odd')
                            elif func.equals(keywords.MORE, new_com):
                                await gp.dice_procces(message, 'more')
                            elif func.equals(keywords.LESS, new_com):
                                await gp.dice_procces(message, 'less')

                        elif func.equals(keywords.EVEN, new_com):
                            await gp.dice_procces(message, 'even')
                        elif func.equals(keywords.ODD, new_com):
                            await gp.dice_procces(message, 'odd')
                        elif func.equals(keywords.MORE, new_com):
                            await gp.dice_procces(message, 'more')
                        elif func.equals(keywords.LESS, new_com):
                            await gp.dice_procces(message, 'less')
                        elif func.equals(keywords.RED, new_com):
                            await gp.darts_procces(message, 'r')
                        elif func.equals(keywords.WHITE, new_com):
                            await gp.darts_procces(message, 'w')
                        elif func.equals(keywords.CENTER, new_com):
                            await gp.darts_procces(message)
                        elif func.equals(keywords.MISS, new_com):
                            await gp.darts_procces(message, 'miss')
                        elif func.equals(keywords.DUEL1, comment):
                            coef += coefs.DUEL
                            await gp.duel_number_process(message, 1, '🎲')
                        elif func.equals(keywords.DUEL2, comment):
                            coef += coefs.DUEL
                            await gp.duel_number_process(message, 2, '🎲')
                        elif func.equals(keywords.GOAL, new_com):
                            await gp.basketball_process(message)
                        elif func.equals(keywords.MISS, new_com):
                            await gp.basketball_process(message, 'miss')
                        elif func.equals(keywords.GOAL, new_com):
                            await gp.footaball_process(message)
                        elif func.equals(keywords.MISS, new_com):
                            await gp.footaball_process(message, 'miss')

                        elif func.contains(keywords.DARTS, comment):
                            new_com = func.remove_prefixes(keywords.DARTS, comment)
                            if func.equals(keywords.RED, new_com):
                                await gp.darts_procces(message, 'r')
                            elif func.equals(keywords.WHITE, new_com):
                                await gp.darts_procces(message, 'w')
                            elif func.equals(keywords.CENTER, new_com):
                                await gp.darts_procces(message)
                            elif func.equals(keywords.MISS, new_com):
                                await gp.darts_procces(message, 'miss')
                            else:
                                await func.invalid_syntax(message, amount, asset, user_id, username, name)
                        elif func.contains(keywords.BASKET, comment):
                                new_com = func.remove_prefixes(keywords.BASKET, comment)
                                if func.equals(keywords.GOAL, new_com):
                                    await gp.basketball_process(message)
                                elif func.equals(keywords.MISS, new_com):
                                    await gp.basketball_process(message, 'miss')
                                else:
                                    await func.invalid_syntax(message, amount, asset, user_id, username, name)
                        elif func.contains(keywords.FOOTBALL, comment):
                            new_com = func.remove_prefixes(keywords.FOOTBALL, comment)
                            if func.equals(keywords.GOAL, new_com):
                                await gp.footaball_process(message)
                            elif func.equals(keywords.MISS, new_com):
                                await gp.footaball_process(message, 'miss')
                            else:
                                await func.invalid_syntax(message, amount, asset, user_id, username, name)
                        elif func.contains(keywords.BOWLING, comment):
                            new_com = func.remove_prefixes(keywords.BOWLING, comment)
                            if new_com.isdigit():
                                stake = int(new_com)
                                if -1 < stake < 7:
                                    await gp.bowling_process(message, stake)
                            elif func.equals(keywords.STRIKE, new_com):
                                await gp.bowling_process(message, 0)
                            else:
                                await func.invalid_syntax(message, amount, asset, user_id, username, name)
                        elif "мины " in comment:
                            if not main.db.user_played_mines(user_id):
                                new_com = comment
                                new_com = new_com.removeprefix("мины ")
                                if new_com.isdigit():
                                    n = int(int(new_com))
                                    if 25 > n > 2:
                                        c = 0
                                        coef += 1
                                        await message.reply(f"*⚡Выберете любой слот*\n*Клеток открыто:* 0\n*Коэффицент:* 1X\n*Выигрыш:* {round(amount * coef, 2)}  {asset}", 'markdown', reply_markup=keyboards.functional.create_mine_keyboards(n, user_id, amount, asset, username))
                                    else:
                                        await func.invalid_syntax(message, amount, asset, user_id, username, name)
                                else:
                                    await func.invalid_syntax(message, amount, asset, user_id, username, name)
                            else:
                                if amount < dict(await get_balance())[asset]:
                                    if amount < 1:
                                        check = await crypto.create_check(asset, amount - amount * 0.1)
                                        main.db.add_check(user_id, check.check_id)
                                        msag = await message.reply("<b>❗Вы ещё не завершили предыдущую игру</b>\n\n<blockquote><b>Нажмите на кнопку ниже, чтобы вернуть деньги c комиссией 10%!</b></blockquote>", 'html', reply_markup=keyboards.functional.create_url_button(await get_start_link(user_id, True), "Вернуть💸"))
                                    else:
                                        await crypto.transfer(user_id, asset, amount - amount * 0.1, text.rnd_id())
                                        msag = await message.reply("<b>❗Вы ещё не завершили предыдущую игру</b>\n\n<blockquote><b>Деньги возвращены на ваш баланс c комиссией 10%!</b></blockquote>", 'html')
                                else:
                                    msag = await message.reply("*❗Вы ещё не завершили предыдущую игру*\n\n<blockquote>Напишите администрации для возвращения средств!</blockquote>", 'markdown')
                                await asyncio.sleep(20)
                                await msag.delete()
                        else:
                            if func.equals(keywords.EVEN, comment):
                                await gp.dice_procces(message, 'even')
                            elif func.equals(keywords.ODD, comment):
                                await gp.dice_procces(message, 'odd')
                            elif func.equals(keywords.RED, comment):
                                await gp.darts_procces(message, 'r')
                            elif func.equals(keywords.WHITE, comment):
                                await gp.darts_procces(message, 'w')
                            elif func.equals(keywords.DARTS, comment) or func.equals(keywords.CENTER, comment):
                                await gp.darts_procces(message)
                            elif func.equals(keywords.BASKET, comment):
                                await gp.basketball_process(message)
                            elif func.equals(keywords.FOOTBALL, comment):
                                await gp.footaball_process(message)
                            elif func.equals(keywords.BOWLING, comment) or func.equals(keywords.STRIKE, comment):
                                await gp.bowling_process(message, 0)
                            elif func.equals(keywords.Plinko, comment):
                                await gp.dice_procces(message, 'pl')
                            elif func.equals(keywords.Zone1, comment):
                                await gp.dice_procces(message, 'zone1')
                            elif func.equals(keywords.Zone2, comment):
                                await gp.dice_procces(message, 'zone2')
                            elif func.equals(keywords.Zone3, comment):
                                await gp.dice_procces(message, 'zone3')
                            elif func.equals(keywords.DUELN, comment):
                                await gp.duel_nproccess(message,'🎲')
                            elif func.equals('2м',comment):
                                await gp.procces2(message, '2m')
                            elif func.equals(keywords.SLOTS, comment):
                                msg = await message.reply_dice('🎰')
                                v = msg.dice.value
                                await asyncio.sleep(6)
                                if v == 64:
                                    await func.winner(message, amount, asset, coefs.SLOTS_777 + coef, user_id, username, "Победа! Вы выбили три в ряд!", type="cas") #777
                                elif v == 1 or v==22:
                                    await func.winner(message, amount, asset, coefs.SLOTS_GRAPE + coef, user_id,  username, "Победа! Вы выбили три в ряд!", type="cas") #bar and grape
                                elif v == 43:
                                    await func.winner(message, amount, asset, coefs.SLOTS_LEMON + coef, user_id, username, "Победа! Вы выбили три в ряд!", type="cas")
                                else:
                                    None
                            elif comment in ['камень', 'ножницы','бумага']:
                                await gp.knb_procces(message, comment)
                            else:
                                await func.invalid_syntax(message, amount, asset, user_id, username, name)
                    else:
                        #если нет комента
                        message = await main.bot.send_message(config.MAIN_CHANNEL, text.get_stake(amount, asset, '❌', name), 'html')
                        await func.invalid_syntax(message, amount, asset, user_id, username, name)
                        await asyncio.sleep(20)
                        await message.delete()
                else:
                    #если бан
                    await main.bot.send_message(config.LOG_CHANNEL, f"Забанненый {username}({user_id}) отправил {amount} {asset}")
            else:
                #если нет ссылки на акк
                await main.bot.send_message(config.LOG_CHANNEL, f"Не удалось распознать ставку пользователя с именем {name}! Ставка{amounta}{asset}")
                masage = await main.bot.send_message(config.MAIN_CHANNEL, f"Мы не смогли опознать игрока с именем <b>{name}</b>! \n\n⚠️Проблема возможно возникла из-за ваших настроек пересылки сообщений!", "html")
                await asyncio.sleep(20)
                await masage.delete()



def register_handlers(dp: Dispatcher):
    dp.register_channel_post_handler(getter, ChatTypeFilter(ChatType.CHANNEL), text_contains="отправил(а)")
