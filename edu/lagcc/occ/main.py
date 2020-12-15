
from edu.lagcc.occ.searcher.class_searcher import SearchCriteria
from datetime import datetime

dt = datetime.now()

if __name__ == "__main__":

    term = "2021 Spring"
    subject_code = "VETE"
    class_num_5_digit = "55576"

    print(datetime.now()-dt)
    obj = SearchCriteria(term, subject_code, class_num_5_digit).check_session_one()
    if not obj.found:
        print("session 2")
        obj.check_session_two()
    print(datetime.now()-dt)
