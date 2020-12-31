
from MySQLdb._exceptions import MySQLError
from MySQLdb._exceptions import IntegrityError
from edu.lagcc.opencc.models.models import User
from edu.lagcc.opencc.models.models import Term
from edu.lagcc.opencc.models.models import Subject
from edu.lagcc.opencc.models.models import Request
from edu.lagcc.opencc.repositories.user_repo import UserRepository
from edu.lagcc.opencc.exceptions.exceptions import NotFoundException
from edu.lagcc.opencc.exceptions.exceptions import NotifyDeveloperException
from edu.lagcc.opencc.exceptions.exceptions import DuplicateRequestException


class RequestRepository:

    """ This repository replicates `requests` table in database. The constructor takes a database connection."""

    def __init__(self, connection):
        self.connection = connection
        self.user_repository = UserRepository(connection)

    def get_requests_to_search_and_notify(self):
        """
            Returns all requests as a dictionary where request(s) are values and a tuple as key consisting
            class_num_5_digit and term name.
        """

        query = """
                select r.fk_user_id, u.phone_num, t.term_name, t.term_value, s.subject_code, s.subject_name, r.class_num_5_digit 
                from requests r
                inner join users u on u.user_id = r.fk_user_id
                inner join terms t on r.fk_term_id = t.term_id
                inner join subjects s on r.fk_subject_id = s.subject_id
                """
        try:
            cur = self.connection.cursor()
            cur.execute(query)
            tuple_class_num_term_to_requests = dict()
            requests = cur.fetchall()
            if len(requests) > 0:
                for request in requests:
                    user_obj = User(user_id=request[0], phone_number=request[1])
                    term_obj = Term(term_name=request[2], term_value=request[3])
                    subject_obj = Subject(subject_code=request[4], subject_name=request[5])
                    request_obj = Request(user=user_obj, term=term_obj, subject=subject_obj, class_num_5_digit=request[6])
                    if (request_obj.class_num_5_digit, request_obj.term.term_name) in tuple_class_num_term_to_requests:
                        tuple_class_num_term_to_requests.get(
                            (request_obj.class_num_5_digit, request_obj.term.term_name)).add(request_obj)
                    else:
                        tuple_class_num_term_to_requests[(request_obj.class_num_5_digit, request_obj.term.term_name)]={
                            request_obj}
                cur.close()
                return tuple_class_num_term_to_requests
            else:
                raise NotFoundException("No requests found to notify.")
        except MySQLError as ex:
            raise NotifyDeveloperException(type(ex).__name__, ex.args)

    def add_request(self, phone_number, term_value, subject_name, subject_code, class_num_5_digit):
        """ Adds this request to notify this user when this class becomes open."""

        query = """
                insert into requests (fk_user_id, fk_term_id, fk_subject_id, class_num_5_digit) values 
                ((select user_id from users where phone_num = %s), 
                (select term_id from terms where term_value = %s),
                (select subject_id from subjects where subject_name = %s and subject_code = %s),
                %s);
                """
        try:
            try:
                self.user_repository.get_user_by_phone_num(phone_number)
            except NotFoundException:
                self.user_repository.save_user(phone_number)
            cur = self.connection.cursor()
            row = cur.execute(query, (phone_number, term_value, subject_name, subject_code, class_num_5_digit))
            if row == 1:
                self.connection.commit()
                cur.close()
                return True
            cur.close()
        except IntegrityError as ex:
            if "for key 'fk_user_id'" in ex.args[1]:
                raise DuplicateRequestException(phone_number=phone_number, subject_name=subject_name, class_num_5_digit=class_num_5_digit)
        except MySQLError as ex:
            raise NotifyDeveloperException(type(ex).__name__, ex.args)

    def delete_request(self, from_number, class_num_5_digit=False):
        """
            If class_num_5_digit is false then deletes all requested associated with the phone number, otherwise
            delete the request associated the phone number and class_num_5_digit.
        """
        try:
            query = None
            data = None
            if class_num_5_digit:
                query = """delete from requests where class_num_5_digit = %(class_num)s and 
                        fk_user_id = (select user_id from users where phone_num = %(phone)s)"""
                data = {'phone': from_number, 'class_num': class_num_5_digit}
            else:
                query = """delete from requests where fk_user_id = 
                        (select user_id from users where phone_num = %(phone)s)"""
                data = {'phone': from_number}
            cur = self.connection.cursor()
            row = cur.execute(query, data)
            if row >= 1:
                self.connection.commit()
                cur.close()
                return True
            cur.close()
        except MySQLError as ex:
            raise NotifyDeveloperException(type(ex).__name__, ex.args)
