from typing import Optional


class CatAsAServiceException(Exception):
    def __init__(self, message: str, code: str = 'none', additional_information=None):
        if additional_information is None:
            additional_information = {}
        self.message = message
        self.code = code
        self.additional_information = additional_information

        super().__init__(self.message)


class ConfigurationError(CatAsAServiceException):
    def __init__(self, message: str, code: str = 'none', parameter: Optional[str] = None):
        super().__init__(message, code, {'parameter': parameter})

    def parameter(self) -> Optional[str]:
        return self.additional_information.get('parameter')


class CatAsAServiceServerError(CatAsAServiceException):
    pass


class CatAsAServiceClientError(CatAsAServiceException):
    pass
