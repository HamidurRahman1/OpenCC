
from edu.lagcc.occ.repositories.request_repo import RequestRepository
from edu.lagcc.occ.instances.flask_instance import FlaskInstance
from edu.lagcc.occ.instances.mysql_instance import MySQLInstance
from os import environ

app = FlaskInstance.get_instance()
mysql = MySQLInstance.get_instance()


@app.route('/', methods=['GET'])
def index():

    for i in RequestRepository(mysql.connection).get_requests_to_notify():
        print(i)
    return "home"

    # s = "===> \n"
    # for key in environ:
    #     s = s + key + "=> " + environ.get(key)
    # return s+"\n <==="


if __name__ == "__main__":

    app.run()



