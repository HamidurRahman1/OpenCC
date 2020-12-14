
from edu.lagcc.occ.cls.search_criteria import SearchCriteria
from datetime import datetime

dt = datetime.now()

if __name__ == "__main__":

    term = "2021 Spring Term"
    subject_code = "VETE"
    class_num_5_digit = "39345"

    print(datetime.now()-dt)
    obj = SearchCriteria(term, subject_code, class_num_5_digit).check_session_one()
    if not obj.found:
        obj.check_session_two()
    print(datetime.now()-dt)
