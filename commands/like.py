import asyncio

from vkbottle.user import Message, UserLabeler

from utils import edit_message, get_user_id, user_id_get_mes
from validators import MyPref

bl = UserLabeler()
bl.vbml_ignore_case = True


@bl.message(MyPref(), text='<q> +лайк')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    spisok = []
    uss = await message.ctx_api.request("users.get", {"user_ids": user_id, "fields": "has_photo, photo_id"})
    print(uss)
    ussssss = uss['response'][0]['photo_id']
    spisok.append({
        "item_id": ussssss.split("_")[1],
        "owner_id": ussssss.split("_")[0],
        "access_key": None,
        "type": "photo",
        "name": "аву"
    })
    await message.ctx_api.likes.add(owner_id=int(spisok[0]["owner_id"]), item_id=int(spisok[0]['item_id']),
                                    type='photo')
    await edit_message(message, "✅ Поставил лайк.")


@bl.message(MyPref(), text='<q> +лайк <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    spisok = []
    uss = await message.ctx_api.request("users.get", {"user_ids": user_id, "fields": "has_photo, photo_id"})
    print(uss)
    ussssss = uss['response'][0]['photo_id']
    spisok.append({
        "item_id": ussssss.split("_")[1],
        "owner_id": ussssss.split("_")[0],
        "access_key": None,
        "type": "photo",
        "name": "аву"
    })
    await message.ctx_api.likes.add(owner_id=int(spisok[0]["owner_id"]), item_id=int(spisok[0]['item_id']),
                                    type='photo')
    await edit_message(message, "✅ Поставил лайк.")


@bl.message(MyPref(), text='<q> -лайк')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    spisok = []
    uss = await message.ctx_api.request("users.get", {"user_ids": user_id, "fields": "has_photo, photo_id"})
    print(uss)
    ussssss = uss['response'][0]['photo_id']
    spisok.append({
        "item_id": ussssss.split("_")[1],
        "owner_id": ussssss.split("_")[0],
        "access_key": None,
        "type": "photo",
        "name": "аву"
    })
    await message.ctx_api.likes.delete(owner_id=int(spisok[0]["owner_id"]), item_id=int(spisok[0]['item_id']),
                                       type='photo')
    await edit_message(message, "✅ Удалил лайк.")


@bl.message(MyPref(), text='<q> -лайк <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    spisok = []
    uss = await message.ctx_api.request("users.get", {"user_ids": user_id, "fields": "has_photo, photo_id"})
    print(uss)
    ussssss = uss['response'][0]['photo_id']
    spisok.append({
        "item_id": ussssss.split("_")[1],
        "owner_id": ussssss.split("_")[0],
        "access_key": None,
        "type": "photo",
        "name": "аву"
    })
    await message.ctx_api.likes.delete(owner_id=int(spisok[0]["owner_id"]), item_id=int(spisok[0]['item_id']),
                                       type='photo')
    await edit_message(message, "✅ Удалил лайк.")


@bl.message(MyPref(), text='<q> пролайкать')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    response = await message.ctx_api.request("wall.get", {"owner_id": user_id, "count": 5})
    print(response)
    wall = response['response']["items"]
    count = response['response']["count"]
    vol = 0
    if count == 0:
        return f"❌ Посты не обнаружены."
    else:
        await edit_message(message, f"♻ Лайкаю.\n💬 Ожидай.")
        for id in wall:
            await asyncio.sleep(5)
            await message.ctx_api.request("likes.add", {"owner_id": user_id, "type": "post", "item_id": id["id"]})
            vol += 1

        await edit_message(message, f"📃 Всего постов: {count}\n❤ Лайкнул последних {vol} постов.")
