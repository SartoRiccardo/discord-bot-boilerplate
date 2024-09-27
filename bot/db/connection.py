import asyncpg
import config
from functools import wraps

pool: asyncpg.Pool | None


async def start():
    global pool
    try:
        pool = await asyncpg.create_pool(
            user=config.DB_USER, password=config.DB_PSWD,
            database=config.DB_NAME, host=config.DB_HOST
        )
    except:
        print("\033[91m" + "Error connecting to Postgres database" + "\033[0m")
        exit(1)


def postgres(wrapped):
    @wraps(wrapped)
    async def wrapper(*args, **kwargs):
        if "conn" in kwargs:
            return await wrapped(*args, **kwargs)

        if pool is None:
            return
        async with pool.acquire() as conn:
            return await wrapped(*args, **kwargs, conn=conn)
    return wrapper
