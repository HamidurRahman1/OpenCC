
from edu.lagcc.occ.repositories.term_repo import TermRepository
from edu.lagcc.occ.instances.flask_instance import FlaskInstance
from edu.lagcc.occ.instances.mysql_instance import MySQLInstance
from os import environ

app = FlaskInstance.get_instance()
mysql = MySQLInstance.get_instance()


@app.route('/', methods=['GET'])
def index():
    print(TermRepository(mysql.connection).get_term_by_name("2025 Fall"))
    return "home"

    # s = "===> \n"
    # for key in environ:
    #     s = s + key + "=> " + environ.get(key)
    # return s+"\n <==="


if __name__ == "__main__":

    app.run()



