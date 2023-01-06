import datetime

from vkbottle.user import Message, UserLabeler

from validators import MyPref

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
bl = UserLabeler()
bl.vbml_ignore_case = True


@bl.message(MyPref(), text=['<q> дд', '<q> дд <count:int>'])
async def greeting(message: Message, count: int = 2):
    ct = count + 1
    await message.ctx_api.execute(DD_SCRIPT % (ct,
                                               message.peer_id,
                                               message.from_id,
                                               int(datetime.datetime.now().timestamp())))
