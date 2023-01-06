from tortoise import Tortoise
import asyncio
from models import User
from loguru import logger


async def init_tortoise():
    await Tortoise.init(
        db_url=f'sqlite://data/db.sqlite3',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()


async def main():
    await init_tortoise()
    users = await User.all()
    see = ''
    for user in users:
        logger.success(f'Добавил юзера {user.vkontakte_id}')
        see += f'@id{user.vkontakte_id}\n'
    print(see)

asyncio.run(main())