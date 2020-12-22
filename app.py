
from edu.lagcc.occ.repositories.request_repo import RequestRepository
from edu.lagcc.occ.instances.flask_instance import FlaskInstance
from edu.lagcc.occ.instances.mysql_instance import MySQLInstance

app = FlaskInstance.get_instance()
mysql = MySQLInstance.get_instance()


@app.route('/', methods=['GET'])
def index():
    next(iter(RequestRepository(mysql.connection).get_requests_to_search_and_notify()[38673])).__str__()
    return "home"


@app.route("/2", methods=['GET'])
def g():
    return next(iter(RequestRepository(mysql.connection).get_requests_to_search_and_notify()[38531])).__str__()


if __name__ == "__main__":
    # from edu.lagcc.occ.task.job_scheduler import init
    # init()
    app.run()



