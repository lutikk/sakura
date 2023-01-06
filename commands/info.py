from datetime import datetime

import vk_api
from tortoise.exceptions import DoesNotExist
from vkbottle.user import Message, UserLabeler

from models import User
from utils import edit_message, check_rang, user_id_get_mes, check_token, b2s_govnokod, get_user_id, b2s_str, data_reg
from validators import MyPref, MyPrefSkript

bl = UserLabeler()
bl.vbml_ignore_case = True


async def dop_info(token, user_id):
    'в бутыле не прописан параметр "counters"... костыли наше все'
    vk = vk_api.VkApi(token=token)
    dopinfo = vk.method("users.get", {"user_ids": user_id, "fields": 'counters'})[0]['counters']
    followers = dopinfo.get("followers")
    if followers == None:
        followers = 0
    friends = dopinfo.get("friends")
    if friends == None:
        friends = 0
    videos = dopinfo.get("videos")
    if videos == None:
        videos = 0
    audios = dopinfo.get("audios")
    if audios == None:
        audios = 0
    photos = dopinfo.get("photos")
    if photos == None:
        photos = 0
    gifts = vk.method("gifts.get", {"user_id": user_id})['count']
    groups = vk.method("groups.get", {"user_id": user_id})['count']
    stickers = \
        vk.method("store.getProducts", {"User_id": user_id, "type": "stickers", "filters": "purchased"})["count"]
    text = f"""
╔⫷| Статистика аккаунта:
╠⫸| Подписчиков: {followers}
╠⫸| Аудитория: {followers + friends}
╠⫸| Стикеров: {stickers}
╠⫸| Подарков: {gifts}
╠⫸| Друзей: {friends}
╠⫸| Группы: {groups}
╠⫸| Аудио: {audios}
╠⫸| Видео: {videos}
╚⫸| Фото: {photos}
"""
    return text


@bl.message(MyPref(), text='<q> инфо подробно')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    try:
        user = await User.get(vkontakte_id=user_id)
    except DoesNotExist:
        text = f"[id{user_id}|⚠️Не обнаружен в MySQL.]"
        await edit_message(message, text)
        return
    a = await message.get_user(user_ids=user_id)
    name = f'[id{a.id}|{a.first_name} {a.last_name}]'


    vk_admin = check_token(user.token_vkadmin)
    vk_me = check_token(user.token_vkme)

    info = f"""
╔⫷| {check_rang(user.rang)}: {name}
║
╠⫸| Ник: {user.nick_name}
╠⫸| User ID: {user_id}
║
╠⫷| Инфо токенов:
╠⫸| KTM: {b2s_govnokod(vk_admin)} 
╠⫸| VKME: {b2s_govnokod(vk_me)}
║
╠⫷| Инфо скриптов:
║
╠⫸| Автоотписка: {b2s_str(user.condition_ot)}
╠⫸| Автооффлайн: {b2s_str(user.condition_off)}
╠⫸| Автоонлайн: {b2s_str(user.condition_on)}
╠⫸| Автоприем: {b2s_str(user.condition_dr)}
╠⫸| Автопилот: {b2s_str(user.condition_ao)}
╠⫸| Автолайк: {b2s_str(user.condition_li)}
╠⫸| Автореки: {b2s_str(user.condition_ar)}
║
╠⫷| Статистика скриптов:
║
╠⫸| Автоотписка: {user.stats_ot}
╠⫸| Автоонлайн: {user.stats_on}
╠⫸| Автоприем: {user.stats_dr}
╠⫸| Автолайк: {user.stats_li}
╠⫸| Автореки: {user.stats_ar}
║
╠⫷| Инфо префиксов:
╠⫸| Команды: {user.prefix_commands}
╠⫸| Люкс: {user.pref_luxury}
╠⫸| Скрипты: {user.prefix_scripts}
╚⫸| Повторялка: {user.prefix_repeats}

"""
    await edit_message(message, info)


@bl.message(MyPref(), text='<q> инфо подробно <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    try:
        user = await User.get(vkontakte_id=user_id)
    except DoesNotExist:
        text = f"[id{user_id}|⚠️Не обнаружен в MySQL.]"
        await edit_message(message, text)
        return
    a = await message.get_user(user_ids=user_id)
    name = f'[id{a.id}|{a.first_name} {a.last_name}]'


    vk_admin = check_token(user.token_vkadmin)
    vk_me = check_token(user.token_vkme)

    info = f"""
╔⫷| {check_rang(user.rang)}: {name}
║
╠⫸| Ник: {user.nick_name}
╠⫸| User ID: {user_id}
║
╠⫷| Инфо токенов:
╠⫸| KTM: {b2s_govnokod(vk_admin)} 
╠⫸| VKME: {b2s_govnokod(vk_me)}
║
╠⫷| Инфо скриптов:
║
╠⫸| Автоотписка: {b2s_str(user.condition_ot)}
╠⫸| Автооффлайн: {b2s_str(user.condition_off)}
╠⫸| Автоонлайн: {b2s_str(user.condition_on)}
╠⫸| Автоприем: {b2s_str(user.condition_dr)}
╠⫸| Автопилот: {b2s_str(user.condition_ao)}
╠⫸| Автолайк: {b2s_str(user.condition_li)}
╠⫸| Автореки: {b2s_str(user.condition_ar)}
║
╠⫷| Статистика скриптов:
║
╠⫸| Автоотписка: {user.stats_ot}
╠⫸| Автоонлайн: {user.stats_on}
╠⫸| Автоприем: {user.stats_dr}
╠⫸| Автолайк: {user.stats_li}
╠⫸| Автореки: {user.stats_ar}
║
╠⫷| Инфо префиксов:
╠⫸| Команды: {user.prefix_commands}
╠⫸| Люкс: {user.pref_luxury}
╠⫸| Скрипты: {user.prefix_scripts}
╚⫸| Повторялка: {user.prefix_repeats}

    """
    await edit_message(message, info)


@bl.message(MyPref(), text='<q> инфо')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    try:
        user = await User.get(vkontakte_id=user_id)
    except DoesNotExist:
        text = f"[id{user_id}|⚠️Не обнаружен в MySQL.]"
        await edit_message(message, text)
        return
    a = await message.get_user(user_ids=user_id)
    name = f'[id{a.id}|{a.first_name} {a.last_name}]'

    register_date = data_reg(user_id)
    vk_admin = check_token(user.token_vkadmin)
    vk_me = check_token(user.token_vkme)
    info = f"""
╔⫷| {check_rang(user.rang)}: {name}
║
╠⫸| Ник: {user.nick_name}
╠⫸| User ID: {message.from_id}
╠⫸| {register_date}
║
╠⫷| Инфо токенов:
╠⫸| KTM: {b2s_govnokod(vk_admin)} 
╠⫸| VKME: {b2s_govnokod(vk_me)}
║
╠⫷| Инфо префиксов:
╠⫸| Команды: {user.prefix_commands}
╠⫸| Люкс: {user.pref_luxury}
╠⫸| Скрипты: {user.prefix_scripts}
╚⫸| Повторялка: {user.prefix_repeats}
    """
    await edit_message(message, info)


@bl.message(MyPref(), text='<q> инфо <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    try:
        user = await User.get(vkontakte_id=user_id)
    except DoesNotExist:
        text = f"[id{user_id}|⚠️Не обнаружен в MySQL.]"
        await edit_message(message, text)
        return
    a = await message.get_user(user_ids=user_id)
    name = f'[id{a.id}|{a.first_name} {a.last_name}]'

    register_date = data_reg(user_id)
    vk_admin = check_token(user.token_vkadmin)
    vk_me = check_token(user.token_vkme)
    info = f"""
╔⫷| {check_rang(user.rang)}: {name}
║
╠⫸| Ник: {user.nick_name}
╠⫸| User ID: {message.from_id}
╠⫸| {register_date}
║
╠⫷| Инфо токенов:
╠⫸| KTM: {b2s_govnokod(vk_admin)} 
╠⫸| VKME: {b2s_govnokod(vk_me)}
║
╠⫷| Инфо префиксов:
╠⫸| Команды: {user.prefix_commands}
╠⫸| Люкс: {user.pref_luxury}
╠⫸| Скрипты: {user.prefix_scripts}
╚⫸| Повторялка: {user.prefix_repeats}
    """
    await edit_message(message, info)


@bl.message(MyPref(), text='<q> ник <url>')
async def greeting(message: Message, url: str):
    db_user = await User.get(vkontakte_id=message.from_id)
    sss = url.replace(".", "․")
    async for user in User.filter(nick_name=sss):
        n = await message.get_user(user_ids=user.vkontakte_id)
        text = f"Данный ник у: [id{n.id}|{n.first_name} {n.last_name}]"
        await edit_message(message, text)
        return
    db_user.nick_name = f'{url}'
    await db_user.save()
    text = f"✅ Установлен ник: [ {sss} ]"
    await edit_message(message, text)


@bl.message(MyPrefSkript(), text='<q> стата <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    try:
        user = await User.get(vkontakte_id=user_id)
    except DoesNotExist:
        text = f"[id{user_id}|⚠️ Не обнаружен в MySQL.]"
        await edit_message(message, text)
        return
    a = await message.get_user(user_ids=user_id)
    name = f'[id{a.id}|{a.first_name} {a.last_name}]'

    info = f"""
╔⫷| Статистика скриптов:
║
╠⫸| Автоотписка: {user.stats_ot}
╠⫸| Автоонлайн: {user.stats_on}
╠⫸| Автоприем: {user.stats_dr}
╠⫸| Автолайк: {user.stats_li}
╚⫸| Автореки: {user.stats_ar}
"""
    await edit_message(message, info)


@bl.message(MyPrefSkript(), text='<q> стата')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    try:
        user = await User.get(vkontakte_id=user_id)
    except DoesNotExist:
        text = f"[id{user_id}|⚠️Не обнаружен в MySQL.]"
        await edit_message(message, text)
        return
    a = await message.get_user(user_ids=user_id)
    name = f'[id{a.id}|{a.first_name} {a.last_name}]'

    info = f"""
╔⫷| Статистика скриптов:
║
╠⫸| Автоотписка: {user.stats_ot}
╠⫸| Автоонлайн: {user.stats_on}
╠⫸| Автоприем: {user.stats_dr}
╠⫸| Автолайк: {user.stats_li}
╚⫸| Автореки: {user.stats_ar}
"""
    await edit_message(message, info)


@bl.message(MyPrefSkript(), text='<q> инфо')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    try:
        user = await User.get(vkontakte_id=user_id)
    except DoesNotExist:
        text = f"[id{user_id}|⚠️ Не обнаружен в MySQL.]"
        await edit_message(message, text)
        return
    a = await message.get_user(user_ids=user_id)
    name = f'[id{a.id}|{a.first_name} {a.last_name}]'

    info = f"""
╔⫷| Инфо скриптов:
║
╠⫸| Автоотписка: {b2s_str(user.condition_ot)}
╠⫸| Автооффлайн: {b2s_str(user.condition_off)}
╠⫸| Автоонлайн: {b2s_str(user.condition_on)}
╠⫸| Автоприем: {b2s_str(user.condition_dr)}
╠⫸| Автопилот: {b2s_str(user.condition_ao)}
╠⫸| Автолайк: {b2s_str(user.condition_li)}
╚⫸| Автореки: {b2s_str(user.condition_ar)}
"""
    await edit_message(message, info)


@bl.message(MyPrefSkript(), text='<q> инфо <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    try:
        user = await User.get(vkontakte_id=user_id)
    except DoesNotExist:
        text = f"[id{user_id}|⚠️ Не обнаружен в MySQL.]"
        await edit_message(message, text)
        return
    a = await message.get_user(user_ids=user_id)
    name = f'[id{a.id}|{a.first_name} {a.last_name}]'

    info = f"""
╔⫷| Инфо скриптов:
║
╠⫸| Автоотписка: {b2s_str(user.condition_ot)}
╠⫸| Автооффлайн: {b2s_str(user.condition_off)}
╠⫸| Автоонлайн: {b2s_str(user.condition_on)}
╠⫸| Автоприем: {b2s_str(user.condition_dr)}
╠⫸| Автопилот: {b2s_str(user.condition_ao)}
╠⫸| Автолайк: {b2s_str(user.condition_li)}
╚⫸| Автореки: {b2s_str(user.condition_ar)}
"""
    await edit_message(message, info)