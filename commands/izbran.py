from vkbottle.user import Message, UserLabeler

from models import User
from utils import edit_message
from validators import MyPref

bl = UserLabeler()
bl.vbml_ignore_case = True


@bl.message(MyPref(), text='<q> +изб')
async def greeting(message: Message):
    user_db = await User.get(vkontakte_id=message.from_id)
    spi = eval(user_db.dont_clear_message)
    if message.peer_id < 0:
        return
    if message.peer_id in spi:
        await edit_message(message, "Чат уже есть в избранном.")
        return
    else:
        spi.append(message.peer_id)
        user_db.dont_clear_message = spi
        await user_db.save()
        await edit_message(message, f"✅ Чат добавлен в избранное.")


@bl.message(MyPref(), text='<q> -изб')
async def greeting(message: Message):
    user_db = await User.get(vkontakte_id=message.from_id)
    spi = eval(user_db.dont_clear_message)
    if message.peer_id < 0:
        return
    if message.peer_id in spi:
        spi.remove(message.peer_id)
        user_db.dont_clear_message = spi
        await user_db.save()
        await edit_message(message, f"✅ Чат удален из избранного.")
        return
    else:
        await edit_message(message, f"❎ Чата нет в избранном.")


@bl.message(MyPref(), text='<q> изб')
async def greeting(message: Message):
    user = []
    chat = []
    txt = '👁‍🗨 Избранные чаты:\n\n'
    user_db = await User.get(vkontakte_id=message.from_id)
    spi = eval(user_db.dont_clear_message)
    if len(spi) == 0:
        await edit_message(message, f"⚠ Нет избранных чатов.")
        return
    for element in spi:
        if element > 2000000000:
            element = element - 2000000000
            chat.append(element)
        else:
            user.append(element)

    txt += '👤 Пользователи:\n'

    for ss in user:
        a = await message.get_user(user_ids=ss)
        name = f'[id{a.id}|{a.first_name} {a.last_name}]'
        txt += f'{name}\n'
    txt += '\n👥 Беседы:\n\n'
    for sss in chat:
        ch = await message.ctx_api.request("messages.getChat", {"chat_ids": sss})
        name = f'{ch["response"][0]["title"]}'
        txt += f'{name}'

    await edit_message(message, txt)
