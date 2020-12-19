
from edu.lagcc.occ.repositories.user_repo import UserRepository
from edu.lagcc.occ.singletons.flask_instance import SingletonFlaskInstance
from edu.lagcc.occ.singletons.mysql_instance import SingletonMySQLInstance
from os import environ

app = SingletonFlaskInstance.get_instance()
mysql = SingletonMySQLInstance.get_instance()


@app.route('/', methods=['GET'])
def index():
    return UserRepository(mysql.connection).get_user_by_phone_num(1111111111).__str__()

    # s = "===> \n"
    # for key in environ:
    #     s = s + key + "=> " + environ.get(key)
    # return s+"\n <==="


if __name__ == "__main__":

    app.run()



