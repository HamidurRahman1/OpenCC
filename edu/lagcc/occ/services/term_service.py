
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
            terms_list.add(Term(term_id=term[0], term_name=term[1], term_value=term[2]))
        cur.close()
        return terms_list

    def get_term_by_name(self, term_name):
        query = """select * from terms where term_name = '%s' """ % term_name
        cur = self.connection.cursor()
        cur.execute(query)
        term = cur.fetchone()
        return Term(term_id=term[0], term_name=term[1], term_value=term[2])
