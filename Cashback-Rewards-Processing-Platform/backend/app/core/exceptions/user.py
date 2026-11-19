from app.core.exceptions.base import ApplicationException


class UserAlreadyExistsException(ApplicationException):
    status_code = 409
    error = "UserAlreadyExists"


class UserNotFoundException(ApplicationException):
    status_code = 404
    error = "UserNotFound"
