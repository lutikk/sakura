from io import BytesIO

import requests
from PIL import Image, ImageEnhance
from vk_api import VkUpload
from vkbottle.user import Message, UserLabeler

from config import vk
from models import User
from utils import edit_message
from validators import MyPref

bl = UserLabeler()
bl.vbml_ignore_case = True


@bl.message(MyPref(), text=['<q> !префиксы', '<q> префиксы'])
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    text = f'Префиксы:\n\n' \
           f'Команды: {user.prefix_commands}\n' \
           f'Скрипты: {user.prefix_scripts}\n' \
           f'Люкс: {user.pref_luxury}\n' \
           f'Повторялка: {user.prefix_repeats}'
    await edit_message(message, text)


@bl.message(MyPref(), text='<q> !префикс команды <pref>')
async def greeting(message: Message, pref: str):
    user = await User.get(vkontakte_id=message.from_id)
    user.prefix_commands = pref
    await user.save()
    text = '✅ Префикс успешно обновлен.'
    await edit_message(message, text)


@bl.message(MyPref(), text='<q> !префикс люкс <pref>')
async def greeting(message: Message, pref: str):
    user = await User.get(vkontakte_id=message.from_id)
    user.pref_luxury = pref
    await user.save()
    text = '✅ Префикс успешно обновлен.'
    await edit_message(message, text)


@bl.message(MyPref(), text='<q> !префикс скрипты <pref>')
async def greeting(message: Message, pref: str):
    user = await User.get(vkontakte_id=message.from_id)
    user.prefix_scripts = pref
    await user.save()
    text = '✅ Префикс успешно обновлен.'
    await edit_message(message, text)


@bl.message(MyPref(), text='<q> !префикс повторялка <pref>')
async def greeting(message: Message, pref: str):
    user = await User.get(vkontakte_id=message.from_id)
    user.prefix_repeats = pref
    await user.save()
    text = '✅ Префикс успешно обновлен.'
    await edit_message(message, text)


@bl.message(MyPref(), text='<q> линии')
async def greeting(message: Message):
    print(message)

    if not message.attachments:
        await edit_message(message, '💢 Фотография не обнаружена.')
        return

    photo = BytesIO(requests.get(message.attachments[0].photo.sizes[-1].url).content)
    width = 1000
    img = Image.open(photo)
    lines = Image.open('watermark.png')
    ratio = (width / float(img.size[0]))
    height = int((float(img.size[1]) * float(ratio)))
    img = img.resize((width, height), Image.ANTIALIAS)
    img.paste(lines, (0, 0), lines)
    img = ImageEnhance.Brightness(img)
    img = img.enhance(1.5)
    image_handle = BytesIO()
    img.save(image_handle, "PNG")
    image_handle.seek(0)
    upload = VkUpload(vk)
    photo_vk = upload.photo_messages(image_handle, peer_id=message.peer_id)
    atts = "photo{}_{}_{}".format(photo_vk[0]["owner_id"], photo_vk[0]["id"], photo_vk[0]["access_key"])
    await edit_message(message, text="✅ Обработал фоточку.\nДержи.", att=atts)
    img.close()
    lines.close()
