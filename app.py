
import logging
from os import environ
from flask import Flask
from flask import request
from flask import render_template
from flask_mysqldb import MySQL
from MySQLdb._exceptions import MySQLError
from twilio.base.exceptions import TwilioRestException
from edu.lagcc.opencc.notifier.sms_sender import Option
from edu.lagcc.opencc.notifier.sms_sender import SMSSender
from edu.lagcc.opencc.utils.util import APP_NAME
from edu.lagcc.opencc.utils.util import POSSIBLE_TERMS
from edu.lagcc.opencc.utils.util import UNK_MSG_LOG_NAME
from edu.lagcc.opencc.utils.util import EXCEPTION_LOG_NAME
from edu.lagcc.opencc.utils.util import SUB_CODES_TO_SUB_NAMES
from edu.lagcc.opencc.repositories.request_repo import RequestRepository
from edu.lagcc.opencc.exceptions.exceptions import DuplicateRequestException


_app = Flask(__name__)
_app.name = APP_NAME
_app.config.from_pyfile("edu/lagcc/opencc/config/config.py")


class MySQLInstance:

    __mysql_instance = None

    def __init__(self):
        if MySQLInstance.__mysql_instance is None:
            MySQLInstance.__mysql_instance = MySQL(_app)

    @staticmethod
    def get_instance():
        if MySQLInstance.__mysql_instance is None:
            MySQLInstance()
        return MySQLInstance.__mysql_instance


mysql = None
try:
    mysql = MySQLInstance.get_instance()
except MySQLError as mex:
    logging.getLogger(EXCEPTION_LOG_NAME).error(mex)


def __add_request__():
    try:
        phone_number = int(request.form.get("phone-number"))
        term_name, term_value = request.form.get("term").split(",")
        subject_code, subject_name = request.form.get("subject").split(",")
        class_num_5_digit = int(request.form.get("class-num-5"))

        req_repo = RequestRepository(mysql.connection)
        status = req_repo.add_request(phone_number, int(term_value), subject_name, subject_code, class_num_5_digit)

        if status:
            SMSSender(option=Option.REQUEST, phone_number=phone_number, subject_name=subject_name,
                      class_num_5_digit=class_num_5_digit, term_name=term_name).send()
            return "Dear {} user, we have processed your request for {} - {} for {} Term."\
                   .format(APP_NAME, subject_name, class_num_5_digit, term_name)
    except DuplicateRequestException as dex:
        return "Dear {} user, {} You may add a different request for a different class if necessary."\
               .format(APP_NAME, str(dex).lower())
    except Exception as e:
        logging.getLogger(EXCEPTION_LOG_NAME).error(e)


@_app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        status = __add_request__()
        return render_template("index.html", title=APP_NAME, terms=POSSIBLE_TERMS, subs=SUB_CODES_TO_SUB_NAMES,
                               request_message=status)
    else:
        return render_template("index.html", title=APP_NAME, terms=POSSIBLE_TERMS, subs=SUB_CODES_TO_SUB_NAMES)


@_app.route("/"+environ.get("TWILIO_RSP_URI"), methods=["POST"])
def unsubscribe_user():
    try:
        from_number = str(request.form['From']).replace("+", "")
        body = str(request.form['Body']).strip().lower()
        body_length = len(body)

        # 'cancel all' --> delete all requests that exists with the this phone number
        if body_length == 10 and body == "cancel all":
            if RequestRepository(mysql.connection).delete_request(from_number):
                SMSSender(option=Option.UN_SUB_ALL, phone_number=from_number).send()
        # 'cancel [5-digit-code]' --> delete the request that exists with the this phone number and 5-digit-class-num
        elif body_length == 12 and body.startswith("cancel"):
            cls_5_digit = body.split(" ")[1]
            if len(cls_5_digit) == 5 and cls_5_digit.isdigit():
                if RequestRepository(mysql.connection).delete_request(from_number, int(cls_5_digit)):
                    SMSSender(option=Option.UN_SUB_1, phone_number=from_number, class_num_5_digit=cls_5_digit).send()
    except TwilioRestException as rex:
        logging.getLogger(UNK_MSG_LOG_NAME).error(rex)
    except Exception as e:
        logging.getLogger(EXCEPTION_LOG_NAME).error(e)


if __name__ == "__main__":
    try:
        # class_search_scheduler()
        _app.run(use_reloader=False)
    except Exception as ex:
        logging.getLogger(EXCEPTION_LOG_NAME).error(ex)

