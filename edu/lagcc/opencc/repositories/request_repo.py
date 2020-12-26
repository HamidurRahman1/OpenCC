
from edu.lagcc.opencc.models.request import Request
from edu.lagcc.opencc.models.term import Term
from edu.lagcc.opencc.models.subject import Subject
from edu.lagcc.opencc.models.user import User


class RequestRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_requests_to_search_and_notify(self):
        query = """
                select r.fk_user_id, u.phone_num, t.term_name, t.term_value, s.subject_code, s.subject_name, r.class_num_5_digit 
                from requests r
                inner join users u on u.user_id = r.fk_user_id
                inner join terms t on r.fk_term_id = t.term_id
                inner join subjects s on r.fk_subject_id = s.subject_id
                order by u.user_id
                """
        cur = self.connection.cursor()
        cur.execute(query)
        class_num_to_requests = dict()
        for request in cur.fetchall():
            user_obj = User(user_id=request[0], phone_number=request[1])
            term_obj = Term(term_name=request[2], term_value=request[3])
            subject_obj = Subject(subject_code=request[4], subject_name=request[5])
            request_obj = Request(user=user_obj, term=term_obj, subject=subject_obj, class_num_5_digit=request[6])
            if (request_obj.class_num_5_digit, request_obj.term.term_name) in class_num_to_requests:
                class_num_to_requests.get((request_obj.class_num_5_digit, request_obj.term.term_name)).add(request_obj)
            else:
                class_num_to_requests[(request_obj.class_num_5_digit, request_obj.term.term_name)] = {request_obj}
        cur.close()
        return class_num_to_requests

    def add_request(self, phone_number, term_value, subject_name, subject_code, class_num_5_digit):
        query = """
                insert into requests (fk_user_id, fk_term_id, fk_subject_id, class_num_5_digit) values 
                ((select user_id from users where phone_num = %s), 
                (select term_id from terms where term_value = %s),
                (select subject_id from subjects where subject_name = %s and subject_code = %s),
                %s);
                """
        cur = self.connection.cursor()
        row = cur.execute(query, (phone_number, term_value, subject_name, subject_code, class_num_5_digit))
        if row == 1:
            self.connection.commit()
        cur.close()
