import asyncio
import asyncpg
import aiohttp
import config
import time
from more_itertools import chunked
from models import get_async_session, save_people_in_db


URL = 'http://swapi.dev/api/people/'
# URL = 'http://swapi.tech/api/people/'

# MAX = 100
MAX = 20
PARTITION = 10
SLEEP_TIME = 1


async def get_person(person_id, session):
    async with session.get(f'{URL}{person_id}') as response:
        return await response.json()


async def get_people(all_ids, partition, session):
    for chunk_ids in chunked(all_ids, partition):
        tasks = [asyncio.create_task(get_person(person_id, session)) for person_id in chunk_ids]
        for task in tasks:
            task_result = await task
            yield task_result


async def main():
    await get_async_session(True, True)
    # pool = await asyncpg.create_pool(config.PG_DSN, min_size=20, max_size=20)
    async with aiohttp.ClientSession() as session:
        async for people in get_people(range(16, MAX + 1), PARTITION, session):
            if 'detail' not in people:
                print(people['name'])
                await asyncio.gather(asyncio.create_task(save_people_in_db(people)))
            else:
                print('Not found')
    # await pool.close()


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main(), debug=True)
    # asyncio.run(main())
    print(time.time() - start)
