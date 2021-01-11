
import logging
from enum import Enum
from os import environ
from twilio.rest import Client
from edu.lagcc.opencc.utils.util import APP_NAME
from twilio.base.exceptions import TwilioRestException
from edu.lagcc.opencc.utils.util import EXCEPTION_LOGGER


class Option(Enum):
    OPEN = 1
    REQUEST = 2
    UN_SUB_1 = 3
    UN_SUB_ALL = 4


class SMSSender:

    __account_sid = environ.get("TWILIO_ACCOUNT_SID")
    __auth_token = environ.get("TWILIO_AUTH_TOKEN")
    __from = environ.get("TWILIO_NUMBER")

    def __init__(self, option, phone_number, subject_name=None, class_num_5_digit=None, term_name=None):

        self.__client = Client(SMSSender.__account_sid, SMSSender.__auth_token)
        self._to = "+1"+str(phone_number)
        self._from = SMSSender.__from

        if option == Option.REQUEST:
            self._body = "Added {}-{}".format(subject_name, class_num_5_digit)
        elif option == Option.OPEN:
            self._body = "Open {}-{}".format(subject_name, class_num_5_digit)
        elif option == Option.UN_SUB_1:
            self._body = "Unsubscribed {}".format(class_num_5_digit)
        elif option == Option.UN_SUB_ALL:
            self._body = "Unsubscribed all"

    def send(self):
        try:
            self.__client.api.account.messages.create(to=self._to, from_=self._from, body=self._body)
        except TwilioRestException as rex:
            logging.getLogger(EXCEPTION_LOGGER).error("Exception type: {}, Message: {}, Status: {}, Details: {}, Args: {}, PhoneNumber: {}, Body: {}"
                                                      .format(type(rex).__name__, rex.msg, rex.status, rex.details, rex.args, self._to, self._body))
        except Exception as ex:
            logging.getLogger(EXCEPTION_LOGGER).error("Exception type: {}, Message: {}".format(type(ex).__name__, ex.args))
