import requests as req
import time

COLLEGE = "LaGuardia CC"
CLG_VALUE = "LAG01"
term = "2021 Spring Term"
URL = "https://globalsearch.cuny.edu/CFGlobalSearchTool/CFSearchToolController"

clg_selector_form_data = {"selectedInstName": COLLEGE, "inst_selection": CLG_VALUE, "selectedTermName": term,
                        "term_value":"1212", "next_btn":"Next"}

session = req.Session()
res = session.post(URL, data=clg_selector_form_data)
time.sleep(1)
print(res.status_code, res.text)
