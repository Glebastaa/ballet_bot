import asyncio
from datetime import time

from database.servise import add_studio, add_group, get_groups, edit_group, get_studios
from database.models import WeekDays
from database.db import async_session_maker

tm = time(hour=10, minute=13)


async def test():
    async with async_session_maker() as session:
        result = await edit_group(session, 'chlen', 'anonimnaya grupa huini', 'hui')
        print(result.name)


if __name__ == '__main__':
    asyncio.run(test())
