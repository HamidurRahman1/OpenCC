
import os
import sys
import logging
import datetime

APP_NAME = "OpenCC"

# possibly change it and read from database at startup
TERMS_VALUES_FILE_PATH = os.path.join(os.path.dirname(__file__), "../props/terms_values.properties")
SUB_CODES_FILE_PATH = os.path.join(os.path.dirname(__file__), "../props/sub_codes.properties")

MSG_LOGGER = "MESSAGE"                      # logger name for exception related to messages
EXCEPTION_LOGGER = "EXCEPTION"                # logger name for other exceptions
SCHEDULER_LOGGER = "SCHEDULER"                # logger name for class search scheduler

LOG_FORMATTER = "$ {} -> %(asctime)s :: %(name)s :: %(levelname)s :: %(module)s :: %(message)s".format(APP_NAME)
LOG_TIME_FMT = "%m-%d-%Y %I:%M:%S %p"


def setup_logger(logger_name, level):

    logging.basicConfig(format=LOG_FORMATTER, datefmt=LOG_TIME_FMT, stream=sys.stdout)
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)


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
    d = datetime.datetime.now()
    terms = dict()
    SP = " Spring"
    FA = " Fall"

    if d.month == 1 and d.day < 10:
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


setup_logger(MSG_LOGGER, logging.DEBUG)
setup_logger(SCHEDULER_LOGGER, logging.DEBUG)
setup_logger(EXCEPTION_LOGGER, logging.ERROR)

TERM_NAMES_TO_VALUES = load_terms_values()
SUB_CODES_TO_SUB_NAMES = load_sub_codes_to_names()
POSSIBLE_TERMS = possible_terms()

