
from flask import Flask
from flask import request
from flask import render_template
from flask_mysqldb import MySQL
from edu.lagcc.opencc.utils.util import APP_NAME
from edu.lagcc.opencc.utils.util import POSSIBLE_TERMS
from edu.lagcc.opencc.utils.util import SUB_CODES_TO_SUB_SET
from edu.lagcc.opencc.repositories.request_repo import RequestRepository


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
    return render_template("index.html", terms=POSSIBLE_TERMS, subs=SUB_CODES_TO_SUB_SET)


@app.route("/add/request", methods=["POST"])
def add_request():
    print(request.form['term'])
    print(request.form['phone-number'])
    return render_template("reqs.html", success="we have processed your request. check out for a notification",
                           terms=POSSIBLE_TERMS, subs=SUB_CODES_TO_SUB_SET)


@app.route("/user/requests", methods=["GET"])
def get():
    return render_template("reqs.html", rs="a", terms=POSSIBLE_TERMS, subs=SUB_CODES_TO_SUB_SET)


@app.route("/delete/request", methods=["DELETE"])
def delete_request():
    return "delete request"


if __name__ == "__main__":
    # class_search_scheduler()
    app.run(use_reloader=False)

