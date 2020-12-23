
from os import environ
from twilio.rest import Client


class SMSSender:

    __account_sid = environ["TWILIO_ACCOUNT_SID"]
    __auth_token = environ["TWILIO_AUTH_TOKEN"]
    __from = environ["TWILIO_NUMBER"]

    def __init__(self, phone, subject, class_num_5_digit, term, is_first=False):
        self.__client = Client(SMSSender.__account_sid, SMSSender.__auth_token)
        self.__to = "+1"+str(phone)
        self.__from_ = SMSSender.__from
        if is_first:
            self.__body = "Dear user, thank you for choosing to use OpenCC to get notified as soon as " \
                          "your requested classes become open. I have got you with your classes, 🤝. Cheers!"
        else:
            self.__body = "Dear OpenCC user, your requested class {} - {} for {} is now OPEN ✅. Good Luck!"\
                            .format(subject, class_num_5_digit, term)

    def send(self):
        self.__client.api.account.messages.create(to=self.__to, from_=self.__from, body=self.__body)
