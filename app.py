
import logging
from os import environ
from flask_mysqldb import MySQL
from MySQLdb._exceptions import MySQLError
from twilio.base.exceptions import TwilioRestException
from flask import Flask, request, render_template, jsonify
from edu.lagcc.opencc.notifier.sms_sender import Option, SMSSender
from edu.lagcc.opencc.repositories.request_repo import RequestRepository
from edu.lagcc.opencc.exceptions.exceptions import DuplicateRequestException
from edu.lagcc.opencc.utils.util import APP_NAME, POSSIBLE_TERMS, INC_MSG_LOGGER, EXCEPTION_LOGGER, SUB_CODES_TO_SUB_NAMES


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
    logging.getLogger(EXCEPTION_LOGGER).error(mex)


def __add_request(form_data_as_dict):
    try:
        phone_number = int(form_data_as_dict.get("phone-number"))
        term_name, term_value = form_data_as_dict.get("term").split(",")
        subject_code, subject_name = form_data_as_dict.get("subject").split(",")
        class_num_5_digit = int(form_data_as_dict.get("class-num-5"))

        # req_repo = RequestRepository(mysql.connection)
        # status = req_repo.add_request(phone_number, int(term_value), subject_name, subject_code, class_num_5_digit)
        #
        # if status:
        #     SMSSender(option=Option.REQUEST, phone_number=phone_number, subject_name=subject_name,
        #               class_num_5_digit=class_num_5_digit, term_name=term_name).send()
        #     return True, "Dear {} user, we have processed your request for {} - {} for {} Term. You should be "\
        #                  "receiving a confirmation message very shortly. Check out FAQs for important information "\
        #                  "about text messages.".format(APP_NAME, subject_name, class_num_5_digit, term_name)
        return True, "Application is in Beta mode. Your current request is not being saved, and to show the "\
                     "application flow we have listed the information. Phone number: {}, Term: {}, Class: {} - {}"\
            .format(phone_number, term_name, subject_name, class_num_5_digit)
    except DuplicateRequestException as dex:
        return False, "Dear {} user, {} You may add a different request for the same class or a different class if "\
                      "necessary.".format(APP_NAME, dex.message)
    except ValueError:
        return False, "The form was not filled properly or invalid input was entered in the form fields. Please "\
                      "fill out the from properly to make a request."
    except Exception as e:
        logging.getLogger(EXCEPTION_LOGGER).error(e)
        return False, "An unexpected error occurred which I am trying to fix. Meanwhile, you can contact Hamidur "\
                      "Rahman and leave your class info and your request will be added manually as soon as the issue "\
                      "is fixed."


@_app.route("/", methods=["GET"])
def index():
    return render_template("index.html", title=APP_NAME, terms=POSSIBLE_TERMS, subs=SUB_CODES_TO_SUB_NAMES)


@_app.route("/api/request", methods=["POST"])
def _request():
    request_status = __add_request(request.get_json(silent=True))
    if request_status[0]:
        return jsonify(success=request_status[1])
    else:
        return jsonify(error=request_status[1])


@_app.route("/secret_uri"+environ.get("TWILIO_RSP_URI"), methods=["POST"])
def unsubscribe_user():
    from_number = None
    body = None
    try:
        from_number = str(request.form['From']).replace("+1", "")
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
        logging.getLogger(INC_MSG_LOGGER).info("Phone: {}, Message: {}".format(from_number, body))
        return str()
    except TwilioRestException as rex:
        logging.getLogger(INC_MSG_LOGGER).error(rex)
        logging.getLogger(INC_MSG_LOGGER).error("Phone: {}, Message: {}".format(from_number, body))
        return str()
    except Exception as e:
        logging.getLogger(EXCEPTION_LOGGER).error(e)
        logging.getLogger(INC_MSG_LOGGER).error("Phone: {}, Message: {}".format(from_number, body))
        return str()


if __name__ == "__main__":
    try:
        _app.run(use_reloader=False)
    except Exception as ex:
        logging.getLogger(EXCEPTION_LOGGER).error(ex)