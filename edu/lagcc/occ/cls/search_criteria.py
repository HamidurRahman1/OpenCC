
from edu.lagcc.occ.util.Utils import *
from bs4 import BeautifulSoup
import requests
import re


class SearchCriteria:

    def __init__(self, term_name, subject_code, class_num_5_digit):
        self.session = requests.Session()
        self.term_name = term_name
        self.__term_value = "1212"                  # determine from prop file using term_name
        self.subject_code = subject_code
        self.class_num_5_digit = class_num_5_digit
        self.status = False
        self.found = False
        self.clg_trm_dict = CLG_TRM_FORM.copy()
        self.cls_details_dict = CLASS_DETAILS_FORM.copy()

    def check_session_one(self):
        return self.__do_extraction("1")

    def check_session_two(self):
        return self.__do_extraction("2")

    def __do_extraction(self, session_code):
        self.clg_trm_dict[CLG_TRM_NAME_KEY] = self.term_name
        self.clg_trm_dict[CLG_TRM_VAL_KEY] = self.__term_value
        self.session.post(URL, data=self.clg_trm_dict)
        self.cls_details_dict[SUBJECT_NAME_KEY] = self.subject_code
        self.cls_details_dict[SESSION_KEY] = session_code
        soup = BeautifulSoup(self.session.post(URL, data=self.cls_details_dict).content, 'html.parser')
        results = soup.find_all("td", {"class": "cunylite_LEVEL3GRIDROW"})
        i = 0
        for elem in results:
            val = elem.text.strip()
            if re.match("^\\d+$", val) and self.class_num_5_digit == val:
                self.found = True
                print("==> found", results[i+7])
                print("==> ", elem.find_next("img")["title"])
                # notify if open
                if elem.find_next("img")["title"] == "Open":
                    self.status = True
                    break
            i = i+1
        return self
