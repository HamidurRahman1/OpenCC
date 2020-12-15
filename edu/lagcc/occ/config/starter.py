
import os
import logging

APP_NAME = "OpenCC"

TERMS_VALUES_FILE_PATH = os.path.join(os.path.dirname(__file__), '../props/terms_values.properties')
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), '../logs/logs.log')

LOG_FORMAT = "$ "+APP_NAME+" ---> %(levelname)s :: %(message)s"
logging.basicConfig(filename=LOG_FILE_PATH, filemode='w', level=logging.INFO, format=LOG_FORMAT)


def load_terms_values():
    terms_dict = dict()
    f_obj = open(TERMS_VALUES_FILE_PATH)
    for line in f_obj.readlines():
        term_val = line.split("=")
        terms_dict[term_val[1].strip()] = term_val[0].strip()
    f_obj.close()
    return terms_dict


TERMS_VALUES_DICT = load_terms_values()