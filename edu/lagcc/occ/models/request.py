
class Request:

    def __init__(self, user, term, subject, class_num_5_digit, request_id=None):
        self.request_id = request_id
        self.user = user
        self.term = term
        self.subject = subject
        self.class_num_5_digit = class_num_5_digit

    def __str__(self):
        return "Request{request_id: "+str(self.request_id)+", user: "+self.user.__str__() + \
               ", term: "+self.term.__str__()+", subject: "+self.subject.__str__() + \
               ", class_num_5_digit: "+str(self.class_num_5_digit)+"}"
