
class DuplicatePhoneNumber(Exception):
    """Exception raised when account with the given phone number exists.
    Attributes:
        phone_number -- indicating the existing phone number
        message -- explanation of the error
    """

    def __init__(self, phone_number, message):
        self.phone_number = phone_number
        self.message = message
        super().__init__(self.message)
