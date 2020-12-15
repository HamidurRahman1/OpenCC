
from edu.lagcc.occ.config.starter import TERMS_VALUES_DICT
from bs4 import BeautifulSoup
import requests
import re


class SearchCriteria:

    URL = "https://globalsearch.cuny.edu/CFGlobalSearchTool/CFSearchToolController"

    def __init__(self, term_name, subject_code, class_num_5_digit):
        self.session = requests.Session()
        self.term_name = term_name + " Term"
        self.__term_value = TERMS_VALUES_DICT[term_name]
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
        return self.__class_finder("2")

    def __class_finder(self, session_code):
        self.session.post(SearchCriteria.URL, data=self.clg_trm_dict)
        self.cls_details_dict["class_session"] = session_code
        soup = BeautifulSoup(self.session.post(SearchCriteria.URL, data=self.cls_details_dict).content, 'html.parser')
        results = soup.find_all("td", {"class": "cunylite_LEVEL3GRIDROW"})
        i = 0
        for elem in results:
            val = elem.text.strip()
            if re.match("^\\d+$", val) and self.class_num_5_digit == val:
                self.found = True
                print("==> ", results[i+7])
                print("==> ", elem.find_next("img")["title"])
                # notify if open
                if elem.find_next("img")["title"] == "Open":
                    self.status = True
                    break
            i = i+1
        return self
