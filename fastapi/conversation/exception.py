from fastapi import status
from fastapi_basic.exception.base_exception import InternalBaseException

class ConversationAlreadyExistException(InternalBaseException):
    code = "conversation_already_exist"
    message = "conversation already exists"

    def __init__(self, message: str = None, **kwargs):
        _message = f'{self.message}, {message}' if message else self.message
        super().__init__(status.HTTP_409_CONFLICT, self.code, _message, **kwargs)

class ConversationSavedFailedException(InternalBaseException):
    code = "conversation_saved_failed"
    message = "conversation saved failed"

    def __init__(self, message: str = None, **kwargs):
        _message = f'{self.message}, {message}' if message else self.message
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, self.code, _message, **kwargs)