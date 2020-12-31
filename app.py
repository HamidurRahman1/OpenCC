
from os import environ
from flask import Flask
from flask import request
from flask import render_template
from flask_mysqldb import MySQL
from edu.lagcc.opencc.exceptions.exceptions import DuplicateRequestException
from edu.lagcc.opencc.exceptions.exceptions import NotifyDeveloperException
from edu.lagcc.opencc.notifier.sms_sender import SMSSender
from edu.lagcc.opencc.repositories.request_repo import RequestRepository
from edu.lagcc.opencc.utils.util import APP_NAME
from edu.lagcc.opencc.utils.util import POSSIBLE_TERMS
from edu.lagcc.opencc.utils.util import SUB_CODES_TO_SUB_SET


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


mysql = MySQLInstance.get_instance()


def __add_request__():
    try:
        phone_number = int(request.form.get("phone-number"))
        term_name, term_value = request.form.get("term").split(",")
        subject_code, subject_name = request.form.get("subject").split(",")
        class_num_5_digit = int(request.form.get("class-num-5"))

        req_repo = RequestRepository(mysql.connection)
        status = req_repo.add_request(phone_number, int(term_value), subject_name, subject_code, class_num_5_digit)

        if status:
            SMSSender(phone_number=phone_number, subject_name=subject_name, class_num_5_digit=class_num_5_digit,
                      term_name=term_name, request=True).send()
            return "Dear {} user, we have processed your request for {} - {} for {} Term."\
                    .format(APP_NAME, subject_name, class_num_5_digit, term_name)
    except DuplicateRequestException as dex:
        return "Dear {} user, {} You may add a different request for a different class if necessary."\
                .format(APP_NAME, str(dex).lower())
    except NotifyDeveloperException as nex:
        SMSSender(dev=True, dev_msg=nex).send()
    except:
        pass


@_app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        status = __add_request__()
        return render_template("index.html", title=APP_NAME, terms=POSSIBLE_TERMS, subs=SUB_CODES_TO_SUB_SET,
                               request_message=status)
    else:
        return render_template("index.html", title=APP_NAME, terms=POSSIBLE_TERMS, subs=SUB_CODES_TO_SUB_SET)


@_app.route("/delete", methods=["POST"])
def unsubscribe_user():
    try:
        from_number = request.form['From']
        body = str(request.form['Body']).strip().lower()
        body_length = len(body)

        # 'cancel all' --> delete all requests that exists with the this phone number
        if body_length == 10:
            RequestRepository(mysql.connection).delete_request(from_number)
            # notify That All Reqs Are Deleted
        # 'cancel [5-digit-code]' --> delete the request that exists with the this phone number and 5-digit-class-num
        elif body_length == 12:
            cls_5_digit = body.split(" ")[1]
            if len(cls_5_digit) == 5 and cls_5_digit.isdigit():
                RequestRepository(mysql.connection).delete_request(from_number, int(cls_5_digit))
                # notify That specific req is Deleted
    except:
        pass


if __name__ == "__main__":
    # class_search_scheduler()
    _app.run(use_reloader=False)

