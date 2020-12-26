
from MySQLdb._exceptions import IntegrityError
from edu.lagcc.opencc.models.user import User


class UserRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_user_by_id(self, user_id):
        query = """select * from users where user_id = %s """
        try:
            cur = self.connection.cursor()
            cur.execute(query, (user_id,))
            user = cur.fetchone()
            cur.close()
            if user is None:
                print("user does not exists", user_id)
                return False
            return User(user_id=user[0], phone_number=user[1])
        except Exception as ex:
            template = "Exception of type '{0}' with arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            pass  # raise DevNotify Exception

    def get_user_by_phone_num(self, phone_number):
        query = """select * from users where phone_num = %s """
        try:
            cur = self.connection.cursor()
            cur.execute(query, (phone_number,))
            user = cur.fetchone()
            cur.close()
            if user is None:
                print("user does not exists", phone_number)
                return False
            return User(user_id=user[0], phone_number=user[1])
        except Exception as ex:
            template = "Exception of type '{0}' with arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            pass  # raise DevNotify Exception

    def save_user(self, phone_number):
        query = """insert into users (phone_num) value (%s)"""
        try:
            cur = self.connection.cursor()
            i = cur.execute(query, (phone_number,))
            if i == 1:
                self.connection.commit()
                cur.close()
                return True
        except IntegrityError as ex:
            template = "Exception of type '{0}' with arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            pass  # raise DevNotify Exception
        except Exception as ex:
            template = "Exception of type '{0}' with arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            pass  # raise DevNotify Exception
