
from edu.lagcc.opencc.models.models import User
from MySQLdb._exceptions import MySQLError, IntegrityError
from edu.lagcc.opencc.exceptions.exceptions import NotFoundException, UserExistsException


class UserRepository:

    """ This repository replicates `users` table in database. The constructor takes a database connection. """

    def __init__(self, connection):
        self.connection = connection

    def get_user_by_phone_num(self, phone_number):
        """ Returns a User object if an associated user with phone_num exists. """

        query = """select * from users where phone_num = %s """
        try:
            cur = self.connection.cursor()
            cur.execute(query, (phone_number,))
            user = cur.fetchone()
            cur.close()
            if user is None:
                raise NotFoundException("No user with phone_number={} exists".format(phone_number))
            return User(user_id=user[0], phone_number=user[1])
        except MySQLError as ex:
            raise MySQLError("Possible malformed input. {}".format(ex))

    def save_user(self, phone_number):
        """ Creates a user record in the database using the this phone number. """

        query = """insert into users (phone_num) value (%s)"""
        try:
            cur = self.connection.cursor()
            i = cur.execute(query, (phone_number,))
            if i == 1:
                self.connection.commit()
                cur.close()
        except IntegrityError as ex:
            if "for key 'phone_num'" in ex.args[1]:
                raise UserExistsException(phone_number=phone_number)
        except MySQLError as ex:
            raise MySQLError("Possible malformed input. {}".format(ex))
