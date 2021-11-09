from fastapi import HTTPException as HTTPException

class APIException(HTTPException):
    default_message = "Internal Server Error"
    default_code = "internal_error"
    status_code = 500

    def __init__(self, detail=None, headers=None):
        if detail is None:
            detail = {
                'error': self.default_message,
                'code': self.default_code
            }
        super(APIException, self).__init__(
            status_code=self.status_code, detail=detail, headers=headers
        )


class NotFound(APIException):
    default_message = "Object Not Found"
    default_code = "object_not_found"
    status_code = 404


