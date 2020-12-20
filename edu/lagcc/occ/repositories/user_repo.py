
from edu.lagcc.occ.models.user import User


class UserRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_user_by_id(self, user_id):
        query = """select * from users where user_id = %s """ % user_id
        cur = self.connection.cursor()
        cur.execute(query)
        user = cur.fetchone()
        cur.close()
        return User(user_id=user[0], phone_number=user[1])

    def get_user_by_phone_num(self, phone_number):
        query = """select * from users where phone_num = %s """ % phone_number
        cur = self.connection.cursor()
        cur.execute(query)
        user = cur.fetchone()
        cur.close()
        return User(user_id=user[0], phone_number=user[1])

    def save_user(self, phone_number):
        query = "insert into users (phone_num) value (%s)" % phone_number
        cur = self.connection.cursor()
        i = cur.execute(query)
        if i == 1:
            cur.execute("select user_id, phone_num from users where phone_num = %s " % phone_number)
            user = cur.fetchone()
            cur.close()
            return User(user_id=user[0], phone_number=user[1])
