from abc import abstractmethod
from logging import Logger
from typing import Dict

from connect.client import ConnectClient
from connect.eaas.extension import ProcessingResponse
from connect.toolkit.requests import RequestBuilder


class Flow:
    def __init__(self, client: ConnectClient, logger: Logger, config: Dict[str, str]):
        self._client = client
        self._logger = logger
        self._config = config

    @property
    def client(self) -> ConnectClient:
        return self._client

    @property
    def logger(self) -> Logger:
        return self._logger

    @property
    def config(self) -> Dict[str, str]:
        return self._config

    @abstractmethod
    def process(self, request: RequestBuilder) -> ProcessingResponse:  # pragma: no cover
        """
        Process the incoming request.

        :param request: The incoming request dictionary.
        :return: ProcessingResponse
        """
