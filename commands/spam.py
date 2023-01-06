import time

from vkbottle.user import Message, UserLabeler
import time
from models import User
from utils import edit_message, get_user_id, data_reg, user_id_get_mes, steps, tokenvkme
from validators import MyPref

bl = UserLabeler()

bl.vbml_ignore_case = True

async def spamer(mes: Message, count: int, text: str = '', att: str = ''):
    i = 1
    while i <= count:
        await mes.answer(message=text, attachment=att)
        i += 1
        time.sleep(1.5)

@bl.message(MyPref(), text=['<q> спам <count:int>\n<text>',
                            '<q> спам <count:int> \n<text>',
                            '<q> спам <count:int>\n <text>'
                            ])
async def greeting(message: Message, count:int, text: str):
    if not message.attachments:
        await edit_message(message, text)
        await spamer(message, count, text)
    else:
        ss = []
        for att in message.attachments:
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

        await edit_message(message, text, att=ss)
        await spamer(message, count, text, ss)
