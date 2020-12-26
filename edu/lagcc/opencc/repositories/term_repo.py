
from edu.lagcc.opencc.models.term import Term


class TermRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all_terms(self):
        query = "select * from terms"
        try:
            cur = self.connection.cursor()
            terms_set = set()
            cur.execute(query)
            for term in cur.fetchall():
                terms_set.add(Term(term_id=term[0], term_name=term[1], term_value=term[2]))
            cur.close()
            return terms_set
        except Exception as ex:
            template = "Exception of type '{0}' with arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            pass  # raise DevNotify Exception

    def get_term_by_name(self, term_name):
        query = """select * from terms where term_name = %s """
        try:
            cur = self.connection.cursor()
            cur.execute(query, (term_name,))
            term = cur.fetchone()
            cur.close()
            return Term(term_id=term[0], term_name=term[1], term_value=term[2])
        except Exception as ex:
            template = "Exception of type '{0}' with arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            pass  # raise DevNotify Exception
