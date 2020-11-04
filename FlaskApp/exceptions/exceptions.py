class UserExistsError(BaseException):
    pass


class EmailExistsError(BaseException):
    pass


class InvalidLoginError(BaseException):
    pass


class SectionNotFoundError(BaseException):
    pass


class FileFormatError(BaseException):
    pass
