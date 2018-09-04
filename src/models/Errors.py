class ParserError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


class BracketError(ParserError):
    def __init__(self, message):
        super().__init__(message)


class OperatorError(ParserError):
    def __init__(self, message):
        super().__init__(message)


class PredicateError(ParserError):
    def __init__(self, message):
        super().__init__(message)
