from vkbottle.user import Message, UserLabeler

from models import User
from utils import edit_message, get_user_id, user_id_get_mes
from validators import MyPref

bl = UserLabeler()
bl.vbml_ignore_case = True


@bl.message(MyPref(), text='<q> +игнор')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    if user_id == message.from_id:
        await edit_message(message, 'Суицид не выход\nЭто вход')
        return
    user_db = await User.get(vkontakte_id=message.from_id)
    spi = eval(user_db.list_ignore)
    if user_id < 0:
        return
    if user_id in spi:
        await edit_message(message, f"🚫 Уже в игнор-листе.")
        return
    else:
        spi.append(user_id)
        user_db.list_ignore = spi
        await user_db.save()
        await edit_message(message, f"✅ Добавлен в список игнора.")


@bl.message(MyPref(), text='<q> +игнор <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    if user_id == message.from_id:
        await edit_message(message, 'Суицид не выход\nЭто вход')
        return
    user_db = await User.get(vkontakte_id=message.from_id)
    spi = eval(user_db.list_ignore)
    if user_id < 0:
        return
    if user_id in spi:
        await edit_message(message, f"🚫 Уже в игнор-листе.")
        return
    else:
        spi.append(user_id)
        user_db.list_ignore = spi
        await user_db.save()
        await edit_message(message, f"✅ Добавлен в список игнора.")


@bl.message(MyPref(), text='<q> -игнор')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    if user_id == message.from_id:
        await edit_message(message, 'Суицид не выход\nЭто вход')
        return
    user_db = await User.get(vkontakte_id=message.from_id)
    spi = eval(user_db.list_ignore)
    if user_id < 0:
        return
    if user_id in spi:
        spi.remove(user_id)
        user_db.list_ignore = spi
        await user_db.save()
        await edit_message(message, f"✅ Удален из списка игнора.")
        return
    else:
        await edit_message(message, f"❎ Нет в списке игнора.")


@bl.message(MyPref(), text='<q> -игнор <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    if user_id == message.from_id:
        await edit_message(message, 'Суицид не выход\nЭто вход')
    user_db = await User.get(vkontakte_id=message.from_id)
    spi = eval(user_db.list_ignore)
    if user_id < 0:
        return
    if user_id in spi:
        spi.remove(user_id)
        user_db.list_ignore = spi
        await user_db.save()
        await edit_message(message, f"✅ Удален из списка игнора.")
        return
    else:
        await edit_message(message, f"❎ Нет в списке игнора.")


@bl.message(MyPref(), text='<q> игнор')
async def greeting(message: Message):
    txt = '👥 Игнорируемые пользователи:\n\n'
    user_db = await User.get(vkontakte_id=message.from_id)
    spi = eval(user_db.list_ignore)
    if len(spi) == 0:
        await edit_message(message, f"🚫 Игнор-лист пуст.")
        return

    for ss in spi:
        a = await message.get_user(user_ids=ss)
        name = f'[id{a.id}|{a.first_name} {a.last_name}]\n'
        txt += f'{name}\n'
    await edit_message(message, txt)
