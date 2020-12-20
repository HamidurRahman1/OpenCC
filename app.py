
from edu.lagcc.occ.repositories.user_repo import UserRepository
from edu.lagcc.occ.instances.flask_instance import FlaskInstance
from edu.lagcc.occ.instances.mysql_instance import MySQLInstance
from os import environ

app = FlaskInstance.get_instance()
mysql = MySQLInstance.get_instance()


@app.route('/', methods=['GET'])
def index():
    s = str(app.__str__())
    s = s.replace('<', '').replace('>', '')
    return str(app.__hash__()) + " => " + s

    # s = "===> \n"
    # for key in environ:
    #     s = s + key + "=> " + environ.get(key)
    # return s+"\n <==="


if __name__ == "__main__":

    app.run()



