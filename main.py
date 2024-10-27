from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN, LOG_CHANNEL
from db_worker import DBINIT
import bot.handlers as h





bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = DBINIT('db.db')

async def on_startup(_):
    await bot.send_message(LOG_CHANNEL, f"Бот запустился")
    print("The bot has been started")

def register_handlers():
    h.game.register_handlers(dp)
    h.game.register_handlers(dp)
    h.cmds.register_handlers(dp)
    h.admin.register_handlers(dp)

if __name__ == "__main__":
    register_handlers()
    executor.start_polling(dp, on_startup=on_startup)

