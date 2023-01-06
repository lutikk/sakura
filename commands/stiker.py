import time
import requests
from dev_up import DevUpAPI
from lyricsgenius import Genius
from vkbottle.user import Message, UserLabeler
from models import User
from config import dev_up_key
from utils import edit_message, get_user_id, user_id_get_mes, join
from validators import MyPref

bl = UserLabeler()

bl.vbml_ignore_case = True


async def stik(uid: int, tok: str):
    url = 'https://api.vk.com/method/gifts.getCatalog?v=5.131&user_id={}&access_token={}'.format(uid, tok)
    stickers = requests.get(url, headers={
        "user-agent": "VKAndroidApp/1.123-123 (Android 123; SDK 123; Unuty_lp; 1; ru; 123x123)"}).json()
    stickers = stickers['response']
 
    url_f = 'https://api.vk.com/method/gifts.getCatalog?v=5.131&user_id=627689528&access_token={}'.format(tok)
    stickers_filter = requests.get(url_f, headers={
        "user-agent": "VKAndroidApp/1.123-123 (Android 123; SDK 123; Unuty_lp; 1; ru; 123x123)"}).json()
    stickers_filter = stickers_filter['response'][1]['items'][2:]
 
    sticker_list = [
        f"{i['sticker_pack']['title']}"
        for i in stickers[1]['items']
        if 'disabled' in i
    ]
 
    sum_price_golosa = sum(
        d['price'] for d in stickers_filter if d['sticker_pack']['title'] in sticker_list)
 
    sum_stick_price_golosa = str(sum_price_golosa)  # цена в голосах
    sum_stick_price_rub = str(sum_price_golosa * 7)  # цена в рублях
    count = str(len(sticker_list))  # количество стикер паков
 
    if count == 0:
        out_message = ".\n🥺 Платных стикерпаков у пользователя нет."
        return out_message
    else:
        text = f"💰 Стоимость в голосах: {sum_stick_price_golosa}\n" \
        f"💵 Стоимость в рублях: {sum_stick_price_rub}₽\n\n"
        return text + join(sticker_list, ", ")


@bl.message(MyPref(), text='<q> стикеры')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    user_db = await User.get(vkontakte_id=message.from_id)
    text = await stik(user_id, user_db.token_vkme)
    await edit_message(message, text)


@bl.message(MyPref(), text='<q> стикеры <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)
    user_db = await User.get(vkontakte_id=message.from_id)
    text = await stik(user_id, user_db.token_vkme)
    await edit_message(message, text)


@bl.message(MyPref(), text='<q> слова')
async def greeting(message: Message):
    audio_artist = message.attachments[0].audio.artist
    audio_name = message.attachments[0].audio.title
    print(audio_name)
    print(audio_artist)
    time.sleep(10)

    genius = Genius("74rW7zvIFhxIraIJtNdptQd51D9vw-CumYrn7bIqVSOk3MSqo-DafWR_PFCPUSl8")
    song = genius.search_song(audio_name, audio_artist)
    await edit_message(message=message, text=song.lyrics)
