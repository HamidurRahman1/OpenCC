
from edu.lagcc.occ.cls.search_criteria import SearchCriteriaPage
from datetime import datetime

dt = datetime.now()

if __name__ == "__main__":

    term = "2021 Spring Term"
    subject_code = "VETE"
    class_num_5_digit = "39335"

    print(datetime.now()-dt)
    obj = SearchCriteriaPage(term, subject_code, class_num_5_digit).check_session_one()
    if obj.status:
        print("open")
    else:
        print(obj.status)
    print(datetime.now()-dt)
