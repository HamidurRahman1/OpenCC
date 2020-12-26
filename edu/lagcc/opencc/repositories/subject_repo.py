
from edu.lagcc.opencc.models.subject import Subject


class SubjectRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all_subjects(self):
        query = "select * from subjects"
        try:
            cur = self.connection.cursor()
            subjects_set = set()
            cur.execute(query)
            for subject in cur.fetchall():
                subjects_set.add(Subject(subject_id=subject[0], subject_code=subject[1], subject_name=subject[2]))
            cur.close()
            return subjects_set
        except Exception as ex:
            template = "Exception of type '{0}' with arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            pass    # raise DevNotify Exception
