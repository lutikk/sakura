from vkbottle.user import Message, UserLabeler

from utils import edit_message, get_user_id, user_id_get_mes
from validators import MyPref

bl = UserLabeler()
bl.vbml_ignore_case = True


@bl.message(MyPref(), text='<q> +чс')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    a = await message.get_user(user_ids=user_id)
    name = f'[id{a.id}|{a.first_name} {a.last_name}]'
    await message.ctx_api.account.ban(user_id)
    await edit_message(message, f'✅ {name} добавлен в ЧС')


@bl.message(MyPref(), text='<q> +чс <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    a = await message.get_user(user_ids=user_id)
    name = f'[id{a.id}|{a.first_name} {a.last_name}]'
    await message.ctx_api.account.ban(user_id)
    await edit_message(message, f'✅ {name} добавлен в ЧС')


@bl.message(MyPref(), text='<q> -чс')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    a = await message.get_user(user_ids=user_id)
    name = f'[id{a.id}|{a.first_name} {a.last_name}]'
    await message.ctx_api.account.unban(user_id)
    await edit_message(message, f'✅ {name} удален из ЧС')


@bl.message(MyPref(), text='<q> -чс <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    a = await message.get_user(user_ids=user_id)
    name = f'[id{a.id}|{a.first_name} {a.last_name}]'
    await message.ctx_api.account.unban(user_id)
    await edit_message(message, f'✅ {name} удален из ЧС')
