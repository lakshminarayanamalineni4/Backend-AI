class ApplicationException(Exception):
    """
    Base exception for all business exceptions.
    """

    status_code = 400
    error = "ApplicationError"

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)