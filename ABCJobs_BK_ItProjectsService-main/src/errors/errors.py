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

class ProjectNotFoundError(ApiError):
    code = 404
    description = "Project does not exist"

class ExternalError(ApiError):
    code = 422 # Default
    description = "External error"

    def __init__(self, code):
        self.code = code

