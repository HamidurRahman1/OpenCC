
import time
import asyncio
import logging
import MySQLdb
import threading
from os import environ
from edu.lagcc.opencc.notifier.sms_sender import Option, SMSSender
from edu.lagcc.opencc.exceptions.exceptions import NotFoundException
from edu.lagcc.opencc.searcher.class_searcher import OpenClassSearcher
from edu.lagcc.opencc.utils.util import MSG_LOG_NAME, EXCEPTION_LOG_NAME
from edu.lagcc.opencc.repositories.request_repo import RequestRepository


def print_requests(t_dict):
    for k in t_dict.keys():
        print(k, "==>")
        for j in t_dict.get(k):
            print(j)


def _send_notification(requests_set):
    for request in requests_set:
        SMSSender(option=Option.OPEN, phone_number=request.user.phone_number, subject_name=request.subject.subject_name,
                  class_num_5_digit=request.class_num_5_digit, term_name=request.term.term_name).send()


def _search(tuple_class_num_term, requests_set):
    req_obj = next(iter(requests_set))
    obj = OpenClassSearcher(req_obj.term.term_name, req_obj.subject.subject_code, tuple_class_num_term[0]).check_session_one()
    if obj.found:
        if obj.status:
            # _send_notification(requests_set)
            print(len(requests_set), "users notified")
    else:
        obj = obj.check_session_two()
        if obj.found and obj.status:
            # _send_notification(requests_set)
            print(len(requests_set), "users notified")


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
    expected_end = 180

    if not OpenClassSearcher.is_site_up():
        time.sleep(expected_end)
        return set()

    try:
        logging.getLogger(MSG_LOG_NAME).info("connecting to db")
        connection = MySQLdb.connect(host=environ.get("MYSQL_HOST"), user=environ.get("MYSQL_USER"),
                                     passwd=environ.get("MYSQL_PASSWORD"), db=environ.get("MYSQL_DB"))
        tuple_class_num_term_to_requests = RequestRepository(connection).get_requests_to_search_and_notify()
        connection.close()

        print_requests(tuple_class_num_term_to_requests)

        s = time.time()
        logging.getLogger(MSG_LOG_NAME).info("starting search: {}".format(s))
        _process(tuple_class_num_term_to_requests)
        logging.getLogger(MSG_LOG_NAME).info("total time taken to search 60 requests and notify users is: {}".format(time.time()-s))

        end = round(time.time()-start)
        if end < expected_end:
            time.sleep(expected_end-end)
        logging.getLogger(MSG_LOG_NAME).info("total time taken by scheduler for 60 requests is: {}".format(time.time()-start))
    except NotFoundException:
        time.sleep(expected_end)
    except Exception as ex:
        logging.getLogger(EXCEPTION_LOG_NAME).error(ex)
        end = round(time.time()-start)
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
