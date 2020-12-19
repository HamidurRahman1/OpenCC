
from edu.lagcc.occ.repositories.subject_repo import SubjectRepository
from edu.lagcc.occ.repositories.term_repo import TermRepository
from edu.lagcc.occ.singletons.flask_instance import SingletonFlaskInstance
from edu.lagcc.occ.singletons.mysql_instance import SingletonMySQLInstance
from os import environ

app = SingletonFlaskInstance.get_instance()
mysql = SingletonMySQLInstance.get_instance()


@app.route('/', methods=['GET'])
def index():
    for i in SubjectRepository(mysql.connection).get_all_subjects():
        print(i)
    return "home"

    # s = "===> \n"
    # for key in environ:
    #     s = s + key + "=> " + environ.get(key)
    # return s+"\n <==="


if __name__ == "__main__":

    app.run()



