
from edu.lagcc.occ.util.Utils import *
import requests


class SearchCriteriaPage:

    def __init__(self):
        self.session = requests.Session()

    def search_criteria_response(self, term_name, term_value, subject_code, session_code):
        CLG_TRM_FORM[CLG_TRM_NAME_KEY] = term_name
        CLG_TRM_FORM[CLG_TRM_VAL_KEY] = term_value
        self.session.post(URL, data=CLG_TRM_FORM)
        CLASS_DETAILS_FORM[SUBJECT_NAME_KEY] = subject_code
        CLASS_DETAILS_FORM[SESSION_KEY] = session_code
        response = self.session.post(URL, data=CLASS_DETAILS_FORM)
        return response
