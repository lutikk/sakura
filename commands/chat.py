from vkbottle.user import Message, UserLabeler

from utils import edit_message, get_user_id, user_id_get_mes
from validators import MyPref

bl = UserLabeler()
bl.vbml_ignore_case = True


@bl.message(MyPref(), text='<q> добавить')
async def greeting(message: Message):
    try:
        user_id = await user_id_get_mes(message)
        await message.ctx_api.request("messages.addChatUser", {"user_id": user_id,
                                                               "chat_id": message.peer_id - 2000000000})
        text = '✅ Добавлен в чат.'
        await edit_message(message, text)
    except Exception as ex:
        await edit_message(message, f"Ошибка: {ex}")


@bl.message(MyPref(), text='<q> добавить <url>')
async def greeting(message: Message, url: str):
    try:
        user_id = get_user_id(url)[0]
        await message.ctx_api.request("messages.addChatUser", {"user_id": user_id,
                                                               "chat_id": message.peer_id - 2000000000})
        text = '✅ Добавлен в чат.'
        await edit_message(message, text)
    except Exception as ex:
        await edit_message(message, f"Ошибка: {ex}")


@bl.message(MyPref(), text='<q> +админ')
async def greeting(message: Message):
    try:
        user_id = await user_id_get_mes(message)
        await message.ctx_api.request("messages.setMemberRole",
                                      {"peer_id": message.peer_id, "member_id": user_id, "role": "admin"})
        text = f"✅ [id{user_id}|Права администратора выданы.]"
        await edit_message(message, text)
    except Exception as ex:
        await edit_message(message, f'Ошибка: {ex}')


@bl.message(MyPref(), text='<q> +админ <url>')
async def greeting(message: Message, url: str):
    try:
        user_id = get_user_id(url)[0]
        await message.ctx_api.request("messages.setMemberRole",
                                      {"peer_id": message.peer_id, "member_id": user_id, "role": "admin"})
        text = f"✅ [id{user_id}|Права администратора выданы.]"
        await edit_message(message, text)
    except Exception as ex:
        await edit_message(message, f'Ошибка: {ex}')


@bl.message(MyPref(), text='<q> -админ')
async def greeting(message: Message):
    try:
        user_id = await user_id_get_mes(message)
        await message.ctx_api.request("messages.setMemberRole",
                                      {"peer_id": message.peer_id, "member_id": user_id, "role": "member"})
        text = f"✅ С [id{user_id}|Права администратора сняты.]"
        await edit_message(message, text)
    except Exception as ex:
        await edit_message(message, f"Ошибка: {ex}")


@bl.message(MyPref(), text='<q> -админ <url>')
async def greeting(message: Message, url: str):
    try:
        user_id = get_user_id(url)[0]
        await message.ctx_api.request("messages.setMemberRole",
                                      {"peer_id": message.peer_id, "member_id": user_id, "role": "member"})
        text = f"✅ С [id{user_id}|Права администратора сняты.]"
        await edit_message(message, text)
    except Exception as ex:
        await edit_message(message, f"Ошибка: {ex}")


@bl.message(MyPref(), text='<q> кик')
async def greeting(message: Message):
    try:
        user_id = await user_id_get_mes(message)
        await message.ctx_api.request("messages.removeChatUser", {"member_id": user_id,
                                                                  "chat_id": message.peer_id - 2000000000})
        text = f"✅ Исключен с беседы."
        await edit_message(message, text)
    except Exception as ex:
        await edit_message(message, f'Ошибка: {ex}')


@bl.message(MyPref(), text='<q> кик <url>')
async def greeting(message: Message, url: str):
    try:
        user_id = get_user_id(url)[0]
        await message.ctx_api.request("messages.removeChatUser", {"member_id": user_id,
                                                                  "chat_id": message.peer_id - 2000000000})
        text = f"✅ Исключен с беседы."
        await edit_message(message, text)
    except Exception as ex:
        await edit_message(message, f'Ошибка: {ex}')


@bl.message(MyPref(), text='<q> выйти')
async def greeting(message: Message):
    text = f"✅ Покинул беседу"
    await edit_message(message, text)
    await message.ctx_api.request("messages.removeChatUser", {"member_id": message.from_id,
                                                              "chat_id": message.peer_id - 2000000000})
