
from flask import Flask
from flask import render_template
from flask_mysqldb import MySQL
from edu.lagcc.opencc.config.starter import APP_NAME
from edu.lagcc.opencc.repositories.request_repo import RequestRepository
from edu.lagcc.opencc.repositories.user_repo import UserRepository
from edu.lagcc.opencc.task.search_invoker import class_search_scheduler


class FlaskInstance:

    __app_instance = None

    def __init__(self):
        if FlaskInstance.__app_instance is None:
            FlaskInstance.__app_instance = Flask(__name__)
            FlaskInstance.__app_instance.name = APP_NAME
            FlaskInstance.__app_instance.config.from_pyfile("edu/lagcc/opencc/config/config.py")

    @staticmethod
    def get_instance():
        if FlaskInstance.__app_instance is None:
            FlaskInstance()
        return FlaskInstance.__app_instance


class MySQLInstance:

    __mysql_instance = None

    def __init__(self):
        if MySQLInstance.__mysql_instance is None:
            MySQLInstance.__mysql_instance = MySQL(FlaskInstance.get_instance())

    @staticmethod
    def get_instance():
        if MySQLInstance.__mysql_instance is None:
            MySQLInstance()
        return MySQLInstance.__mysql_instance


app = FlaskInstance.get_instance()
mysql = MySQLInstance.get_instance()


@app.route("/", methods=["GET"])
def index():
    d = UserRepository(mysql.connection).save_user(1111111111)
    print(d, "success")
    return render_template("index.html")


if __name__ == "__main__":
    # class_search_scheduler()
    app.run(use_reloader=False)

