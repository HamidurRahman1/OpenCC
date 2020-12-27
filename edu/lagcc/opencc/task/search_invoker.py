
import asyncio
import threading
import time
import MySQLdb
from os import environ
from edu.lagcc.opencc.exceptions.exceptions import NotFoundException
from edu.lagcc.opencc.exceptions.exceptions import NotifyDeveloperException
from edu.lagcc.opencc.notifier.sms_sender import SMSSender
from edu.lagcc.opencc.repositories.request_repo import RequestRepository
from edu.lagcc.opencc.searcher.class_searcher import OpenClassSearcher


def print_requests(t_dict):
    for k in t_dict.keys():
        print(k, "==>")
        for j in t_dict.get(k):
            print(j)


def _search(tuple_class_num_term, requests_set):
    req_obj = next(iter(requests_set))
    obj = OpenClassSearcher(req_obj.term.term_name, req_obj.subject.subject_code, tuple_class_num_term[0]).check_session_one()
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
    expected_end = 360

    # check if the global_search_site is up
        # if up then check if req > 0
            # if not then sleep for 5 min
        # search and send texts
    # if not then sleep for 5 min

    try:
        connection = MySQLdb.connect(host=environ.get("MYSQL_HOST"), user=environ.get("MYSQL_USER"),
                                   passwd=environ.get("MYSQL_PASSWORD"), db=environ.get("MYSQL_DB"))

        tuple_class_num_term_to_requests = RequestRepository(connection).get_requests_to_search_and_notify()
        connection.close()

        print_requests(tuple_class_num_term_to_requests)

        _process(tuple_class_num_term_to_requests)

        end = round(time.time()-start)
        print(end, "all")
        if end < expected_end:
            time.sleep(expected_end-end)
    except NotFoundException:
        time.sleep(expected_end)
    except NotifyDeveloperException as dex:
        pass
    except Exception as e:
        pass
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
