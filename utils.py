import datetime
import re
from typing import Union, Iterable

import aiohttp
import requests
import vk_api
from bs4 import BeautifulSoup
from vkbottle.user import Message

import config
from config import token
from models import User


def join(data: Union[str, Iterable], separator: str = ",") -> str:
    if isinstance(data, str):
        data = [data]
    if not data:
        return ''
    return separator.join([str(obj) for obj in data])


async def edit_message(
        message: Message,
        text: str = '',
        att: str = ''
):
    return await message.ctx_api.messages.edit(peer_id=message.peer_id, message=text,
                                               message_id=message.id, keep_forward_messages=True,
                                               keep_snippets=True,
                                               dont_parse_links=False,
                                               attachment=att

                                               )


def get_user_id_by_domain(user_domain: str):
    """Поиск ID по домену"""
    vk = vk_api.VkApi(token=token)

    obj = vk.method('utils.resolveScreenName', {"screen_name": user_domain})

    if isinstance(obj, list):
        return
    if obj['type'] == 'user':
        return obj["object_id"]


def get_user_id(text):
    result = []

    regex = r"(?:vk\.com\/(?P<user>[\w\.]+))|(?:\[id(?P<user_id>[\d]+)\|)"

    for user_domain, user_id in re.findall(regex, text):
        if user_domain:
            result.append(get_user_id_by_domain(user_domain))
        if user_id:
            result.append(int(user_id))

    _result = []
    for r in result:
        if r is not None:
            _result.append(r)
    return _result


async def user_id_get_mes(message: Message):
    if message.reply_message == None:
        vk_user = message.from_id

    else:
        vk_user = message.reply_message.from_id
    return vk_user


# ✅✅✅ ДАТА РЕГИСТРАЦИИ
def data_reg(akk_id):
    try:
        response = requests.get(f'https://vk.com/foaf.php?id={akk_id}')
        xml = response.text
        soup = BeautifulSoup(xml, 'lxml')
        created = soup.find('ya:created').get('dc:date')
        dates = created.split("T")[0].split("-")
        times = created.split("T", maxsplit=1)[1].split("+", maxsplit=1)[0]
        created = f"""{dates[2]}-{dates[1]}-{dates[0]} | {times}"""
        return f"Дата регистрации: {created}."
    except Exception as error:
        return f"⚠ Ошибка выполнения.\n⚙ Информация об ошибке:\n{error}"


def steps(vk_me):
    try:
        token = vk_me
        user_agent = "VKAndroidApp/7.7-10445 (Android 11; SDK 30; arm64-v8a; Xiaomi M2003J15SC; ru; 2340x1080)"
        url = "https://api.vk.com/method/vkRun.setSteps?"
        steps = "steps=80000&"
        distance = "distance=50000&"
        date = f"date={datetime.time().strftime('%Y-%m-%d')}&"
        access_token = f"access_token={token}&"
        requests.post(f'{url}{steps}{distance}{date}{access_token}v=5.131',
                      headers={'User-Agent': user_agent})
        return f"✅ Добавлено: 80000 шагов и 50000 метров"
    except Exception as ex:
        return f'Ошибка: {ex}'


async def tokenvkme(login: str, password: str, us_id: int):
    user = await User.get(vkontakte_id=us_id)
    try:
        try:

            response = requests.post(f'https://oauth.vk.com/token', params={
                'grant_type': 'password',
                'client_id': '2274003',
                'client_secret': 'hHbZxrka2uZ6jB1inYsH',
                'username': login,
                'password': password,
                'v': '5.131',
                '2fa_supported': '1',
                'force_sms': '1' if False else '0',
                'code': None if False else None
            }).json()
            token = response["access_token"]

        except Exception as error:
            return f"╔⫷⚠ Ошибка.\n╠⫸⚙ Повторите попытку.\n╠⫸🔱 Пример:\n╠⫸.к vk_me\n╠⫸79950981374\n╠⫸цербер000\n╠⫸🔐 Токен не активирован\n╚⫸🚫 Ошибка: {error}"
        else:
            user_id = vk_api.VkApi(token=token).method("users.get")[0]['id']
            if user_id == us_id:

                user.token_vkme = token
                await user.save()
                return "✅ «SKRLP Module» Token SKR updated."

            else:
                return "⚠ Используй свой логин и пароль"
    except Exception as error:
        return f"⚠ Ошибка выполнения.\n⚙ Информация об ошибке:\n{error}"


def check_rang(rang):
    'вроде как основные ранги'
    if rang == 1:
        return "Пользователь"
    elif rang == 2:
        return "Агент"
    elif rang == 3:
        return "Админ"
    elif rang == 4:
        return "Владелец"


def check_token(token):
    try:
        vks = vk_api.VkApi(token=token)
        vks._auth_token()
        owner_info = vks.method("account.getProfileInfo")
    except Exception as error:
        return 2
    else:
        return 1


def b2s(value: bool) -> str:
    'как должно быть'
    if value is None:
        return "N/A"
    return "✅" if value else "🚫"


def b2s_govnokod(value: int):
    'как у тебя'
    if value is None:
        return "N/A"

    return '✅' if value == 1 else "🚫"


def b2s_str(value: str):
    'как у тебя'
    if value is None:
        return "N/A"

    return "🚫" if value == 'off' else '✅'


def get_group_id_by_domain(user_domain: str):
    """Поиск ID по домену"""
    vk = vk_api.VkApi(token=token)

    obj = vk.method('utils.resolveScreenName', {"screen_name": user_domain})

    if isinstance(obj, list):
        return
    if obj['type'] in ('group', 'page',):
        return obj["object_id"]


def search_group_ids(text: str):
    result = []

    regex = r"(?:vk\.com\/(?P<group>[\w\.]+))|(?:\[club(?P<group_id>[\d]+)\|)"

    for group_domain, group_id in re.findall(regex, text):
        if group_domain:
            result.append(get_group_id_by_domain(group_domain))
        if group_id:
            result.append(int(group_id))

    _result = []
    for r in result:
        if r is not None:
            _result.append(abs(r))
    return _result


async def send_request(request_data: dict, mes: Message):
    message = ""
    async with aiohttp.ClientSession(headers={"User-Agent": config.APP_USER_AGENT},
                                     connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.post(config.CALLBACK_LINK(), json=request_data) as resp:
            if resp.status != 200:
                message = f"⚠ Ошибка сервера Luxury Multi. Сервер, ответил кодом {resp.status}."
            else:
                data_json = await resp.json()
                if data_json['response'] == 'ok':
                    return
                elif data_json['response'] == "error":
                    if data_json.get('error_code') == 1:
                        message = f"⚠ Ошибка сервера Luxury Multi. Сервер, ответил: <<Пустой запрос>>"
                    elif data_json.get('error_code') == 2:
                        message = f"⚠ Ошибка сервера Luxury Multi. Сервер, ответил: <<Неизвестный тип сигнала>>"
                    elif data_json.get('error_code') == 3:
                        message = (
                            f"⚠ Ошибка сервера Luxury Multi. "
                            f"Сервер, ответил: <<Пара пользователь/секрет не найдены>>"
                        )
                    elif data_json.get('error_code') == 4:
                        message = f"⚠ Ошибка сервера Luxury Multi. Сервер, ответил: <<Беседа не привязана>>"
                    elif data_json.get('error_code') == 10:
                        message = f"⚠ Ошибка сервера Luxury Multi. Сервер, ответил: <<Не удалось связать беседу>>"
                    else:
                        message = (
                            f"⚠ Ошибка сервера Luxury Multi. "
                            f"Сервер, ответил: <<Ошибка #{data_json.get('error_code')}>>"
                        )
                elif data_json['response'] == "vk_error":
                    message = (
                        f"⚠ Ошибка сервера Luxury Multi. "
                        f"Сервер, ответил: "
                        f"<<Ошибка VK #{data_json.get('error_code')} {data_json.get('error_message', '')}>>"
                    )
    if message:
        await mes.ctx_api.messages.edit(peer_id=mes.peer_id, message=message,
                                        message_id=mes.id, keep_forward_messages=True,
                                        keep_snippets=True,
                                        dont_parse_links=False

                                        )


async def get_code(token):
    APP_USER_AGENT = f"IDMLP({config.lux_id};{config.key_lux})"
    qq = requests.post(url=config.GET_LP_INFO_LINK(), headers={"User-Agent": APP_USER_AGENT},
                       json={'access_token': token})

    return qq


async def tokens_lux(tk_1, tk_2):
    APP_USER_AGENT = f"IDMLP({config.lux_id};{config.key_lux})"
    qq = requests.post(url='https://luxuryduty.ru/api/dutys/refresh_tokens/', headers={"User-Agent": APP_USER_AGENT},
                       json={'token': tk_1, 'token_me': tk_2})
    return qq


async def yved(name: str, rang: int, name_admin: str):
    vk = vk_api.VkApi(token=config.gp_token)
    msg = f'{name_admin} назначил {check_rang(rang)} {name}'
    vk.method("messages.send",
              {"peer_id": config.admin_id, "message": msg, "random_id": 0})
