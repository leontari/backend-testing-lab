import asyncio


async def sleep_and_flush(seconds=3):
    await asyncio.sleep(seconds)
