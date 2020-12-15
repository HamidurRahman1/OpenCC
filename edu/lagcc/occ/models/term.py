
class Term:

    def __init__(self, term_name, term_value, term_id=None):
        self.term_id = term_id
        self.term_name = term_name
        self.term_value = term_value

    def __str__(self):
        return "Term{term_id: "+str(self.term_id)+", term_name: " \
               + self.term_name + ", term_value: "+self.term_value+"}"
