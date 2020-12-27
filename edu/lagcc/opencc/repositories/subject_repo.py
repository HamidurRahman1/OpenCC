
from MySQLdb._exceptions import MySQLError
from edu.lagcc.opencc.exceptions.exceptions import NotifyDeveloperException
from edu.lagcc.opencc.models.subject import Subject


class SubjectRepository:

    """ This repository replicates `subjects` table in database. The constructor takes a database connection."""

    def __init__(self, connection):
        self.connection = connection

    def get_all_subjects(self):
        """ Returns all available subjects in the database. """

        query = "select * from subjects"
        try:
            cur = self.connection.cursor()
            subjects_set = set()
            cur.execute(query)
            for subject in cur.fetchall():
                subjects_set.add(Subject(subject_id=subject[0], subject_code=subject[1], subject_name=subject[2]))
            cur.close()
            return subjects_set
        except MySQLError as ex:
            raise NotifyDeveloperException(type(ex).__name__, ex.args)
