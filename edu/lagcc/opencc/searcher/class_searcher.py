
import logging
import requests
from re import match
from bs4 import BeautifulSoup
from edu.lagcc.opencc.utils.util import EXCEPTION_LOG_NAME
from edu.lagcc.opencc.utils.util import TERM_NAMES_TO_VALUES


class OpenClassSearcher:

    URL = "https://globalsearch.cuny.edu/CFGlobalSearchTool/CFSearchToolController"

    def __init__(self, term_name, subject_code, class_num_5_digit):
        self.session = requests.Session()
        self.term_name = term_name + " Term"
        self.__term_value = TERM_NAMES_TO_VALUES[term_name]
        self.subject_code = subject_code
        self.class_num_5_digit = class_num_5_digit
        self.status = False
        self.found = False
        self.clg_trm_dict = {"selectedInstName":    "LaGuardia CC",
                            "inst_selection":       "LAG01",
                            "selectedTermName":     self.term_name,
                            "term_value":           self.__term_value,
                            "next_btn":             "Next"}
        self.cls_details_dict = {"subject_name":             self.subject_code,
                                "selectedSessionName":        "",
                                "class_session":              "",
                                "meetingStart":               "LT",
                                "selectedMeetingStartName":   "less than",
                                "meetingStartText":           "",
                                "AndMeetingStartText":        "",
                                "meetingEnd":                 "LE",
                                "selectedMeetingEndName":     "less than or equal to",
                                "meetingEndText":             "",
                                "AndMeetingEndText":          "",
                                "daysOfWeek":                 "I",
                                "selectedDaysOfWeekName":     "include only these days",
                                "instructor":                 "B",
                                "selectedInstructorName":     "begins with",
                                "instructorName":             "",
                                "search_btn_search":          "Search"}

    def check_session_one(self):
        return self.__class_finder("1")

    def check_session_two(self):
        obj = self.__class_finder("2")
        if not obj.found:
            self.session.close()
        return obj

    def __class_finder(self, session_code):
        self.session.post(OpenClassSearcher.URL, data=self.clg_trm_dict)
        self.cls_details_dict["class_session"] = session_code
        soup = BeautifulSoup(self.session.post(OpenClassSearcher.URL, data=self.cls_details_dict).content, 'html.parser')
        results = soup.find_all("td", {"class": "cunylite_LEVEL3GRIDROW"})
        i = 0
        for elem in results:
            val = elem.text.strip()
            if match("^\\d+$", val) and self.class_num_5_digit == int(val):
                self.found = True
                if elem.find_next("img")["title"] == "Open":
                    self.status = True
                    self.session.close()
                break
            i = i+1
        soup.clear(decompose=True)
        return self

    @staticmethod
    def is_site_up():
        try:
            return requests.get(OpenClassSearcher.URL).status_code == 200
        except Exception as e:
            logging.getLogger(EXCEPTION_LOG_NAME).error("CUNY global class search page is down. {}".format(e))
            return False
