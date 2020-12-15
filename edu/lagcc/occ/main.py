
from edu.lagcc.occ.searcher.class_searcher import OpenClassSearcher
from edu.lagcc.occ.config.starter import *
from edu.lagcc.occ.models.term import Term
from edu.lagcc.occ.models.user import User
from edu.lagcc.occ.models.subject import Subject
from datetime import datetime

dt = datetime.now()

if __name__ == "__main__":

    term = "2021 Spring"
    subject_code = "VETE"
    class_num_5_digit = "55576"

    print(Term(term, "1212"))
    print(User("2124700016", 89))
    print(Subject("MATH", "MAT 115"))

    print(TERMS_VALUES_DICT)
    print(SUB_CODES_TO_SUB_LIST)

    print(datetime.now()-dt)
    obj = OpenClassSearcher(term, subject_code, class_num_5_digit).check_session_one()
    if not obj.found:
        print("session 2")
        obj.check_session_two()
    print(datetime.now()-dt)
