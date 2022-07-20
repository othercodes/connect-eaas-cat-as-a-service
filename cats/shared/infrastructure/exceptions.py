from typing import Optional

from cats.shared.domain.exceptions import CatException


class CatConfigurationError(CatException):
    def __init__(self, message: str, code: str = 'none', parameter: Optional[str] = None):
        super().__init__(message, code, {'parameter': parameter})

    @property
    def parameter(self) -> Optional[str]:
        return self.additional_information.get('parameter')


class CatServerError(CatException):
    pass


class CatClientError(CatException):
    pass


class CatConnectionTimeout(CatException):
    pass
