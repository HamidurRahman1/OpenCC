
import os
import datetime

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
        sub_code_to_names[code_names[0].strip()] = list(code_names[1].strip().split(","))
    f_obj.close()
    return sub_code_to_names


def possible_terms():
    d = datetime.datetime.now()
    terms = list()
    SP = " Spring Term"
    FA = " Fall Term"

    if d.month == 1 and d.day < 10:
        terms.append(str(d.year-1) + FA)
        terms.append(str(d.year) + SP)
    elif d.month >= 1 and d.month <= 5:
        if d.month == 5 and d.day >= 15:
            terms.append(str(d.year) + SP)
            terms.append(str(d.year) + FA)
        else:
            terms.append(str(d.year) + SP)
    elif d.month == 5 or d.month == 6:
        if d.month == 6 and d.day >= 25:
            terms.append(str(d.year) + FA)
        else:
            terms.append(str(d.year) + SP)
            terms.append(str(d.year) + FA)
    elif d.month >= 6 and d.month <= 10:
        if d.month == 10 and d.day >= 15:
            terms.append(str(d.year+1) + SP)
            terms.append(str(d.year) + FA)
        else:
            terms.append(str(d.year) + FA)
    else:
        terms.append(str(d.year) + FA)
        terms.append(str(d.year+1) + SP)
    return terms


TERMS_VALUES_DICT = load_terms_values()
SUB_CODES_TO_SUB_SET = load_sub_codes_to_names()
POSSIBLE_TERMS = possible_terms()

