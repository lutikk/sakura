import sys

import vk_api
from vk_api import VkApi

token = sys.argv[1]
from tortoise import Tortoise

user_id = VkApi(token=token).method("users.get")[0]['id']

vk = vk_api.VkApi(token=token)
vk._auth_token()

gp_token = ''

admin_id = 645697619

dev_up_key = ''

pat = '/root/data/db.sqlite3'


async def init_tortoise():
    await Tortoise.init(
        db_url=f'sqlite://data/db.sqlite3',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()


BASE_DOMAIN = 'https://luxuryduty.ru'


def CALLBACK_LINK():
    return f"{BASE_DOMAIN}/callback/"


def GET_LP_INFO_LINK():
    return f"{BASE_DOMAIN}/api/dutys/get_lp_info/"


key_lux = 'dinjgokrgjbfkemdlgregerfefefrhyrfefy'
lux_id = 4

APP_USER_AGENT = f"IDMLP({lux_id};{key_lux})"


__model = {
    "user_id": message.from_id,
    "method": "lpSendMySignal",
    "secret": user_db.secret_code,
    "message": {
        "conversation_message_id": message.conversation_message_id,
        "from_id": message.from_id,
        "date": message.date,
        "text": 'йорха' + ' ' + text,
        "peer_id": message.peer_id
    },
    "object": {
        "chat": None,
        "from_id": message.from_id,
        "value": 'сакура' + ' ' + text,
        "conversation_message_id": message.conversation_message_id
    },
    "vkmessage": message_['items'][0]
}

