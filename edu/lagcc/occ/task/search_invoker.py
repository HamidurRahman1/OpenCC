
import asyncio
import threading
import time
import MySQLdb
import logging
from os import environ


def invoke_class_searcher():
    db = MySQLdb.connect(host=environ.get("MYSQL_HOST"), user=environ.get("MYSQL_USER"),
                         passwd=environ.get("MYSQL_PASSWORD"), db=environ.get("MYSQL_DB"))
    cur = db.cursor()
    cur.execute("SELECT * FROM users")
    s = ""
    for row in cur.fetchall():
        s = s + str(row[0]) + " " + row[1] + " => "
    logging.info(s)
    db.close()
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
