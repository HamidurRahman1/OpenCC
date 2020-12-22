
import asyncio
import threading
from random import seed
from random import randint


def get():
    import urllib3
    http = urllib3.PoolManager()
    url = 'http://127.0.0.1:5000/__g'
    response = http.request('GET', url)
    print(response.status)
    return set()


@asyncio.coroutine
def check_every_5_secs():
    seed(1)
    while True:
        print('Hello World', randint(0, 10))
        yield from get()


def loop_in_thread(_loop):
    asyncio.set_event_loop(_loop)
    _loop.run_until_complete(check_every_5_secs())


def init():
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=loop_in_thread, args=(loop,))
    t.start()
