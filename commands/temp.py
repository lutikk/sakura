from tortoise.exceptions import DoesNotExist
from vkbottle.user import Message, UserLabeler
import datetime
from models import Template
from utils import edit_message
from validators import MyPref

bl = UserLabeler()
bl.vbml_ignore_case = True

DD_SCRIPT = (
    'var i = 0;var msg_ids = [];var count = %d;'
    'var items = API.messages.getHistory({"peer_id":%d,"count":"200", "offset":"0"}).items;'
    'while (count > 0 && i < items.length) {if (items[i].out == 1) {if (items[i].id == %d) {'
    'if (items[i].reply_message) {msg_ids.push(items[i].id);msg_ids.push(items[i].reply_message.id);'
    'count = 0;};if (items[i].fwd_messages) {msg_ids.push(items[i].id);var j = 0;while (j < '
    'items[i].fwd_messages.length) {msg_ids.push(items[i].fwd_messages[j].id);j = j + 1;};count = 0;};};'
    'msg_ids.push(items[i].id);count = count - 1;};if ((%d - items[i].date) > 86400) {count = 0;};i = i + 1;};'
    'API.messages.delete({"message_ids": msg_ids,"delete_for_all":"1"});return count;'
)


@bl.message(MyPref(), text=['<q> шаб <name>', "<q> шаб <name>", "<q> шаб <name>"])
async def greeting(e: Message, name: str):
    try:
        temp = await Template.get(name=name, vkontakte_id=e.from_id)
        if temp.attachment != None:
            try:
                await edit_message(message=e, text=temp.message, att=eval(temp.attachment))
            except:
                await e.ctx_api.execute(DD_SCRIPT % (1,
                                                           e.peer_id,
                                                           e.from_id,
                                                           int(datetime.datetime.now().timestamp())))
                await e.answer(message=temp.message, attachment=eval(temp.attachment))
            return
        else:
            await edit_message(message=e, text=temp.message)
            return
    except DoesNotExist:
        text = f'🚫 Шаблон «{name}» не найден.'
        await edit_message(e, text)
        return


@bl.message(MyPref(), text=['<q> +шаб <name>\n<text>', "<q> +шаб <name>\n <text>", "<q> +шаб <name>"])
async def greeting(e: Message, name: str, text: str = ''):
    ss = []
    payload = e.reply_message.text if e.reply_message else text
    attachments = e.reply_message.attachments if e.reply_message else e.attachments

    if not payload and not attachments:
        await edit_message(e, text='⚠ Для создания шаблона необходим текст или вложение')
        return

    try:
        await Template.get(vkontakte_id=e.from_id, name=name)
        await edit_message(e, text=f'⚠ Шаблон <<{name}>> уже существует')
        return
    except DoesNotExist:
        pass
    if not attachments:
        template = await Template.get_or_new_temp(
            vkontakte_id=e.from_id,
            name=name,
            message=payload
        )
    else:

        for att in attachments:
            if att.photo != None:
                if att.photo.access_key == None:
                    ss.append(f'photo{att.photo.owner_id}_{att.photo.id}')
                else:
                    ss.append(f'photo{att.photo.owner_id}_{att.photo.id}_{att.photo.access_key}')
            elif att.graffiti != None:
                if att.graffiti.access_key == None:
                    ss.append(f'graffiti{att.graffiti.owner_id}_{att.graffiti.id}')
                else:
                    ss.append(f'graffiti{att.graffiti.owner_id}_{att.graffiti.id}_{att.graffiti.access_key}')
            elif att.audio_message != None:
                if att.audio_message.access_key == None:
                    ss.append(f'audio_message{att.audio_message.owner_id}_{att.audio_message.id}')
                else:
                    ss.append(
                        f'audio_message{att.audio_message.owner_id}_{att.audio_message.id}_{att.audio_message.access_key}')
            elif att.video != None:
                if att.video.access_key == None:
                    ss.append(f'video{att.video.owner_id}_{att.video.id}')
                else:
                    ss.append(f'video{att.video.owner_id}_{att.video.id}_{att.video.access_key}')

            elif att.audio != None:
                if att.audio.access_key == None:
                    ss.append(f'audio{att.audio.owner_id}_{att.audio.id}')
                else:
                    ss.append(f'audio{att.audio.owner_id}_{att.audio.id}_{att.audio.access_key}')
            elif att.doc != None:
                if att.doc.access_key == None:
                    ss.append(f'doc{att.doc.owner_id}_{att.doc.id}')
                else:
                    ss.append(f'doc{att.doc.owner_id}_{att.doc.id}_{att.doc.access_key}')

        template = await Template.get_or_new_temp(
            vkontakte_id=e.from_id,
            name=name,
            message=payload,
            attachment=ss
        )

    print(ss)
    print(text)
    message = f'✅ Создан шаблон: «{name}».\n'

    await edit_message(e, text=message)
    return


@bl.message(MyPref(), text=['<q> шабы все', "<q> шабы все", "<q> шабы все"])
async def greeting(e: Message):
    t = '⛓ Ваши шаблоны:\n'
    temp = await Template.filter(vkontakte_id=e.from_id)
    if len(temp) == 0:
        await edit_message(e, "🚫 Список шаблонов пуст.")
        return
    else:
        for ss in temp:
            t += f'{ss.name}\n'
        await edit_message(e, t)
        return


@bl.message(MyPref(), text=['<q> -шаб <name>', "<q> -шаб <name>"])
async def greeting(e: Message, name: str):
    tem = await Template.filter(name=name, vkontakte_id=e.from_id).delete()
    text = f'✅ Удален шаблон: «{name}»'
    await edit_message(e, text)
