from threading import Thread

from vkbottle.user import Message, UserLabeler

from models import User
from utils import edit_message, get_user_id, user_id_get_mes, check_token
from validators import MyPref
from workers.frends import clear_friends, clear_dog, clear_uved

bl = UserLabeler()
bl.vbml_ignore_case = True


@bl.message(MyPref(), text='<q> +др')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message=message)
    await message.ctx_api.friends.add(user_id)
    a = await message.get_user(user_ids=user_id)
    name = f'[id{a.id}|{a.first_name} {a.last_name}]'
    text = f'✅ {name} добавлен в друзья.'
    await edit_message(message, text)


@bl.message(MyPref(), text='<q> +др <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    await message.ctx_api.friends.add(user_id)
    a = await message.get_user(user_ids=user_id)
    name = f'[id{a.id}|{a.first_name} {a.last_name}]'
    text = f'✅ {name} добавлен в друзья.'
    await edit_message(message, text)


@bl.message(MyPref(), text='<q> -др')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message=message)
    await message.ctx_api.friends.delete(user_id)
    a = await message.get_user(user_ids=user_id)
    name = f'[id{a.id}|{a.first_name} {a.last_name}]'
    text = f'✅ {name} удалён из друзей.'
    await edit_message(message, text)


@bl.message(MyPref(), text='<q> -др <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    await message.ctx_api.friends.delete(user_id)
    a = await message.get_user(user_ids=user_id)
    name = f'[id{a.id}|{a.first_name} {a.last_name}]'
    text = f'✅ {name} удалён из друзей.'
    await edit_message(message, text)


@bl.message(MyPref(), text='<q> !др')
async def greeting(message: Message):
    text = f"✅ Чистка Friends запущена."
    Thread(target=clear_friends).start()
    await edit_message(message, text)


@bl.message(MyPref(), text='<q> !собак')
async def greeting(message: Message):
    text = f"✅ Чистка DeadFriends запущена."
    Thread(target=clear_dog).start()
    await edit_message(message, text)


@bl.message(MyPref(), text='<q> +ув')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    user_db = await User.get(vkontakte_id=message.from_id)
    await message.ctx_api.request("wall.subscribe", {"owner_id": user_id})
    text = f"{user_db.text_uv}"

    await edit_message(message, text)


@bl.message(MyPref(), text='<q> +ув <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    await message.ctx_api.request("wall.subscribe", {"owner_id": user_id})
    user_db = await User.get(vkontakte_id=message.from_id)
    text = f"{user_db.text_uv}"

    await edit_message(message, text)


@bl.message(MyPref(), text='<q> -ув')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    await message.ctx_api.request("wall.unsubscribe", {"owner_id": user_id})
    text = f"✅ [id{user_id}|Выключил уведомления.]"

    await edit_message(message, text)


@bl.message(MyPref(), text='<q> -ув <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    await message.ctx_api.request("wall.unsubscribe", {"owner_id": user_id})
    text = f"✅ [id{user_id}|Выключил уведомления.]"

    await edit_message(message, text)


@bl.message(MyPref(), text='<q> !исток')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)

    if check_token(user.token_vkme) == 2:
        text = "⚠ Для использования данной функции необходим токен vk me."
        await edit_message(message, text)
        return
    else:

        text = f"✅ Чистка Sources запущена."
        Thread(target=clear_uved, args=(user.token_vkme, )).start()
        await edit_message(message, text)
