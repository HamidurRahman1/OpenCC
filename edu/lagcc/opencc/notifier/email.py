
import logging
import smtplib
from os import environ
from edu.lagcc.opencc.utils.util import EXCEPTION_LOGGER


class EmailNotifier:

    __user_name = environ.get("GMAIL_USER")
    __password = environ.get("GMAIL_PASS")
    __carriers = {
                "att":          "@mms.att.net",
                "tmobile":      "@tmomail.net",
                "verizon":      "@vtext.com",
                "sprint":       "@page.nextel.com"}

    def __init__(self, phone_num, carrier, message):
        self.sent_from = EmailNotifier.__user_name
        self.to = ["{}{}".format(phone_num, EmailNotifier.__carriers[carrier])]
        self.subject = "Requested class is open"
        self.body = message
        self.email_text = """\
        From: %s
        To: %s
        Subject: %s
    
        %s
        """ % (self.sent_from, ", ".join(self.to), self.subject, self.body)

    def send(self):
        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.ehlo()
            server.login(EmailNotifier.__user_name, EmailNotifier.__password)
            server.sendmail(self.sent_from, self.to, self.email_text)
            server.close()
        except Exception as ex:
            logging.getLogger(EXCEPTION_LOGGER).error(ex)
