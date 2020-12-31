
import logging
from enum import Enum
from os import environ
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from edu.lagcc.opencc.utils.util import APP_NAME, UNK_MSG_LOG_NAME


class Option(Enum):
    DEV = 1
    OPEN = 2
    REQUEST = 3
    UN_SUB_1 = 4
    UN_SUB_ALL = 5


class SMSSender:

    __account_sid = 'environ.get("TWILIO_ACCOUNT_SID")'
    __auth_token = 'environ.get("TWILIO_AUTH_TOKEN")'
    __from = 'environ.get("TWILIO_NUMBER")'
    __dev_num = 'environ.get("DEV_NUMBER")'

    def __init__(self, option, phone_number=None, subject_name=None, class_num_5_digit=None, term_name=None, msg=None):

        self.__client = Client(SMSSender.__account_sid, SMSSender.__auth_token)

        if option == Option.DEV:
            self._to = SMSSender.__dev_num
            self._body = msg
        elif option == Option.REQUEST:
            self._to = "+1"+str(phone_number)
            self._body = "Dear {} user, requested {}-{} for {} has been added and will get notified once it's open. I "\
                         "have got you with your classes,🤝. Cheers!".format(APP_NAME, subject_name, class_num_5_digit, term_name)
        elif option == Option.OPEN:
            self._to = "+1"+str(phone_number)
            self._body = "Dear {} user, your requested class {} - {} for {} is now OPEN ✅. Good Luck!"\
                         .format(APP_NAME, subject_name, class_num_5_digit, term_name)
        elif option == Option.UN_SUB_1:
            self._to = "+1"+str(phone_number)
            self._body = "Dear {} user, you have been UNSUBSCRIBE from Class Number: {}.".format(APP_NAME, class_num_5_digit)
        elif option == Option.UN_SUB_ALL:
            self._to = "+1"+str(phone_number)
            self._body = "Dear {} user, you have been UNSUBSCRIBE from all your classes.".format(APP_NAME)

        self._from = SMSSender.__from

    def send(self):
        try:
            self.__client.api.account.messages.create(to=self._to, from_=self._from, body=self._body)
        except TwilioRestException as rex:
            logging.getLogger(UNK_MSG_LOG_NAME).error(rex)
        except Exception as ex:
            logging.getLogger(UNK_MSG_LOG_NAME).error(ex)
