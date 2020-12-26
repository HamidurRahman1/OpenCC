
import asyncio
import threading
import time
import MySQLdb
from os import environ
from edu.lagcc.opencc.notifier.sms_sender import SMSSender
from edu.lagcc.opencc.repositories.request_repo import RequestRepository
from edu.lagcc.opencc.searcher.class_searcher import OpenClassSearcher


def _search(tuple_class_num_term, requests_set):
    req_obj = next(iter(requests_set))
    obj = OpenClassSearcher(req_obj.term.term_name, req_obj.subject.subject_code, tuple_class_num_term).check_session_one()
    if obj.found:
        if obj.status:
            SMSSender(req_obj.user.phone_number, req_obj.subject.subject_name, tuple_class_num_term[0], req_obj.term.term_name).send()
            print(len(requests_set), "users notified")
        else:
            print("class still closed in session 1")
    else:
        obj = obj.check_session_two()
        if obj.found:
            if obj.status:
                SMSSender(req_obj.user.phone_number, req_obj.subject.subject_name, tuple_class_num_term[0], req_obj.term.term_name).send()
                print(len(requests_set), "users notified")
            else:
                print("class still closed in session 2")


def _process(tuple_to_req_dict):
    threads = []
    for tuple_key in tuple_to_req_dict.keys():
        thread = threading.Thread(target=_search, args=[tuple_key, tuple_to_req_dict.get(tuple_key)])
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()


def _invoke_class_searcher():
    start = time.time()
    expected_end = 120

    connection = MySQLdb.connect(host=environ.get("MYSQL_HOST"), user=environ.get("MYSQL_USER"),
                                 passwd=environ.get("MYSQL_PASSWORD"), db=environ.get("MYSQL_DB"))

    tuple_class_num_term_to_requests = RequestRepository(connection).get_requests_to_search_and_notify()
    connection.close()
    for k in tuple_class_num_term_to_requests.keys():
        print(k, "==>")
        for j in tuple_class_num_term_to_requests.get(k):
            print(j)
    ss = time.time()
    _process(tuple_class_num_term_to_requests)
    print(time.time()-ss, "pro")
    end = round(time.time()-start)
    print(time.time()-start, "all")
    if end < expected_end:
        time.sleep(expected_end-end)
    return set()


@asyncio.coroutine
def _call_class_search():
    while True:
        yield from _invoke_class_searcher()


def _loop_in_thread(_loop):
    asyncio.set_event_loop(_loop)
    _loop.run_until_complete(_call_class_search())


def class_search_scheduler():
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=_loop_in_thread, args=(loop,))
    t.start()