
class User:

    def __init__(self, phone_number, user_id=None):
        self.user_id = user_id
        self.phone_number = phone_number

    def __str__(self):
        return "User{user_id: "+str(self.user_id)+", phone: "+self.phone_number+"}"
