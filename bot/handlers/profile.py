from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from bot import keyboards
from bot.utils import text
from bot.utils.cryptopay import crypto, get_balance
from bot.states import states_groups
import main
async def cb_withdraw(call: CallbackQuery, state: FSMContext):
    if main.db.get_moneyback(call.from_user.id) >= 1:
        await call.message.edit_caption("Введите сумму вывода:", reply_markup=keyboards.start_keyboards.back_keyboard)
        await states_groups.UserState.withdraw.set()
        async with state.proxy() as data:
            data['msg'] = call.message
    else:
        await call.answer("⚠️Сумма на балансе должна превышать 1 USDT", show_alert=True)

async def amount_handler(message: Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            msg = data['msg']
        amount = float(message.text)
        if amount >= 1:
            if amount <= main.db.get_moneyback(message.from_user.id):
                if amount <= dict(await get_balance())['USDT']:
                    print("член")
                    check = await crypto.create_check("USDT", amount)
                    await message.answer("*Возьмите заслуженную награду!*", 'markdown', reply_markup=keyboards.functional.create_url_button(check.bot_check_url))
                    main.db.edit_moneyback(message.from_user.id, -amount)
                    await msg.edit_caption(text.get_profile(message.from_user.id, message.from_user.username), 'html', reply_markup=keyboards.start_keyboards.profile_keyboard)
                    await state.finish()
                else:
                    await message.answer("⚠️Произошли технические проблемы при снятии баланса!\n\nСвяжитесь с администрацией")
                    await msg.edit_caption(text.get_profile(message.from_user.id, message.from_user.username), 'html', reply_markup=keyboards.start_keyboards.profile_keyboard)
                    await state.finish()
            else:
                await message.answer("У вас нет таких средств")
        else:
            await message.answer("*⚠️Сумма снятия должна быть выше 1 USDT*", 'markdown')
    except ValueError:     
        await message.answer("Вы ввели не число!")   

async def cb_back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_caption(text.get_profile(call.from_user.id, call.from_user.username), 'html', reply_markup=keyboards.start_keyboards.profile_keyboard)
    
def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(cb_withdraw, text="withdraw")
    dp.register_message_handler(amount_handler, state=states_groups.UserState.withdraw)
    dp.register_callback_query_handler(cb_back_to_menu, text="back_to_menu", state='*')

