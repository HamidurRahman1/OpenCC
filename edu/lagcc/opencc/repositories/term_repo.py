
from MySQLdb._exceptions import MySQLError
from edu.lagcc.opencc.models.term import Term
from edu.lagcc.opencc.exceptions.exceptions import NotFoundException
from edu.lagcc.opencc.exceptions.exceptions import NotifyDeveloperException


class TermRepository:

    """ This repository replicates `terms` table in database. The constructor takes a database connection."""

    def __init__(self, connection):
        self.connection = connection

    def get_all_terms(self):
        """ Returns all terms that exists in the database. """

        query = "select * from terms"
        try:
            cur = self.connection.cursor()
            terms_set = set()
            cur.execute(query)
            for term in cur.fetchall():
                terms_set.add(Term(term_id=term[0], term_name=term[1], term_value=term[2]))
            cur.close()
            return terms_set
        except MySQLError as ex:
            raise NotifyDeveloperException(type(ex).__name__, ex.args)

    def get_term_by_name(self, term_name):
        """ Returns a Term object if an associated record found with the given term_name. """

        query = """select * from terms where term_name = %s """
        try:
            cur = self.connection.cursor()
            cur.execute(query, (term_name,))
            term = cur.fetchone()
            cur.close()
            if term is None:
                raise NotFoundException("No term exists with the name={}".format(term_name))
            return Term(term_id=term[0], term_name=term[1], term_value=term[2])
        except MySQLError as ex:
            raise NotifyDeveloperException(type(ex).__name__, ex.args)
