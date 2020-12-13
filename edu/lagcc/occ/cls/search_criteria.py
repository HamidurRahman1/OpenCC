
from edu.lagcc.occ.util.Utils import *
from bs4 import BeautifulSoup
import requests
import re


class SearchCriteriaPage:

    def __init__(self, term_name, subject_code, class_num_5_digit):
        self.session = requests.Session()
        self.term_name = term_name
        self.subject_code = subject_code
        self.class_num_5_digit = class_num_5_digit
        self.status = False

    def check_session_one(self):
        CLG_TRM_FORM[CLG_TRM_NAME_KEY] = self.term_name
        CLG_TRM_FORM[CLG_TRM_VAL_KEY] = "1212"
        self.session.post(URL, data=CLG_TRM_FORM)
        CLASS_DETAILS_FORM[SUBJECT_NAME_KEY] = self.subject_code
        CLASS_DETAILS_FORM[SESSION_KEY] = "1"
        soup = BeautifulSoup(self.session.post(URL, data=CLASS_DETAILS_FORM).content, 'html.parser')
        results = soup.find_all("td", {"class": "cunylite_LEVEL3GRIDROW"})
        i = 0
        for elem in results:
            val = elem.text.strip()
            if re.match("^\\d+$", val) and self.class_num_5_digit == val:
                print("found", results[i+7])
                print(elem.find_next("img")["title"])
                # notify if open
                if elem.find_next("img")["title"] == "Open":
                    self.status = True
                    break
            i = i+1
        return self
