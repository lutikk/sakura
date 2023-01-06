import asyncio

from loguru import logger
from tortoise import Tortoise

from models import User

pat = '/root/data/db.sqlite3'


async def init_tortoise():
    await Tortoise.init(
        db_url=f'sqlite://{pat}',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()


async def main(user_id: int):
    await init_tortoise()
    ss = await User.get_or_new(vkontakte_id=user_id)
    ss.rang = 4
    await ss.save()
    logger.success(f"Зарегистрировал юзера: {user_id} и выдал ему Владельца")


if __name__ in '__main__':
    asyncio.run(main(int(input("Введите ид владельца: "))))
