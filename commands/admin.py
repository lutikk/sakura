from tortoise.exceptions import DoesNotExist
import os 
from vkbottle.user import Message, UserLabeler

import config
from models import User, Referals
from utils import edit_message, get_user_id, user_id_get_mes, yved
from validators import MyPref


bl = UserLabeler()

bl.vbml_ignore_case = True


@bl.message(MyPref(), text='<q> !setagent')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    if user_id == message.from_id:
        await edit_message(message, 'Самоотсос это конечно прекрасно но мб выберешь кого-нибудь на эту роль?')
        return
    admin_db = await User.get(vkontakte_id=message.from_id)
    if not admin_db.rang >= 3:
        return
    else:
        agent_id = await User.get(vkontakte_id=user_id)
        agent_id.rang = 2
        await agent_id.save()
        a = await message.get_user(user_ids=user_id)
        name = f'[id{a.id}|{a.first_name} {a.last_name}]'
        adm = await message.get_user(user_ids=message.from_id)
        name_admin = f'[id{adm.id}|{adm.first_name} {adm.last_name}]'
        await edit_message(message, "✅ Выдан ранг: Агент")
        await yved(name=name, rang=2, name_admin=name_admin)


@bl.message(MyPref(), text='<q> !setadmin')
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    if user_id == message.from_id:
        await edit_message(message, 'Самоотсос это конечно прекрасно но мб выберешь кого-нибудь на эту роль?')
        return
    admin_db = await User.get(vkontakte_id=message.from_id)
    if not admin_db.rang >= 3:
        return
    else:
        agent_id = await User.get(vkontakte_id=user_id)
        agent_id.rang = 3
        await agent_id.save()
        a = await message.get_user(user_ids=user_id)
        name = f'[id{a.id}|{a.first_name} {a.last_name}]'
        adm = await message.get_user(user_ids=message.from_id)
        name_admin = f'[id{adm.id}|{adm.first_name} {adm.last_name}]'
        await edit_message(message, "✅ Выдан ранг: Админ")
        await yved(name=name, rang=3, name_admin=name_admin)


@bl.message(MyPref(), text=['<q> !unsetagent', "<q> !unsetadmin"])
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    if user_id == message.from_id:
        await edit_message(message, 'Самоотсос это конечно прекрасно но мб выберешь кого-нибудь на эту роль?')
        return
    admin_db = await User.get(vkontakte_id=message.from_id)
    if not admin_db.rang >= 3:
        return
    else:
        agent_id = await User.get(vkontakte_id=user_id)
        agent_id.rang = 1
        await agent_id.save()
        a = await message.get_user(user_ids=user_id)
        name = f'[id{a.id}|{a.first_name} {a.last_name}]'
        adm = await message.get_user(user_ids=message.from_id)
        name_admin = f'[id{adm.id}|{adm.first_name} {adm.last_name}]'
        await edit_message(message, "🚫 Снят с ранга.")
        await yved(name=name, rang=1, name_admin=name_admin)


@bl.message(MyPref(), text='<q> !setagent <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    if user_id == message.from_id:
        await edit_message(message, 'Самоотсос это конечно прекрасно но мб выберешь кого-нибудь на эту роль?')
        return
    admin_db = await User.get(vkontakte_id=message.from_id)
    if not admin_db.rang >= 3:
        return
    else:
        agent_id = await User.get(vkontakte_id=user_id)
        agent_id.rang = 2
        await agent_id.save()
        a = await message.get_user(user_ids=user_id)
        name = f'[id{a.id}|{a.first_name} {a.last_name}]'
        adm = await message.get_user(user_ids=message.from_id)
        name_admin = f'[id{adm.id}|{adm.first_name} {adm.last_name}]'
        await edit_message(message, "✅ Выдан ранг: Агент")
        await yved(name=name, rang=2, name_admin=name_admin)


@bl.message(MyPref(), text='<q> !setadmin <url>')
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    if user_id == message.from_id:
        await edit_message(message, 'Самоотсос это конечно прекрасно но мб выберешь кого-нибудь на эту роль?')
        return
    admin_db = await User.get(vkontakte_id=message.from_id)
    if not admin_db.rang >= 3:
        return
    else:
        agent_id = await User.get(vkontakte_id=user_id)
        agent_id.rang = 3
        await agent_id.save()
        a = await message.get_user(user_ids=user_id)
        name = f'[id{a.id}|{a.first_name} {a.last_name}]'
        adm = await message.get_user(user_ids=message.from_id)
        name_admin = f'[id{adm.id}|{adm.first_name} {adm.last_name}]'
        await edit_message(message, "✅ Выдан ранг: Админ")
        await yved(name=name, rang=3, name_admin=name_admin)


@bl.message(MyPref(), text=['<q> !unsetagent <url>', "<q> !unsetadmin <url>"])
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    if user_id == message.from_id:
        await edit_message(message, 'Самоотсос это конечно прекрасно но мб выберешь кого-нибудь на эту роль?')
        return
    admin_db = await User.get(vkontakte_id=message.from_id)
    if not admin_db.rang >= 3:
        return
    else:
        agent_id = await User.get(vkontakte_id=user_id)
        agent_id.rang = 1
        await agent_id.save()
        a = await message.get_user(user_ids=user_id)
        name = f'[id{a.id}|{a.first_name} {a.last_name}]'
        adm = await message.get_user(user_ids=message.from_id)
        name_admin = f'[id{adm.id}|{adm.first_name} {adm.last_name}]'
        await edit_message(message, "✅ Выдан ранг: Пользователя")
        await yved(name=name, rang=1, name_admin=name_admin)




@bl.message(MyPref(), text=['<q> !рег'])
async def greeting(message: Message):
    user_id = await user_id_get_mes(message)
    admin_db = await User.get(vkontakte_id=message.from_id)
    if admin_db.rang >= 2:
        try:
            await User.get(vkontakte_id=user_id)
            await edit_message(message, f'✅ @id{user_id}(Уже есть в MySQL.)')
        except DoesNotExist:
            await User.get_or_new(vkontakte_id=user_id)
            admin_db.referral += 1
            await admin_db.save()
            await Referals.get_or_new_ref(user_id=user_id, reg_id=message.from_id)
            await edit_message(message, f'✅ @id{user_id}(«YoRHa | LP» Session created.)')
    else:
        return


@bl.message(MyPref(), text=['<q> !рег <url>'])
async def greeting(message: Message, url: str):
    user_id = get_user_id(url)[0]
    admin_db = await User.get(vkontakte_id=message.from_id)
    if admin_db.rang >= 2:
        try:
            await User.get(vkontakte_id=user_id)
            await edit_message(message, f'🚫 @id{user_id}(Уже есть в MySQL.)')
        except DoesNotExist:
            await User.get_or_new(vkontakte_id=user_id)
            admin_db.referral +=1
            await admin_db.save()
            await Referals.get_or_new_ref(user_id=user_id, reg_id=message.from_id)
            await edit_message(message, f'✅ @id{user_id}(«YoRHa | LP Module» Session created.)')
    else:
        return


@bl.message(MyPref(), text=['<q> !чек'])
async def greeting(message: Message):
    try:
        user_id = await user_id_get_mes(message)
        ss = await Referals.get(user_id=user_id)
        a = await message.get_user(user_ids=ss.reg_id)
        name = f'[id{a.id}|{a.first_name} {a.last_name}]'
        text = f"👤 Зарегистрирован: {name}"
        await edit_message(message, text)
    except DoesNotExist:
        await edit_message(message, 'Олд')



@bl.message(MyPref(), text=['<q> !чек <url>'])
async def greeting(message: Message, url: str):
    try:
        user_id = get_user_id(url)[0]
        ss = await Referals.get(user_id=user_id)
        a = await message.get_user(user_ids=ss.reg_id)
        name = f'[id{a.id}|{a.first_name} {a.last_name}]'
        text = f"👤 Зарегистрирован: {name}"
        await edit_message(message, text)
    except DoesNotExist:
        await edit_message(message, 'Олд')


