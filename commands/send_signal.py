import vk_api
from vkbottle.user import Message, UserLabeler

from models import User
from utils import edit_message, send_request, get_code, tokens_lux
from validators import MyPrefLuxury, MyPref

bl = UserLabeler()

bl.vbml_ignore_case = True


@bl.message(MyPrefLuxury(), text='<q> <text>')
async def greeting(message: Message, text: str):
    user_db = await User.get(vkontakte_id=message.from_id)
    vk = vk_api.VkApi(token=user_db.token_vkadmin)
    message_ = vk.method("messages.getByConversationMessageId",
                         {"conversation_message_ids": message.conversation_message_id,
                          'peer_id': message.peer_id})
    print(message_)
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
send_request(__model, message)


@bl.message(MyPref(), text='<q> секретка')
async def greeting(message: Message):
    user_db = await User.get(vkontakte_id=message.from_id)
    lux = await get_code(user_db.token_vkadmin)
    sek = lux.json()['response']['secret_code']
    user_db.secret_code = sek
    await user_db.save()
    await edit_message(message, "✅ Получил секретку для Luxury.")


@bl.message(MyPref(), text='<q> обновить токены')
async def greeting(message: Message):
    user_db = await User.get(vkontakte_id=message.from_id)
    await tokens_lux(user_db.token_vkadmin, user_db.token_vkme)

    await edit_message(message, "✅ Обновил токены в Luxury.")
