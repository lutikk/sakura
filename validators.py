from loguru import logger
from tortoise.exceptions import DoesNotExist
from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

from config import user_id
from models import User


class MyPref(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        ss = ''
        try:
            if not event.from_id == int(user_id):
                return False
            else:

                pref = await User.get(vkontakte_id=event.from_id)
                sq = 0
                for i in pref.prefix_commands.lower():
                    ss += f'{i}'
                    sq +=1
                sqq = 0
                tex = ''
                for ii in event.text.lower():
                    if sqq == sq:
                        break
                    else:
                        tex += f'{ii}'
                        sqq += 1

                if ss in tex.lower():
                    return True
                else:
                    return False
        except DoesNotExist:
            return False
        except Exception as ex:
            logger.error(ex)


class MyPrefSkript(ABCRule[Message]):
    async def check(self, event: Message) -> bool:

        try:
            if not event.from_id == int(user_id):
                return False
            else:

                pref = await User.get(vkontakte_id=event.from_id)
                ss = ''
                sq = 0
                for i in pref.prefix_scripts.lower():
                    ss += f'{i}'
                    sq +=1
                sqq = 0
                tex = ''
                for ii in event.text.lower():
                    if sqq == sq:
                        break
                    else:
                        tex += f'{ii}'
                        sqq += 1

                if ss in tex.lower():
                    return True
                else:
                    return False
        except DoesNotExist:
            return False
        except Exception as ex:
            logger.error(ex)


class MyPrefLuxury(ABCRule[Message]):
    async def check(self, event: Message) -> bool:

        try:
            if not event.from_id == int(user_id):
                return False
            else:

                pref = await User.get(vkontakte_id=event.from_id)
                if pref.pref_luxury == None:
                    pref.pref_luxury = '.л'
                    await pref.save()
                    return False
                ss = ''
                sq = 0
                for i in pref.pref_luxury.lower():
                    ss += f'{i}'
                    sq += 1
                sqq = 0
                tex = ''
                for ii in event.text.lower():
                    if sqq == sq:
                        break
                    else:
                        tex += f'{ii}'
                        sqq += 1
                if ss in event.text.lower():
                    return True
                else:
                    return False
        except DoesNotExist:
            return False
        except Exception as ex:
            logger.error(ex)
            return False


class Dov(ABCRule[Message]):
    async def check(self, event: Message) -> bool:

        try:
            if event.from_id == user_id:
                return False

            pref = await User.get(vkontakte_id=user_id)
            ss = ''
            sq = 0
            for i in pref.prefix_repeats.lower():
                ss += f'{i}'
                sq += 1
            sqq = 0
            tex = ''
            for ii in event.text.lower():
                if sqq == sq:
                    break
                else:
                    tex += f'{ii}'
                    sqq += 1

            if ss in tex.lower() and event.from_id in eval(pref.list_trusted):
                return True
            else:
                return False
        except DoesNotExist:
            return False
        except Exception as ex:
            logger.error(ex)
