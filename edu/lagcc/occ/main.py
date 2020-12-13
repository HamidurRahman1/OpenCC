
from edu.lagcc.occ.util.Utils import URL, CLG_TRM_FORM, CLG_TRM_NAME_KEY, CLG_TRM_VAL_KEY
from datetime import datetime
import requests as req
import time

dt = datetime.now()
term = "2021 Spring Term"
term_val = "1212"

session = req.Session()
CLG_TRM_FORM[CLG_TRM_NAME_KEY] = term
CLG_TRM_FORM[CLG_TRM_VAL_KEY] = term_val
res = session.post(URL, data=CLG_TRM_FORM)
time.sleep(1)
print(res.status_code, datetime.now()-dt)
