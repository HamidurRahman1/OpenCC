
import asyncio
import threading
import time
import MySQLdb
from os import environ
from edu.lagcc.occ.repositories.request_repo import RequestRepository


def invoke_class_searcher():
    connection = MySQLdb.connect(host=environ.get("MYSQL_HOST"), user=environ.get("MYSQL_USER"),
                         passwd=environ.get("MYSQL_PASSWORD"), db=environ.get("MYSQL_DB"))
    d = RequestRepository(connection).get_requests_to_search_and_notify()
    for k in d.keys():
        print(k, "==>")
        for j in d.get(k):
            print(j)
    connection.close()
    time.sleep(10)
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
