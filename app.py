
from flask import Flask
from flask import request
from flask import render_template
from flask_mysqldb import MySQL
from edu.lagcc.opencc.exceptions.exceptions import DuplicateRequestException
from edu.lagcc.opencc.notifier.sms_sender import SMSSender
from edu.lagcc.opencc.repositories.request_repo import RequestRepository
from edu.lagcc.opencc.repositories.user_repo import UserRepository
from edu.lagcc.opencc.utils.util import APP_NAME
from edu.lagcc.opencc.utils.util import POSSIBLE_TERMS
from edu.lagcc.opencc.utils.util import SUB_CODES_TO_SUB_SET


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


def __add_request__():
    try:
        phone_number = int(request.form.get("phone-number"))
        term_name, term_value = request.form.get("term").split(",")
        subject_code, subject_name = request.form.get("subject").split(",")
        class_num_5_digit = int(request.form.get("class-num-5"))

        req_repo = RequestRepository(mysql.connection)
        user_repo = UserRepository(mysql.connection)
        status = req_repo.add_request(phone_number, int(term_value), subject_name, subject_code, class_num_5_digit)

        if status:
            user = user_repo.get_user_by_phone_num(phone_number)
            SMSSender(phone_number=phone_number, subject_name=subject_name, class_num_5_digit=class_num_5_digit,
                      term_name=term_name, request=True, user_id=user.user_id).send()
            return "Dear {} user, we have processed your request for {} - {} for {} Term. You user id is: {}. " \
                   "It is needed when you get the requested class(es) and would like to opt out from " \
                   "getting notification.".format(APP_NAME, subject_name, class_num_5_digit, term_name, user.user_id)
    except DuplicateRequestException as dex:
        return "Dear {} user, {} You may add a different request for a different class if necessary."\
                .format(APP_NAME, dex)
    except Exception as ex:
        SMSSender(dev=True, dev_msg=ex.args).send()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", title=APP_NAME, terms=POSSIBLE_TERMS, subs=SUB_CODES_TO_SUB_SET)
    elif request.method == "POST":
        status = __add_request__()
        return render_template("index.html", title=APP_NAME, terms=POSSIBLE_TERMS, subs=SUB_CODES_TO_SUB_SET,
                               request_message=status)


if __name__ == "__main__":
    # class_search_scheduler()
    app.run(use_reloader=False)

