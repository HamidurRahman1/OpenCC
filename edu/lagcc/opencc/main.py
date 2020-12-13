
from edu.lagcc.opencc.util.Utils import COLLEGE, CLG_VALUE, URL, NEXT

from datetime import datetime
import requests as req
import time

dt = datetime.now()
term = "2021 Spring Term"
term_val = "1212"

clg_selector_form_data = {"selectedInstName": COLLEGE, "inst_selection": CLG_VALUE, "selectedTermName": term,
                        "term_value": term_val, "next_btn": NEXT}

session = req.Session()
res = session.post(URL, data=clg_selector_form_data)
time.sleep(1)
print(res.status_code, res.text)
print(datetime.now()-dt)
