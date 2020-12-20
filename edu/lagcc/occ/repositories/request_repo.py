
from edu.lagcc.occ.models.request import Request
from edu.lagcc.occ.models.term import Term
from edu.lagcc.occ.models.subject import Subject
from edu.lagcc.occ.models.user import User


class RequestRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_requests_to_notify(self):
        query = """
                    select r.fk_user_id, u.phone_num, t.term_name, s.subject_name, r.class_num_5_digit from requests r
                    inner join users u on u.user_id = r.fk_user_id
                    inner join terms t on r.fk_term_id = t.term_id
                    inner join subjects s on r.fk_subject_id = s.subject_id
                    order by u.user_id
                """
        cur = self.connection.cursor()
        cur.execute(query)
        requests = set()
        for request in cur.fetchall():
            user_obj = User(user_id=request[0], phone_number=request[1])
            term_obj = Term(term_name=request[2], term_value="")
            subject_obj = Subject(subject_name=request[3], subject_code="")
            requests.add(Request(user=user_obj, term=term_obj, subject=subject_obj, class_num_5_digit=request[4]))
        return requests
