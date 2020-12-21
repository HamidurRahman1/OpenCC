
from edu.lagcc.occ.models.user import User


class UserRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_user_by_id(self, user_id):
        query = """select * from users where user_id = %s """
        cur = self.connection.cursor()
        cur.execute(query, (user_id,))
        user = cur.fetchone()
        cur.close()
        return User(user_id=user[0], phone_number=user[1])

    def get_user_by_phone_num(self, phone_number):
        query = """select * from users where phone_num = %s """
        cur = self.connection.cursor()
        cur.execute(query, (phone_number,))
        user = cur.fetchone()
        cur.close()
        return User(user_id=user[0], phone_number=user[1])

    def save_user(self, phone_number):
        query = """insert into users (phone_num) value (%s)"""
        cur = self.connection.cursor()
        i = cur.execute(query, (phone_number,))
        if i == 1:
            self.connection.commit()
            cur.close()
