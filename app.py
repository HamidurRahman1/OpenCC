
from edu.lagcc.occ.services.subject_service import SubjectService
from edu.lagcc.occ.singletons.flask_instance import SingletonFlaskInstance
from edu.lagcc.occ.singletons.mysql_instance import SingletonMySQLInstance
from os import environ

app = SingletonFlaskInstance.get_instance()
mysql = SingletonMySQLInstance.get_instance()


@app.route('/', methods=['GET'])
def index():
    for sub in SubjectService(mysql.connection).get_all_subjects():
        print(sub)
    return "subject service tested"
    # s = "===> \n"
    # for key in environ:
    #     s = s + key + "=> " + environ.get(key)
    # return s+"\n <==="


if __name__ == "__main__":

    app.run()



