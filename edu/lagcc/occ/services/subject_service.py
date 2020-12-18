
from edu.lagcc.occ.models.subject import Subject


class SubjectService:

    def __init__(self, connection):
        self.connection = connection

    def get_all_subjects(self):
        query = "select * from subjects"
        cur = self.connection.cursor()
        subjects_list = set()
        cur.execute(query)
        for subject in cur.fetchall():
            subjects_list.add(Subject(subject_id=subject[0], subject_code=subject[1], subject_name=subject[2]))
        cur.close()
        return subjects_list


