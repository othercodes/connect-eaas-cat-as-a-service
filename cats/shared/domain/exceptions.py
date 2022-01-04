class CatAsAServiceException(Exception):
    def __init__(self, message: str, code: str = 'none', additional_information=None):
        if additional_information is None:
            additional_information = {}
        self.message = message
        self.code = code
        self.additional_information = additional_information

        super().__init__(self.message)
