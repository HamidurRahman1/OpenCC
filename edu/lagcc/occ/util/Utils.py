
import os

TERMS_VALUES_FILE_PATH = os.path.join(os.path.dirname(__file__), '../props/terms_values.txt')
TERM = "Term"


def load_terms_values():
    terms_dict = dict()
    f_obj = open(TERMS_VALUES_FILE_PATH)
    for line in f_obj.readlines():
        term_val = line.split("=")
        terms_dict[term_val[0]] = term_val[1].strip()
    return terms_dict


TERMS_VALUES_DICT = load_terms_values()

URL = "https://globalsearch.cuny.edu/CFGlobalSearchTool/CFSearchToolController"

SESSION_1 = "1"
SESSION_2 = "2"

FIVE_DIGIT_CLASS_LEVEL = "cunylite_LEVEL3GRIDROW"

OPEN_STATUS = "Open"
CLOSED_STATUS = "Open"

CLG_TRM_NAME_KEY = "selectedTermName"
CLG_TRM_VAL_KEY = "term_value"
CLG_TRM_FORM = {"selectedInstName":     "LaGuardia CC",
                "inst_selection":       "LAG01",
                CLG_TRM_NAME_KEY:       "",
                CLG_TRM_VAL_KEY:        "",
                "next_btn":             "Next"}


SESSION_KEY = "class_session"
SUBJECT_NAME_KEY = "subject_name"
CLASS_DETAILS_FORM = {SUBJECT_NAME_KEY:             "",
                      "selectedSessionName":        "",
                      SESSION_KEY:                  "",
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

