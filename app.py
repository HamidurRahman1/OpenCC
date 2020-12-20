
from edu.lagcc.occ.repositories.request_repo import RequestRepository
from edu.lagcc.occ.instances.flask_instance import FlaskInstance
from edu.lagcc.occ.instances.mysql_instance import MySQLInstance
from os import environ

app = FlaskInstance.get_instance()
mysql = MySQLInstance.get_instance()


@app.route('/', methods=['GET'])
def index():
    d = RequestRepository(mysql.connection).get_requests_to_search_and_notify()
    print(len(d))
    for k in d:
        print(k, " => ")
        for s in d.get(k):
            print(s)
    return "home"

    # s = "===> \n"
    # for key in environ:
    #     s = s + key + "=> " + environ.get(key)
    # return s+"\n <==="


if __name__ == "__main__":

    app.run()



