import requests
import vk_api

BASE_DOMAIN = 'https://luxuryduty.ru'


def CALLBACK_LINK():
    return f"{BASE_DOMAIN}/callback/"


def GET_LP_INFO_LINK():
    return f"{BASE_DOMAIN}/api/dutys/get_lp_info/"


key_lux = ''
lux_id = 8

APP_USER_AGENT = f"IDMLP({lux_id};{key_lux})"




def send_request(request_data: dict):
    'Сам код сигнала который принимает только модельку'
    message = ""
    xyi = requests.session()
    xyi.headers.update({"User-Agent": APP_USER_AGENT})
    resp = xyi.post(CALLBACK_LINK(), json=request_data)


    if resp.status_code != 200:
        message = f"⚠ Ошибка сервера Luxury. Сервер, ответил кодом {resp.status_code}."
    else:
        data_json = resp.json()
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
        pass  # если есть сообщение то выполнится этот код но как это юзать решать тока тебе


def get_code(token):
    "получение секретного кода по токену"
    APP_USER_AGENT = f"IDMLP({lux_id};{key_lux})"
    qq = requests.post(url=GET_LP_INFO_LINK(), headers={"User-Agent": APP_USER_AGENT},
                       json={'access_token': token})

    return qq


def tokens_lux(tk_1, tk_2):
    'Обновление токенов (принимает vk_me и кейт)'
    APP_USER_AGENT = f"IDMLP({lux_id};{key_lux})"
    qq = requests.post(url='https://luxuryduty.ru/api/dutys/refresh_tokens/', headers={"User-Agent": APP_USER_AGENT},
                       json={'token': tk_1, 'token_me': tk_2})
    return qq

token = ''
vk = vk_api.VkApi(token=token)


message_ = vk.method("messages.getByConversationMessageId",
                         {"conversation_message_ids": 4637,
                          'peer_id': 572033978})
print(message_)

mes = message_['items'][0]
secret_code = "блятьчтонибудьнарусском"

__model = {
    "user_id": mes['from_id'],
    "method": "lpSendMySignal",
    "secret": secret_code,
    "message": {
        "conversation_message_id": mes['conversation_message_id'],
        "from_id": mes['from_id'],
        "date": mes['date'],
        "text": 'преф' + ' ' + "тут текст команды без префикса",
        "peer_id": mes['peer_id']
    },
    "object": {
        "chat": None,
        "from_id": mes['from_id'],
        "value": 'сакура' + ' ' + "тут текст команды без префикса",
        "conversation_message_id": mes['conversation_message_id']
    },
    "vkmessage": message_['items'][0]
}

