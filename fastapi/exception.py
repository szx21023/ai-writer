from fastapi import status
from fastapi_basic.exception.base_exception import InternalBaseException

class RequiredColumnMissingException(InternalBaseException):
    code = "required_column_missing"
    message = "required column is missing"

    def __init__(self, message: str = None, **kwargs):
        _message = f'{self.message}, {message}' if message else self.message
        super().__init__(status.HTTP_403_FORBIDDEN, self.code, _message, **kwargs)