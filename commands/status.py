from vkbottle.user import Message, UserLabeler

from utils import edit_message
from validators import MyPref

bl = UserLabeler()

bl.vbml_ignore_case = True


@bl.message(MyPref(), text='<q> статус <text>')
async def greeting(message: Message, text: str):
    await message.ctx_api.status.set(text)
    await edit_message(message, f"✅ Изменил статус на: <<{text}>>")
