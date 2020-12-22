
from edu.lagcc.occ.repositories.request_repo import RequestRepository
from edu.lagcc.occ.instances.flask_instance import FlaskInstance
from edu.lagcc.occ.instances.mysql_instance import MySQLInstance
from edu.lagcc.occ.task.search_invoker import init

app = FlaskInstance.get_instance()
mysql = MySQLInstance.get_instance()


@app.route("/____cc_search__", methods=['GET'])
def g():
    return next(iter(RequestRepository(mysql.connection).get_requests_to_search_and_notify()[38531])).__str__()


if __name__ == "__main__":
    init()
    app.run(use_reloader=False)



