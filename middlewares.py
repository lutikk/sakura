from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from config import user_id
from models import User


class UserIgnore(BaseMiddleware[Message]):

    async def pre(self):
        user_db = await User.get(vkontakte_id=user_id)

        if self.event.from_id in eval(user_db.list_ignore) and self.event.from_id != user_id:
            await self.event.ctx_api.request("messages.delete",
                                             {"peer_id": self.event.peer_id, "message_id": self.event.id})
            return False
        else:
            return True


class FiltersIwents(BaseMiddleware[Message]):
    async def pre(self):
        user_db = await User.get(vkontakte_id=user_id)
        spi = eval(user_db.list_trusted)
        if self.event.from_id in spi or self.event.from_id == user_id:
            return True
        else:
            return False