
class UserExistsException(Exception):
    """
    Exception raised when account with the given phone number exists.
    Attributes:
        phone_number --> indicating the existing user with this phone number
    """

    def __init__(self, phone_number):
        self.message = "A user associated with Phone Number: {} already exists.".format(phone_number)
        super().__init__(self.message)


class DuplicateRequestException(Exception):
    """
    Exception raised user attempts to make a request for the same class that exists.
    Attributes:
        phone_number --> indicating the existing phone number
        subject_name --> indicates subject
        class_num_5_digit --> unique 5 digit to identify the class
    """

    def __init__(self, phone_number, subject_name, class_num_5_digit):
        self.message = "A request with Phone number: {}, Subject: {}, and Class Number: {} already exists."\
            .format(phone_number, subject_name, class_num_5_digit)
        super().__init__(self.message)


class NotFoundException(Exception):
    """
    Exception raised when a record is not found.
    Attributes:
        message --> a message to get hint of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NotifyDeveloperException(Exception):
    """
    Exception raised when cause is completely unknown and/or database is down, and/or application is down.
    Attributes:
        error_type --> indicating the existing phone number
        partial_message --> a message to get hint of the error
    """

    def __init__(self, error_type, partial_message):
        self.message = "Dev: Exception of type '{0}' with arguments:\n{1!r}".format(error_type, partial_message)
        super().__init__(self.message)
