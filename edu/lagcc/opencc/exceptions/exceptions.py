
class DuplicatePhoneNumber(Exception):
    """Exception raised when account with the given phone number exists.
    Attributes:
        phone_number --> indicating the existing phone number
    """

    def __init__(self, phone_number):
        self.message = "A user associated with Phone Number: {} already exists.".format(phone_number)
        super().__init__(self.message)


class DuplicateRequest(Exception):
    """Exception raised user attempts to make a request for the same class that exists.
    Attributes:
        phone_number --> indicating the existing phone number
        subject_name --> indicates subject
        class_num_5_digit --> unique 5 digit to identify the class
    """

    def __init__(self, phone_number, subject_name, class_num_5_digit):
        self.message = "A request with Phone number: {}, Subject: {}, and Class Number: {} already exists."\
            .format(phone_number, subject_name, class_num_5_digit)
        super().__init__(self.message)
