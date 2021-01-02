
import time
import asyncio
import logging
import MySQLdb
import threading
from os import environ
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from edu.lagcc.opencc.notifier.sms_sender import Option, SMSSender
from edu.lagcc.opencc.exceptions.exceptions import NotFoundException
from edu.lagcc.opencc.searcher.class_searcher import OpenClassSearcher
from edu.lagcc.opencc.utils.util import MSG_LOGGER, EXCEPTION_LOGGER, SCHEDULER_LOGGER
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


def _search_request(tuple_class_num_term, requests_set):
    req_obj = next(iter(requests_set))
    obj = OpenClassSearcher(req_obj.term.term_name, req_obj.term.term_value, req_obj.subject.subject_code,
                            tuple_class_num_term[0]).check_session_one()
    if obj.found:
        if obj.status:
            # _send_notification(requests_set)
            pass
    else:
        obj = obj.check_session_two()
        if obj.found and obj.status:
            # _send_notification(requests_set)
            pass


def _process_request(tuple_to_req_dict):
    threads = []
    for tuple_key in tuple_to_req_dict.keys():
        thread = threading.Thread(target=_search_request, args=[tuple_key, tuple_to_req_dict.get(tuple_key)])
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()


def _get_requests_and_search():
    start = time.time()

    """
        expecting to complete all search by 2.5 mins, if all the search is completed in less than 2.5 mins
        then the scheduler will sleep (2.5 mins - time taken to search) secs.
    """
    expected_end = 150

    if not OpenClassSearcher.is_site_up():
        time.sleep(expected_end)
        return

    try:
        connection = MySQLdb.connect(host=environ.get("MYSQL_HOST"), user=environ.get("MYSQL_USER"),
                                     passwd=environ.get("MYSQL_PASSWORD"), db=environ.get("MYSQL_DB"))
        tuple_class_num_term_to_requests = RequestRepository(connection).get_requests_to_search_and_notify()
        connection.close()

        searching = time.time()
        _process_request(tuple_class_num_term_to_requests)
        logging.getLogger(MSG_LOGGER).info("total time taken to search 60 requests and notify users is: {}".format(time.time()-searching))

        end = round(time.time()-start)
        logging.getLogger(MSG_LOGGER).info("total time taken by scheduler for 60 requests is: {}".format(time.time()-end))
        if end < expected_end:
            time.sleep(expected_end-end)
    except NotFoundException:
        time.sleep(expected_end)
    except Exception as ex:
        logging.getLogger(EXCEPTION_LOGGER).error(ex)
        end = round(time.time()-start)
        if end < expected_end:
            time.sleep(expected_end-end)


async def _search_scheduler():
    while True:
        await _get_requests_and_search()


scheduler = AsyncIOScheduler()
scheduler.start()

try:
    asyncio.get_event_loop().run_until_complete(_search_scheduler())
except SystemExit:
    logging.getLogger(SCHEDULER_LOGGER).debug("system exit")

