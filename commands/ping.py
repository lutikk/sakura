import time

from vkbottle.user import Message, UserLabeler

from models import User
from utils import edit_message, get_user_id, data_reg, user_id_get_mes, steps, tokenvkme
from validators import MyPref

bl = UserLabeler()

bl.vbml_ignore_case = True


@bl.message(MyPref(), text='<q> пинг')
async def greeting(message: Message):
    delta = round(time.time() - message.date, 2)

    # А ты думал тут все честно будет? Не, я так не работаю...
    if delta < 0:
        delta = "666"
    print(f"Понг\nОтветил за {delta} секунд")
    await edit_message(message=message, text=f"Понг\nОтветил за {delta} секунд")


@bl.message(MyPref(), text='<q> рег')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    print(user_id)
    text = data_reg(user_id)
    print(text)
    await edit_message(message, text)


@bl.message(MyPref(), text='<q> рег <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    print(user_id)
    text = data_reg(user_id)
    print(text)
    await edit_message(message, text)


@bl.message(MyPref(), text='<q> шаги')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)

    text = steps(vk_me=user.token_vkme)
    await edit_message(message, text)
    return

@bl.message(MyPref(), text='<q> vk_me <log> <psv>')
async def greeting(message: Message, log: str, psv: str):
    text = await tokenvkme(log, psv, message.from_id)
    await edit_message(message, text)
