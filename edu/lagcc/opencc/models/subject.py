
class Subject:

    def __init__(self, subject_code, subject_name, subject_id=None):
        self.subject_id = subject_id
        self.subject_code = subject_code
        self.subject_name = subject_name

    def __str__(self):
        return "Subject{subject_id: "+str(self.subject_id)+", subject_code: " \
               + self.subject_code + ", subject_name: "+self.subject_name+"}"
