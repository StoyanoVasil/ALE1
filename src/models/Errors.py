class NotAProperPredicateException(Exception):
    def __init__(self, message):
        self.message = message


class BinaryOperatorException(Exception):
    def __init__(self, message):
        self.message = message

class OperatorException(Exception):
    def __init__(self, message):
        self.message = message
