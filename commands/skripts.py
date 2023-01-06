from vkbottle.user import Message, UserLabeler

from models import User
from utils import edit_message
from validators import MyPrefSkript

bl = UserLabeler()

bl.vbml_ignore_case = True


@bl.message(MyPrefSkript(), text='<q> +пилот')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_ao == 'on':
        await edit_message(message, "[Автопилот]\nУже запущен")
        return
    else:
        user.condition_ao = 'on'
        await user.save()
        await edit_message(message, '[Автопилот]\nУспешно включен.')


@bl.message(MyPrefSkript(), text='<q> -пилот')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_ao == 'off':
        await edit_message(message, "[Автопилот]\nНе запущен.")
        return
    else:
        user.condition_ao = 'off'
        await user.save()
        await edit_message(message, f"[Автопилот]\nУспешно выключен.")


@bl.message(MyPrefSkript(), text='<q> +вч')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_on == 'on':
        await edit_message(message, f"[Автоонлайн]\nУже запущен.")
        return
    else:
        user.condition_on = 'on'
        await user.save()
        await edit_message(message, f"[Автоонлайн]\nУспешно включен.")


@bl.message(MyPrefSkript(), text='<q> -вч')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_on == 'off':
        await edit_message(message, f"[Автоонлайн]\nНе запущен.")
        return
    else:
        user.condition_on = 'off'
        await user.save()
        await edit_message(message, f"[Автоонлайн]\nУспешно выключен.")


@bl.message(MyPrefSkript(), text='<q> +ффлайн')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_off == 'on':
        await edit_message(message, f"[Автооффлайн]\nУже запущен.")
        return
    else:
        user.condition_off = 'on'
        await user.save()
        await edit_message(message, f"[Автооффлайн]\nУспешно включен.")


@bl.message(MyPrefSkript(), text='<q> -оффлайн')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_off == 'off':
        await edit_message(message, f"[Автооффлайн]\nНе запущен.")
        return
    else:
        user.condition_off = 'off'
        await user.save()
        await edit_message(message, f"[Автооффлайн]\nУспешно выключен.")


@bl.message(MyPrefSkript(), text='<q> +увед')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_uv == 'on':
        await edit_message(message, "[Автоувед]\nУже запущен.")
        return
    else:
        sq = await message.ctx_api.request("wall.get", {"count": 1, "owner_id": message.from_id})

        if sq['response']['count'] == 0:
            await edit_message(message, f"Пост не обнаружен")
            return
        else:
            user.condition_uv = 'on'
            await user.save()
            await edit_message(message, "[Автоувед]\nУспешно запущен.")


@bl.message(MyPrefSkript(), text='<q> -увед')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_uv == 'off':
        await edit_message(message, f"[Автоувед]\nНе запущен.")
        return
    else:
        user.condition_uv = 'off'
        await user.save()
        await edit_message(message, f"[Автоувед]\nУспешно выключен.")


@bl.message(MyPrefSkript(), text='<q> +др')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_dr == 'on':
        await edit_message(message, f"[Автоприем]\nУспешно запущен")
        return
    else:
        user.condition_dr = 'on'
        await user.save()
        await edit_message(message, "[Автоприем]\nУспешно включен.")


@bl.message(MyPrefSkript(), text='<q> -др')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_dr == 'off':
        await edit_message(message, f"[Автоприем]\nНе запущен.")
        return
    else:
        user.condition_dr = 'off'
        await user.save()
        await edit_message(message, f"⚙[Автоприем]\nУспешно выключен.")


@bl.message(MyPrefSkript(), text='<q> +лайк')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_li == 'on':
        await edit_message(message, f"[Автолайк]\nУже запущен.")
        return
    else:
        user.condition_li = 'on'
        await user.save()
        await edit_message(message, "[Автолайк]\nУспешно включен.")


@bl.message(MyPrefSkript(), text='<q> -лайк')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_li == 'off':
        await edit_message(message, f"[Автолайк]\nНе запущен.")
        return
    else:
        user.condition_li = 'off'
        await user.save()
        await edit_message(message, f"[Автолайк]\nУспешно выключен.")


@bl.message(MyPrefSkript(), text='<q> +ферма')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_fm == 'on':
        await edit_message(message, f"[Автоферма]\nУже запущен.")
        return
    else:
        user.condition_fm = 'on'
        await user.save()
        await edit_message(message, "[Автоферма]\nУспешно включен.")


@bl.message(MyPrefSkript(), text='<q> -ферма')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_fm == 'off':
        await edit_message(message, f"[Автоферма]\nНе запущен.")
        return
    else:
        user.condition_fm = 'off'
        await user.save()
        await edit_message(message, f"[Автоферма]\nУспешно выключен.")


@bl.message(MyPrefSkript(), text='<q> +рек')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_ar == 'on':
        await edit_message(message, f"[Авторекомендации]\nУже запущен.")
        return
    else:
        user.condition_ar = 'on'
        await user.save()
        await edit_message(message, f"[Авторекомендации]\nУспешно включен.")


@bl.message(MyPrefSkript(), text='<q> -рек')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_ar == 'off':
        await edit_message(message, f"[Авторекомендации]\nНе запущен.")
        return
    else:
        user.condition_ar = 'off'
        await user.save()
        await edit_message(message, "[Авторекомендации]\nУспешно выключен.")


@bl.message(MyPrefSkript(), text='<q> +отп')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_ot == 'on':
        await edit_message(message, f"[Автоотписка]\nУже запущен.")
        return
    else:
        user.condition_ot = 'on'
        await user.save()
        await edit_message(message, f"[Автоотписка]\nУспешно включен.")


@bl.message(MyPrefSkript(), text='<q> -отп')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_ot == 'off':
        await edit_message(message, f"[Автоотписка]\nНе запущен.")
        return
    else:
        user.condition_ot = 'off'
        await user.save()
        await edit_message(message, f"[Автоотписка]\nУспешно выключен.")


@bl.message(MyPrefSkript(), text='<q> +оффлайн')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_off == 'on':
        await edit_message(message, f"[Невидимка]\nУже запущена")
        return
    else:
        user.condition_off = 'on'
        await user.save()
        await edit_message(message, f"[Невидимка]\nУспешно включена")


@bl.message(MyPrefSkript(), text='<q> -оффлайн')
async def greeting(message: Message):
    user = await User.get(vkontakte_id=message.from_id)
    if user.condition_off == 'off':
        await edit_message(message, f"[Невидимка]\nНе запущена")
        return
    else:
        user.condition_off = 'on'
        await user.save()
        await edit_message(message, f"[Невидимка]\nУспешно выключена")
