
from edu.lagcc.occ.models.term import Term


class TermService:

    def __init__(self, connection):
        self.connection = connection

    def get_all_terms(self):
        query = "select * from terms"
        cur = self.connection.cursor()
        terms_list = set()
        cur.execute(query)
        for term in cur.fetchall():
            terms_list.add(Term(term[1], term[2], term[0]))
        cur.close()
        return terms_list
