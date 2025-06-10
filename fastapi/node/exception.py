from fastapi import status
from fastapi_basic.exception.base_exception import InternalBaseException

class NodeSavedFailedException(InternalBaseException):
    code = "node_saved_failed"
    message = "node saved failed"

    def __init__(self, message: str = None, **kwargs):
        _message = f'{self.message}, {message}' if message else self.message
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, self.code, _message, **kwargs)

class NodeNotFoundException(InternalBaseException):
    code = "node_not_found"
    message = "node not found"

    def __init__(self, message: str = None, **kwargs):
        _message = f'{self.message}, {message}' if message else self.message
        super().__init__(status.HTTP_404_NOT_FOUND, self.code, _message, **kwargs)