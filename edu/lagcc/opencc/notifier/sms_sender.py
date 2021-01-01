
import logging
from enum import Enum
from os import environ
from twilio.rest import Client
from edu.lagcc.opencc.utils.util import APP_NAME
from edu.lagcc.opencc.utils.util import MSG_LOG_NAME
from twilio.base.exceptions import TwilioRestException


class Option(Enum):
    OPEN = 1
    REQUEST = 2
    UN_SUB_1 = 3
    UN_SUB_ALL = 4


class SMSSender:

    __account_sid = environ.get("TWILIO_ACCOUNT_SID")
    __auth_token = environ.get("TWILIO_AUTH_TOKEN")
    __from = environ.get("TWILIO_NUMBER")
    __msg_service_id = environ.get("MSG_SERVICE_ID")

    def __init__(self, option, phone_number, subject_name=None, class_num_5_digit=None, term_name=None):

        self.__client = Client(SMSSender.__account_sid, SMSSender.__auth_token)
        self._to = "+1"+str(phone_number)
        self._from = SMSSender.__from

        if option == Option.REQUEST:
            # self._body = "Dear {} user, requested {}-{} for {} has been added and will get notified once it's open. I "\
            #              "have got you with your classes,🤝. Cheers!".format(APP_NAME, subject_name, class_num_5_digit, term_name)
            self._body = "Added {}-{}".format(subject_name, class_num_5_digit)
        elif option == Option.OPEN:
            # self._body = "Dear {} user, your requested class {} - {} for {} is now OPEN ✅. Good Luck!"\
            #              .format(APP_NAME, subject_name, class_num_5_digit, term_name)
            self._body = "Open {}-{}".format(subject_name, class_num_5_digit)
        elif option == Option.UN_SUB_1:
            # self._body = "Dear {} user, you have been UNSUBSCRIBED from Class Number: {} and won't get notification" \
            #              "for this class anymore.".format(APP_NAME, class_num_5_digit)
            self._body = "Unsubscribed {}".format(class_num_5_digit)
        elif option == Option.UN_SUB_ALL:
            # self._body = "Dear {} user, you have been UNSUBSCRIBED from all your classes but you can always go ahead" \
            #              "and add new requests again.".format(APP_NAME)
            self._body = "Unsubscribed all"

    def send(self):
        try:
            self.__client.api.account.messages.create(to=self._to, from_=self._from, body=self._body)
        except TwilioRestException as rex:
            logging.getLogger(MSG_LOG_NAME).error(rex)
        except Exception as ex:
            logging.getLogger(MSG_LOG_NAME).error(ex)
