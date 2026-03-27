class BaseAppException(Exception):

    def __init__(
        self,
        message: str,
    ):
        self.message = message


class PageFetchError(BaseAppException):

    def __init__(self, message: str, status_code: int):
        super().__init__(
            message=message,
        )
        self.status_code = status_code


class PageTimeoutError(BaseException):
    pass


class PageConnectionError(BaseException):
    pass


class ValidationException(BaseException):
    pass


class DataBaseException(BaseException):
    pass


class PageInvalidURLError(BaseException):
    pass


class UniqueURLError(BaseException):
    pass


class NotFoundException(BaseException):
    pass


class BadDataException(BaseException):
    pass


class TemporaryFailException(BaseException):
    pass


class UnexpectedException(BaseException):
    pass
