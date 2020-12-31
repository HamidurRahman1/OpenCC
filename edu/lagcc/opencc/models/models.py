
class User:

    def __init__(self, phone_number, user_id=None):
        self.user_id = user_id
        self.phone_number = phone_number

    def __str__(self):
        return "User{user_id: "+str(self.user_id)+", phone: "+self.phone_number+"}"


class Request:

    def __init__(self, user, term, subject, class_num_5_digit, request_id=None):
        self.request_id = request_id
        self.user = user
        self.term = term
        self.subject = subject
        self.class_num_5_digit = class_num_5_digit

    def __str__(self):
        return "Request{request_id: "+str(self.request_id)+", user: "+self.user.__str__() +\
               ", term: "+self.term.__str__()+", subject: "+self.subject.__str__() +\
               ", class_num_5_digit: "+str(self.class_num_5_digit)+"}"


class Subject:

    def __init__(self, subject_code, subject_name, subject_id=None):
        self.subject_id = subject_id
        self.subject_code = subject_code
        self.subject_name = subject_name

    def __str__(self):
        return "Subject{subject_id: "+str(self.subject_id)+", subject_code: "\
               + self.subject_code + ", subject_name: "+self.subject_name+"}"


class Term:

    def __init__(self, term_name, term_value, term_id=None):
        self.term_id = term_id
        self.term_name = term_name
        self.term_value = term_value

    def __str__(self):
        return "Term{term_id: "+str(self.term_id)+", term_name: "\
               + self.term_name + ", term_value: "+self.term_value+"}"

