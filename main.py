from threading import Thread

from vkbottle.user import User

from commands import labelers
from config import init_tortoise
from config import token, user_id
from middlewares import UserIgnore, FiltersIwents
from workers.auto import start
from loguru import logger as log
import sys
bot = User(token)

bot.labeler.vbml_ignore_case = True
for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)

session_manager = True
ignore_error = True
ask_each_event = True

bot.labeler.message_view.register_middleware(UserIgnore)
bot.labeler.message_view.register_middleware(FiltersIwents)
Thread(target=start, args=(user_id, )).start()
bot.loop_wrapper.on_startup = [init_tortoise()]
if not "логи" in sys.argv:
    log.remove()
    log.disable('vkbottle')

if __name__ == "__main__":
    bot.run_forever()
