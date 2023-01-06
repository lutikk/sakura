from vkbottle.user import Message, UserLabeler

from models import User
from utils import edit_message
from validators import MyPref

bl = UserLabeler()
bl.vbml_ignore_case = True


@bl.message(MyPref(), text='<q> агенты')
async def greeting(e: Message):
    t = '👨🏼‍💻 Агенты ТП YoRHa:\n\n'
    agent = await User.filter(rang=2)
    if len(agent) == 0:
        await edit_message(e, "❎ Нету пользователей на ранге Агент.")
        return
    else:
        for ss in agent:
            t += f'👤 [id{ss.vkontakte_id}|{ss.nick_name}]\n'
        await edit_message(e, t)
        return

@bl.message(MyPref(), text='<q> админы')
async def greeting(e: Message):
    t = '👨🏼‍💻 Админы LP | YoRHa:\n\n'
    admin = await User.filter(rang=3)
    if len(admin) == 0:
        await edit_message(e, "❎ Нету пользователей на ранге Админ.")
        return
    else:
        for sss in admin:
            t += f'👤 [id{sss.vkontakte_id}|{sss.nick_name}]\n'
        await edit_message(e, t)
        return

