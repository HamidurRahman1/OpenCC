
from os import environ
from twilio.rest import Client
from edu.lagcc.opencc.utils.util import APP_NAME


class SMSSender:

    __account_sid = 'environ.get("TWILIO_ACCOUNT_SID")'
    __auth_token = 'environ.get("TWILIO_AUTH_TOKEN")'
    __from = 'environ.get("TWILIO_NUMBER")'
    __dev_num = 'environ.get("DEV_NUMBER")'

    def __init__(self, phone_number=None, subject_name=None, class_num_5_digit=None, term_name=None, request=False,
                 user_id=None, dev=False, dev_msg=None):

        self.__client = Client(SMSSender.__account_sid, SMSSender.__auth_token)
        self.__to = "+1"+str(phone_number)
        self.__from_ = SMSSender.__from
        if request:
            self.__body = "Dear {} user, your user id: {}. Your requested class {}-{} for {} has been added. " \
                          "I have got you with your classes, 🤝. Cheers!"\
                            .format(APP_NAME, user_id, subject_name, class_num_5_digit, term_name)
        elif dev:
            self.__to = SMSSender.__dev_num
            self.__body = dev_msg
        else:
            self.__body = "Dear {} user, your requested class {} - {} for {} is now OPEN ✅. Good Luck!"\
                            .format(APP_NAME, subject_name, class_num_5_digit, term_name)

    def send(self):
        self.__client.api.account.messages.create(to=self.__to, from_=self.__from, body=self.__body)
