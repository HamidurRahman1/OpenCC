
import asyncio
import threading
import urllib3
import time


def invoke_class_searcher():
    response = urllib3.PoolManager().request("GET", "https://opencclagcc.herokuapp.com/____cc_search__")
    print(response.status, response.data.decode("utf-8"))
    time.sleep(60)
    return set()


@asyncio.coroutine
def call_class_search():
    while True:
        yield from invoke_class_searcher()


def loop_in_thread(_loop):
    asyncio.set_event_loop(_loop)
    _loop.run_until_complete(call_class_search())


def init():
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=loop_in_thread, args=(loop,))
    t.start()
