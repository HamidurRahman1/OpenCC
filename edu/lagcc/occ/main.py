
from edu.lagcc.occ.util.Utils import *
from datetime import datetime
import requests as req
import time

dt = datetime.now()

session = req.Session()

CLG_TRM_FORM[CLG_TRM_NAME_KEY] = "2021 Spring Term"
CLG_TRM_FORM[CLG_TRM_VAL_KEY] = "1212"
res = session.post(URL, data=CLG_TRM_FORM)
time.sleep(1)
print(res.status_code, datetime.now()-dt)

CLASS_DETAILS_FORM[SUBJECT_NAME_KEY] = "VETE"
CLASS_DETAILS_FORM[SESSION_KEY] = "1"
res2 = session.post(URL, data=CLASS_DETAILS_FORM)
print(res2.status_code, datetime.now()-dt)
print(res2.text)

