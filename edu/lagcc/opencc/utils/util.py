
import os
import sys
import pytz
import logging
from datetime import datetime

APP_NAME = "OpenCC"

TERMS_VALUES_FILE_PATH = os.path.join(os.path.dirname(__file__), "../props/terms_values.properties")
SUB_CODES_FILE_PATH = os.path.join(os.path.dirname(__file__), "../props/sub_codes.properties")

DATETIME_FORMATTER = "%m-%d-%Y %I:%M:%S %p"

INC_MSG_LOGGER = "INC_MESSAGES_LOGGER"
EXCEPTION_LOGGER = "EXCEPTIONS_LOGGER"
APP_HITS_LOGGER = "APP_HITS_LOGGER"
SCHEDULER_LOGGER = "SCHEDULER_LOGGER"

INC_MSG_LOG_FORMATTER = "$ {} -> %(nyc_datetime)s :: %(name)s => %(message)s".format(APP_NAME)
APP_HITS_LOG_FORMATTER = "$ {} -> %(nyc_datetime)s :: %(name)s => %(message)s".format(APP_NAME)
TASK_LOG_FORMATTER = "$ {} -> %(nyc_datetime)s :: %(name)s => %(message)s".format(APP_NAME)
EXCEPTION_LOG_FORMATTER = "$ {} -> %(nyc_datetime)s :: %(name)s :: %(levelname)s :: %(module)s => %(message)s".format(APP_NAME)


class DateTimeFilter(logging.Filter):
    def filter(self, record):
        record.nyc_datetime = formatted_nyc_datetime()
        return True


def formatted_nyc_datetime():
    return datetime.now(tz=pytz.timezone("America/New_York")).strftime(DATETIME_FORMATTER)


def setup_logger(name, formatter, level):
    logger = logging.getLogger(name)
    logger.addFilter(DateTimeFilter())
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter(formatter))
    logger.setLevel(level)
    logger.addHandler(handler)


def load_terms_values():
    terms_dict = dict()
    f_obj = open(TERMS_VALUES_FILE_PATH)
    for line in f_obj.readlines():
        term_val = line.split("=")
        terms_dict[term_val[1].strip()] = term_val[0].strip()
    f_obj.close()
    return terms_dict


def load_sub_codes_to_names():
    sub_code_to_names = dict()
    f_obj = open(SUB_CODES_FILE_PATH)
    for line in f_obj.readlines():
        code_names = line.split("=")
        sub_code_to_names[code_names[0].strip()] = list(code_names[1].strip().split(","))
    f_obj.close()
    return sub_code_to_names


def possible_terms():
    d = datetime.now()
    terms = dict()
    SP = " Spring"
    FA = " Fall"

    if d.month == 1 and d.day < 7:
        terms[str(d.year-1) + FA] = TERM_NAMES_TO_VALUES[str(d.year-1)+FA]
        terms[str(d.year) + SP] = TERM_NAMES_TO_VALUES[str(d.year)+SP]
    elif d.month >= 1 and d.month <= 5:
        if d.month == 5 and d.day >= 15:
            terms[str(d.year) + SP] = TERM_NAMES_TO_VALUES[str(d.year)+SP]
            terms[str(d.year) + FA] = TERM_NAMES_TO_VALUES[str(d.year)+FA]
        else:
            terms[str(d.year) + SP] = TERM_NAMES_TO_VALUES[str(d.year)+SP]
    elif d.month == 5 or d.month == 6:
        if d.month == 6 and d.day >= 25:
            terms[str(d.year) + FA] = TERM_NAMES_TO_VALUES[str(d.year)+FA]
        else:
            terms[str(d.year) + SP] = TERM_NAMES_TO_VALUES[str(d.year)+SP]
            terms[str(d.year) + FA] = TERM_NAMES_TO_VALUES[str(d.year)+FA]
    elif d.month >= 6 and d.month <= 10:
        if d.month == 10 and d.day >= 15:
            terms[str(d.year+1) + SP] = TERM_NAMES_TO_VALUES[str(d.year+1)+SP]
            terms[str(d.year) + FA] = TERM_NAMES_TO_VALUES[str(d.year)+FA]
        else:
            terms[str(d.year) + FA] = TERM_NAMES_TO_VALUES[str(d.year)+FA]
    else:
        terms[str(d.year) + FA] = TERM_NAMES_TO_VALUES[str(d.year)+FA]
        terms[str(d.year+1) + SP] = TERM_NAMES_TO_VALUES[str(d.year+1)+SP]
    return terms


setup_logger(SCHEDULER_LOGGER, TASK_LOG_FORMATTER, logging.DEBUG)
setup_logger(INC_MSG_LOGGER, INC_MSG_LOG_FORMATTER, logging.DEBUG)
setup_logger(APP_HITS_LOGGER, APP_HITS_LOG_FORMATTER, logging.INFO)
setup_logger(EXCEPTION_LOGGER, EXCEPTION_LOG_FORMATTER, logging.ERROR)

TERM_NAMES_TO_VALUES = load_terms_values()
SUB_CODES_TO_SUB_NAMES = load_sub_codes_to_names()
POSSIBLE_TERMS = possible_terms()
