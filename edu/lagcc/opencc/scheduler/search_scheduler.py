
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
from edu.lagcc.opencc.repositories.request_repo import RequestRepository
from edu.lagcc.opencc.utils.util import MSG_LOGGER, EXCEPTION_LOGGER, SCHEDULER_LOGGER


def print_requests(t_dict):
    for k in t_dict.keys():
        print(k, "==>")
        for j in t_dict.get(k):
            print(j)


def _send_notification(requests_set):
    """" sends text messages to the user(s) who have made a request to get notified for the class in request obj """
    for request in requests_set:
        SMSSender(option=Option.OPEN, phone_number=request.user.phone_number, subject_name=request.subject.subject_name,
                  class_num_5_digit=request.class_num_5_digit, term_name=request.term.term_name).send()


def _search_request(tuple_class_num_term, requests_set):
    """"
        tuple_class_num_term: a tuple consists of 5_digit_class_number and term_name
        requests_set: the requests (users) who made the request for the 5_digit_class_number and term_name in param 1
    """
    req_obj = next(iter(requests_set))
    obj = OpenClassSearcher(req_obj.term.term_name, req_obj.term.term_value, req_obj.subject.subject_code,
                            tuple_class_num_term[0]).check_session_one()
    if obj.found:
        if obj.status:
            _send_notification(requests_set)
    else:
        obj = obj.check_session_two()
        if obj.found and obj.status:
            _send_notification(requests_set)


def _process_request(tuple_to_req_dict):
    """
        creates N threads where N is the length of the tuple_to_req_dict to search and notify users about the class(es)

        tuple_to_req_dict: a dictionary,
            key : tuple(5_digit_class_number, term_name)
            value : list of requests (e.g. users) who made the request
    """

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
        expecting to complete all requests to search in 2.5 mins, if all the searches are completed in less than 
        2.5 mins then the scheduler will sleep (2.5 mins - time taken to search) secs.
    """
    expected_end = 150

    if not OpenClassSearcher.is_site_up():
        time.sleep(expected_end)
        return set()

    try:
        connection = MySQLdb.connect(host=environ.get("MYSQL_HOST"), user=environ.get("MYSQL_USER"),
                                     passwd=environ.get("MYSQL_PASSWORD"), db=environ.get("MYSQL_DB"))

        """
            tuple_class_num_term_to_requests: a dictionary
                key : tuple(5_digit_class_number, term_name) 
                value : list of requests (e.g. users) who made the request
        """
        tuple_class_num_term_to_requests = RequestRepository(connection).get_requests_to_search_and_notify()
        connection.close()

        requests_length = len(tuple_class_num_term_to_requests)

        logging.getLogger(SCHEDULER_LOGGER).debug("Total requests found: {}".format(requests_length))

        searching_start = time.time()
        _process_request(tuple_class_num_term_to_requests)
        logging.getLogger(MSG_LOGGER).info("Total time taken to search {} requests and notify users is: {}"
                                           .format(requests_length, time.time()-searching_start))

        end = round(time.time()-start)
        logging.getLogger(MSG_LOGGER).info("Total time taken by scheduler for {} requests is: {}"
                                           .format(requests_length, end))
        if end < expected_end:
            time.sleep(expected_end-end)
    except NotFoundException:
        # thrown by the repository if there are no request to search and notify, just sleep expected time and try again
        time.sleep(expected_end)
    except Exception as ex:
        logging.getLogger(EXCEPTION_LOGGER).error(ex)
        end = round(time.time()-start)
        if end < expected_end:
            time.sleep(expected_end-end)
    return set()


@asyncio.coroutine
def _search_scheduler():
    while True:
        yield from _get_requests_and_search()


scheduler = AsyncIOScheduler()
scheduler.start()

try:
    asyncio.get_event_loop().run_until_complete(_search_scheduler())
except Exception as e:
    logging.getLogger(SCHEDULER_LOGGER).error(e)
except SystemExit as se:
    logging.getLogger(SCHEDULER_LOGGER).debug("System EXIT. {}".format(se))

