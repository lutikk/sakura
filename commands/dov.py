from vkbottle.user import Message, UserLabeler

from models import User
from utils import edit_message, get_user_id, user_id_get_mes
from validators import MyPref, Dov

bl = UserLabeler()
bl.vbml_ignore_case = True


@bl.message(MyPref(), text='<q> +дов')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    if user_id == message.from_id:
        await edit_message(message, '🚫 Нельзя добавить самого себя в доверенных.')
        return
    if user_id < 0:
        return
    user_db = await User.get(vkontakte_id=message.from_id)
    spi = eval(user_db.list_trusted)
    if user_id in spi:
        await edit_message(message, '🚫 Уже в списке довов.')
        return
    else:
        spi.append(user_id)
        user_db.list_trusted = spi
        await user_db.save()
        a = await message.get_user(user_ids=user_id)
        name = f'[id{a.id}|{a.first_name} {a.last_name}]'
        await edit_message(message, f'✅ {name} добавлен в доверенных.')


@bl.message(MyPref(), text='<q> +дов <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    if user_id == message.from_id:
        await edit_message(message, '🚫 Нельзя добавить самого себя в доверенных.')
        return
    if user_id < 0:
        return
    user_db = await User.get(vkontakte_id=message.from_id)
    spi = eval(user_db.list_trusted)
    if user_id in spi:
        await edit_message(message, '🚫 Уже в списке довов.')
        return
    else:
        spi.append(user_id)
        user_db.list_trusted = spi
        await user_db.save()
        a = await message.get_user(user_ids=user_id)
        name = f'[id{a.id}|{a.first_name} {a.last_name}]'
        await edit_message(message, f'✅ {name} добавлен в доверенных.')


@bl.message(MyPref(), text='<q> довы')
async def greeting(message: Message):
    user_db = await User.get(vkontakte_id=message.from_id)
    spi = eval(user_db.list_trusted)
    text = '👤 Ты доверяешь:\n\n'
    if len(spi) == 0:
        await edit_message(message, "⚙ Доверенных нету.")
        return
    for s in spi:
        a = await message.get_user(user_ids=s)
        name = f'[id{a.id}|{a.first_name} {a.last_name}]\n'
        text += name
    await edit_message(message, text)


@bl.message(MyPref(), text='<q> -дов')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    if user_id == message.from_id:
        await edit_message(message, '🚫 Нельзя удалить с довов.')
        return
    if user_id < 0:
        return
    user_db = await User.get(vkontakte_id=message.from_id)
    spi = eval(user_db.list_trusted)
    if user_id in spi:
        spi.remove(user_id)
        user_db.list_trusted = spi
        await user_db.save()
        a = await message.get_user(user_ids=user_id)
        name = f'[id{a.id}|{a.first_name} {a.last_name}]'
        await edit_message(message, f'✅ {name} удален с доверенных.')
        return
    else:
        a = await message.get_user(user_ids=user_id)
        name = f'[id{a.id}|{a.first_name} {a.last_name}]'
        await edit_message(message, f'🚫 {name} не был в доверенных.')


@bl.message(MyPref(), text='<q> -дов <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    if user_id == message.from_id:
        await edit_message(message, '🚫 Нельзя удалить с довов.')
        return
    if user_id < 0:
        return
    user_db = await User.get(vkontakte_id=message.from_id)
    spi = eval(user_db.list_trusted)
    if user_id in spi:
        spi.remove(user_id)
        user_db.list_trusted = spi
        await user_db.save()
        a = await message.get_user(user_ids=user_id)
        name = f'[id{a.id}|{a.first_name} {a.last_name}]'
        await edit_message(message, f'✅ {name} удален с доверенных.')
        return
    else:
        a = await message.get_user(user_ids=user_id)
        name = f'[id{a.id}|{a.first_name} {a.last_name}]'
        await edit_message(message, f'🚫 {name} не был в доверенных.')


@bl.message(Dov(), text='<q> <text>')
async def greeting(message: Message, text: str):
    await message.answer(text)
