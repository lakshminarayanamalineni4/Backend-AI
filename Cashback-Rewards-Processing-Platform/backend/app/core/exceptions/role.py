from app.core.exceptions.base import ApplicationException


class RoleAlreadyExistsException(ApplicationException):
    status_code = 409
    error = "RoleAlreadyExists"


class RoleNotFoundException(ApplicationException):
    status_code = 404
    error = "RoleNotFound"