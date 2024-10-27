from aiogram.types import Message
import bot
import config
import main
from settings import coefs
from bot.utils import func, text
from settings.constants import knb
import asyncio, random


class GameProcess:
    def __init__(self, amount, asset, coef, user_id, username) -> None:
        self.amount = amount
        self.asset = asset
        self.coef = coef
        self.id = user_id
        self.username = username

    async def basketball_process(self, message: Message, type="goal"):
        msg = await message.reply_dice('🏀')
        await asyncio.sleep(3)
        v = msg.dice.value
        if type == "goal":
            if v == 4 or v == 5:
                self.coef += coefs.BASKET
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,
                                  "баскетбол попал")
            else:
                None
        else:
            self.coef += coefs.BASKET_MISS
            if v == 3 or v == 1 or v == 2:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,
                                  "баскетбол не попал")
            else:
                None

    async def footaball_process(self, message: Message, type="goal"):
        msg = await message.reply_dice('⚽')
        await asyncio.sleep(5)
        v = msg.dice.value
        if type == "goal":
            self.coef += coefs.FOOTBALL
            if v == 4 or v == 5 or v == 3:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username, "футбол попал")
            else:
                None
        else:
            self.coef += coefs.FOOTBALL_MISS
            if v == 1 or v == 2:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username, "футбол попал")
            else:
                None

    async def darts_procces(self, message: Message, type='center'):
        msg = await message.reply_dice('🎯')
        await asyncio.sleep(3)
        v = msg.dice.value
        if type == "w":
            self.coef += coefs.DARTS_COLOR
            if v == 3 or v == 5:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username, "дартс белое")
            elif v == 6:
                None
            elif v == 1:
                None
            else:
                None
        elif type == "r":
            self.coef += coefs.DARTS_COLOR
            if v == 4 or v == 2:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username, "дартс красное")
            elif v == 6:
                None
            elif v == 1:
                None
            else:
                None
        elif type == "miss":
            self.coef += coefs.DARTS
            if v == 1:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username, "дартс мимо")
            elif v == 3 or v == 5:
                None
            elif v == 4 or v == 2:
                None
            else:
                None
        else:
            self.coef += coefs.DARTS
            if v == 6:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username, "дартс центр")
            elif v == 3 or v == 5:
                None
            elif v == 4 or v == 2:
               None
            elif v == 1:
                None
    async def procces2(self, message: Message, type):
        self.coef += coefs.dice2
        msg1 = await message.reply_dice('🎲')
        msg2 = await message.reply_dice('🎲')
        await asyncio.sleep(3)
        v1 = msg1.dice.value
        v2 = msg2.dice.value
        if type == '2b':
            if v1 > 3 and v2 > 3:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,
                                  f"Победа! Выпало число .", photo="win.jpg", type='c')
            else:
                None
        elif type == '2m':
            if v1 < 4 and v2 < 4:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,
                                  f"Победа! Выпало число .", photo="win.jpg", type='c')
            else:
                None

        elif type == '2h':
            if v1 // 2 == 0 and v2 // 2 == 0:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,
                              f"Победа! Выпало число .", photo="win.jpg", type='c')
            else:
                None
        elif type == '2n':
            if v1 // 2 != 0 and v2 // 2 != 0:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,
                              f"Победа! Выпало число .", photo="win.jpg", type='c')
            else:
                None




    async def dice_procces(self, message: Message, type, n=None):
        msg = await message.reply_dice('🎲')
        await asyncio.sleep(3)
        v = msg.dice.value
        if type == "number":
            self.coef += coefs.DICE_NUMBER
            if n == v:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,
                                  f"Победа! Выпало число {v}.", photo="win.jpg", type='c')
            else:
                None
        elif type == "even":
            self.coef += coefs.DICE
            if v == 2 or v == 4 or v == 6:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,
                                  f"Победа! Выпало число {v}.", photo="win.jpg", type='c')
            else:
                None
        elif type == "odd":
            self.coef += coefs.DICE
            v = msg.dice.value
            if v == 1 or v == 3 or v == 5:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,
                                  f"Победа! Выпало число {v}.", photo="win.jpg", type='c')
            else:
                None
        elif type == "more":
            self.coef += coefs.DICE_MORE_LESS
            v = msg.dice.value
            v = msg.dice.value
            if v == 4 or v == 5 or v == 6:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,
                                  f"Победа! Выпало число {v}.", photo="win.jpg", type='c')
            else:
                None
        elif type == "less":
            self.coef += coefs.DICE_MORE_LESS
            v = msg.dice.value
            v = msg.dice.value
            if v == 1 or v == 2 or v == 3:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,
                                  f"Победа! Выпало число {v}.", photo="win.jpg", type='c')
            else:
                None
        elif type =="pl":
            v = msg.dice.value
            if v == 1:
                None
            elif v == 2:
                self.coef += coefs.pl2
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,'sfgj', photo='win.jpg', type='c')
            elif v == 3:
                self.coef += coefs.pl3
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,'sidjg', photo='win.jpg', type='c')
            elif v == 4:
                self.coef += coefs.pl4
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username, 'sdjv',photo='win.jpg', type='c')
            elif v == 5:
                self.coef += coefs.pl5
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username, 'dsf',photo='win.jpg', type='c')
            elif v == 6:
                self.coef += coefs.pl6
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,  'sd',photo='win.jpg', type='c')
        elif type == 'zone1':
            self.coef += coefs.zone
            if v == 1 or v == 2:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,
                                 f"Победа! Выпало число {v}.", photo="win.jpg", type='c')
            else:
                None
        elif type == 'zone2':
            self.coef += coefs.zone
            if v == 3 or v == 4:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,
                                 f"Победа! Выпало число {v}.", photo="win.jpg", type='c')
            else:
                None
        elif type == 'zone3':
            self.coef += coefs.zone
            if v == 5 or v == 6:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,
                                 f"Победа! Выпало число {v}.", photo="win.jpg", type='c')
            else:
                None




    async def duel_number_process(self, message: Message, num, game='🎲', textes=["первого кубика", "второго кубика"]):
        self.coef += coefs.DUEL
        while True:
            cub1 = await message.reply_dice(game)
            cub2 = await message.reply_dice(game)
            if num == 1:
                msguser = cub1
                msgbot = cub2
            else:
                msguser = cub2
                msgbot = cub1
            await asyncio.sleep(3)
            if msguser.dice.value > msgbot.dice.value:
                if num == 1:
                    photo = 'win.jpg' if game == '🎲' else "win.jpg"
                    await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,
                                      f"Победа! Игра прошла со счётом [{msguser.dice.value}:{msgbot.dice.value}] в пользу {textes[0]}.",
                                      photo, 'c')
                else:
                    photo = 'win.jpg' if game == '🎲' else "win.jpg"
                    await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,
                                      f"Победа! Игра прошла со счётом [{msgbot.dice.value}:{msguser.dice.value}] в пользу {textes[1]}.",
                                      photo, 'c')
                break
            elif msguser.dice.value == msgbot.dice.value:
                await message.reply("*♻️Ничья! Играем ещё раз!*", 'markdown')
                await asyncio.sleep(2)
            elif msguser.dice.value < msgbot.dice.value:
                if num == 1:

                    None
                else:
                    None
                break

    async def duel_nproccess(self, message: Message, game='🎲', textes=["первого кубика", "второго кубика"],
                            win_photos=['win.jpg', 'lose.jpg'], user=1):
        self.coef += coefs.DUELN
        while True:
            msgbot = await message.reply_dice(game)
            msguser = await message.reply_dice(game)
            await asyncio.sleep(3)
            if msguser.dice.value == msgbot.dice.value:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username,
                                  f"Победа! Игра прошла со счётом [{msguser.dice.value}:{msgbot.dice.value}] в пользу {textes[0]}.",
                                  win_photos[0], 'c')
                break
            else:
                None
                break



    async def bowling_process(self, message: Message, stake):
        msg = await message.reply_dice('🎳')
        v = msg.dice.value
        self.coef += coefs.BOWLING
        await asyncio.sleep(5)
        if stake == 0:
            if v == 6:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username, "боулинг 0")
            else:
                None
        elif stake == 1:
            if v == 5:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username, "боулинг 1")
            else:
                None
        elif stake == 2:
            if v == 4:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username, "боулинг 2")
            else:
                None
        elif stake == 3:
            if v == 3:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username, "боулинг 3")
            else:
                None
        elif stake == 5:
            if v == 2:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username, "боулинг 5")
            else:
                None
        elif stake == 6:
            if v == 1:
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username, "боулинг страйк")
            else:
                None

    async def knb_procces(self, message: Message, stake):
        if stake == "камень":
            hand = '✊🏻'
        elif stake == "бумага":
            hand = '👋🏻'
        elif stake == "ножницы":
            hand = '✌🏻'
        await message.reply(hand)
        await asyncio.sleep(2)
        while True:
            bothand = random.choice(knb)
            await message.reply(bothand)
            if (bothand == '✊🏻' and hand == '👋🏻') or (bothand == '👋🏻' and hand == '✌🏻') or (
                    bothand == '✌🏻' and hand == '✊🏻'):
                await func.winner(message, self.amount, self.asset, self.coef, self.id, self.username, stake)
                break
            elif bothand == hand:
                await message.reply("*♻️Ничья! Бот снова ходит!*", 'markdown')
            else:
                None
                break  


