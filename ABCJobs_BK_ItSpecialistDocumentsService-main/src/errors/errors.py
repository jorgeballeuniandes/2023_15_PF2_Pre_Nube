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

class ItSpecialistDocumentNotFoundError(ApiError):
    code = 404
    description = "It specialist does not exist"

class ItSpecialistDocumentUserIdAlreadyExistis(ApiError):
    code = 409
    description = "It Specialists with the same User Id already exists"
    
class NoFilePart(ApiError):
    code = 400
    description = "No file part"

class ExternalError(ApiError):
    code = 422 # Default
    description = "External error"

class NoSelectedFile(ApiError):
    code = 400 # Default
    description = "No selected file"

class NotAllowedFileType(ApiError):
    code = 400 # Default
    description = "Not allowed file type"

    def __init__(self, code):
        self.code = code

