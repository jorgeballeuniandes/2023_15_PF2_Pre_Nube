class ApiError(Exception):
    code = 422
    description = "Default message"

class InvalidDates(ApiError):
    code = 412
    description = "Invalid dates"

class IncompleteParams(ApiError):
    code = 400
    description = "Bad request"

class InvalidParams(ApiError):
    code = 400
    description = "Bad request"

class Unauthorized(ApiError):
    code = 401
    description = "Unauthorized"

class InterviewNotFoundError(ApiError):
    code = 404
    description = "Interview does not exist"

class ParentNotFoundError(ApiError):
    code = 404
    description = ""

class ExternalError(ApiError):
    code = 422 # Default
    description = "External error"

    def __init__(self, code):
        self.code = code

