
import asyncio
import threading
import time
import MySQLdb
from os import environ
from edu.lagcc.occ.repositories.request_repo import RequestRepository
from edu.lagcc.occ.searcher.class_searcher import OpenClassSearcher


def _search(class_num, requests_set):
    req_obj = next(iter(requests_set))
    obj = OpenClassSearcher(req_obj.term.term_name, req_obj.subject.subject_code, class_num).check_session_one()
    if obj.found:
        if obj.status:
            # send text to all users in requests_set
            print("notify", len(requests_set), "users")
        else:
            print("class still closed in s1")
    else:
        obj = obj.check_session_two()
        print("check 2")
        if obj.found:
            if obj.status:
                # send text to all users in requests_set
                print("notify", len(requests_set), "users")
            else:
                print("class still closed in s2")


def _process(class_num_to_req_dict):
    threads = []
    for class_num in class_num_to_req_dict.keys():
        thread = threading.Thread(target=_search, args=[class_num, class_num_to_req_dict.get(class_num)])
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()


def _invoke_class_searcher():
    start = time.time()
    expected_end = 60

    connection = MySQLdb.connect(host=environ.get("MYSQL_HOST"), user=environ.get("MYSQL_USER"),
                                 passwd=environ.get("MYSQL_PASSWORD"), db=environ.get("MYSQL_DB"))

    class_num_to_requests = RequestRepository(connection).get_requests_to_search_and_notify()
    connection.close()
    for k in class_num_to_requests.keys():
        print(k, "==>")
        for j in class_num_to_requests.get(k):
            print(j)
    ss = time.time()
    _process(class_num_to_requests)
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
