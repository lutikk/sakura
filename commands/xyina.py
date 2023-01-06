"В этот файл я буду записывать всю хуйню которой не могу придумать название"
from threading import Thread

from vkbottle.user import Message, UserLabeler

from utils import edit_message, user_id_get_mes, \
    search_group_ids
from validators import MyPref
from workers.groop import clear_group

bl = UserLabeler()

bl.vbml_ignore_case = True


@bl.message(MyPref(), text='<q> +гп')
async def greeting(message: Message):
    gp_id = await user_id_get_mes(message)

    group = await message.ctx_api.request('groups.join', {'group_id': abs(gp_id)})

    await edit_message(message, f'✅ Вы вступили в группу')


@bl.message(MyPref(), text='<q> +гп <url>')
async def greeting(message: Message, url: str):
    gp_id = search_group_ids(url)[0]
    print(gp_id)
    group = await message.ctx_api.request('groups.join', {'group_id': abs(gp_id)})

    await edit_message(message, f'✅ Вы вступили в группу')


@bl.message(MyPref(), text='<q> -гп')
async def greeting(message: Message):
    gp_id = await user_id_get_mes(message)

    group = await message.ctx_api.request('groups.leave', {'group_id': abs(gp_id)})

    await edit_message(message, f'✅ Вы покинули группу.')


@bl.message(MyPref(), text='<q> -гп <url>')
async def greeting(message: Message, url: str):
    gp_id = search_group_ids(url)[0]
    print(gp_id)
    group = await message.ctx_api.request('groups.leave', {'group_id': abs(gp_id)})

    await edit_message(message, f'✅ Вы покинули группу.')


@bl.message(MyPref(), text='<q> !группы')
async def greeting(message: Message):
    Thread(target=clear_group).start()
    await edit_message(message, f"✅ Чистка Groups запущена.")


