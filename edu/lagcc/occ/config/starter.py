
import os

APP_NAME = "OpenCC"

TERMS_VALUES_FILE_PATH = os.path.join(os.path.dirname(__file__), "../props/terms_values.properties")
SUB_CODES_FILE_PATH = os.path.join(os.path.dirname(__file__), "../props/sub_codes.properties")


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
        sub_code_to_names[code_names[0].strip()] = set(code_names[1].strip().split(","))
    f_obj.close()
    return sub_code_to_names


TERMS_VALUES_DICT = load_terms_values()
SUB_CODES_TO_SUB_SET = load_sub_codes_to_names()
