
import asyncio
import threading
from random import seed
from random import randint


@asyncio.coroutine
def check_every_5_secs():
    seed(1)
    while True:
        print('Hello World', randint(0, 10))
        yield from asyncio.sleep(5)     # do class search here


def loop_in_thread(_loop):
    asyncio.set_event_loop(_loop)
    _loop.run_until_complete(check_every_5_secs())


loop = asyncio.get_event_loop()
t = threading.Thread(target=loop_in_thread, args=(loop,))
t.start()
