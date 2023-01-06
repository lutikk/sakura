from io import BytesIO

import requests
import vk_api
from gtts import gTTS
from vk_api import VkUpload
from vkbottle.user import Message, UserLabeler

from models import User
from utils import edit_message, user_id_get_mes, get_user_id
from validators import MyPref

bl = UserLabeler()
bl.vbml_ignore_case = True


@bl.message(MyPref(), text=['<q> озвучь\n<text>', '<q> озвучь \n<text>'])
async def greetingh(message: Message, text: str):
    users = await User.get(vkontakte_id=message.from_id)
    print(text)
    try:

        vk = vk_api.VkApi(users.token_vkadmin)
        bytes_io = BytesIO()
        tts = gTTS(text, lang='ru')
        tts.write_to_fp(bytes_io)
        bytes_io.name = 'voice_message.mp3'
        bytes_io.seek(0)
        upload = VkUpload(vk)
        uploads = upload.document(bytes_io, doc_type='audio_message', title='voice_message.mp3',
                                  message_peer_id=message.peer_id)
        atts = "audio_message{}_{}_{}".format(uploads["audio_message"]["owner_id"], uploads["audio_message"]["id"],
                                              uploads["audio_message"]["access_key"])
        await edit_message(message=message, att=atts)
    except Exception as error:
        return f"⚠ Ошибка выполнения.\n⚙ Информация об ошибке:\n{error}"


async def set_ava(message: Message, token, user_id):
    vks = vk_api.VkApi(token)
    vk = vks.get_api()
    upload = VkUpload(vks)
    responce = vk.method("messages.getByConversationMessageId",
                         {"conversation_message_ids": message.conversation_message_id,
                          'peer_id': message.peer_id})
    print(responce)
    url = None
    if responce.get("reply_message"):
        if len(responce["reply_message"]["attachments"]) != 0:
            if responce["reply_message"]["attachments"][0]["type"] == "photo":
                for types in responce["reply_message"]["attachments"][0]["photo"]["sizes"]:
                    if types["type"] == "w":
                        url = types["url"]
                    elif types["type"] == "z":
                        url = types["url"]
                    elif types["type"] == "y":
                        url = types["url"]
                    else:
                        pass
            else:
                return "⚠ Фотография не обнаружена.\n⚙ Возможно плохое качество изображения."
        else:
            url = vk.method("users.get", {"user_ids": user_id, "fields": "photo_max_orig"})[0]["photo_max_orig"]
    elif len(responce["attachments"]) != 0:
        if responce["attachments"][0].get("photo"):
            for types in responce["attachments"][0]["photo"]["sizes"]:
                if types["type"] == "w":
                    url = types["url"]
                elif types["type"] == "z":
                    url = types["url"]
                elif types["type"] == "y":
                    url = types["url"]
                else:
                    pass
        else:
            return "⚠ Фотография не обнаружена.\n⚙ Возможно плохое качество изображения."
    else:
        return "⚠ Фотография не обнаружена.\n⚙ Возможно плохое качество изображения."
    if url == None:
        return "⚠ Фотография не обнаружена.\n⚙ Возможно плохое качество изображения."
    photo = BytesIO(requests.get(url).content)
    photo_vk = upload.photo_profile(photo)
    return "✅ Новая аватарка установлена."



@bl.message(MyPref(), text='<q> ава')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    token = await User.get(vkontakte_id=message.from_id)
    print(token.token_vkadmin)
    text = await set_ava(message=message, token=token.token_vkadmin, user_id=user_id)
    await edit_message(message, text)


async def send_themes(token, nambe, peer_id):
    vk = vk_api.VkApi(token)
    try:

        num_th = int(nambe)
        if num_th > 11 or num_th < 1:
            return "⚠️ Доступно 11 тем для чата."
        th_list = [0, "marine", "retrowave", "disco", "twilight", "unicorn", "emerald", "crimson", "lagoon", "sunset",
                   "midnight", "candy"]
        try:
            vk.method("messages.setConversationStyle",dict(peer_id=peer_id,
                    style="{}".format(th_list[num_th])))
        except Exception as error:
            return f"💢 Произошла ошибка.\n💬 Информация об ошибке:/n{error}"

    except Exception as error:
        return f"💢 Произошла ошибка.\n💬 Информация об ошибке:/n{error}"


@bl.message(MyPref(), text='<q> тема <n:int>')
async def greeting(message: Message, n: int):
    user_db = await User.get(vkontakte_id=message.from_id)
    text = await send_themes(user_db.token_vkme, n, message.peer_id)
    await edit_message(message, text)


@bl.message(MyPref(), text=['<q> лс\n<text>', '<q> лс\n <text>'])
async def greeting(message: Message, text: str):
    user_id = await user_id_get_mes(message)
    print(user_id)
    await message.ctx_api.request("messages.send", {"peer_id": user_id, "message": text, "random_id": 0})
    tt = '✅ Сообщение отправлено.'
    await edit_message(message, tt)


@bl.message(MyPref(), text=['<q> лс <url>\n<text>', '<q> лс <url>\n <text>'])
async def greeting(message: Message, url: str, text: str):
    user_id = get_user_id(url)[0]
    print(user_id)
    await message.ctx_api.request("messages.send", {"peer_id": user_id, "message": text, "random_id": 0})
    tt = '✅ Сообщение отправлено.'
    await edit_message(message, tt)
