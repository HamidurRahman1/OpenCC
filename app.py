
from edu.lagcc.occ.services.term_service import TermService
from edu.lagcc.occ.singletons.flask_instance import SingletonFlaskInstance
from edu.lagcc.occ.singletons.mysql_instance import SingletonMySQLInstance
from os import environ

app = SingletonFlaskInstance.get_instance()


@app.route('/', methods=['GET'])
def index():
    s = "===> \n"
    for key in environ:
        s = s + key + "=> " + environ.get(key)
    return s+"\n <==="


if __name__ == "__main__":

    app.run()



