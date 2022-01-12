from connect.eaas.extension import CustomEventResponse
from connect.eaas.helpers import get_environment
from connect.processors_toolkit.application.contracts import CustomEventFlow
from connect.processors_toolkit.configuration.exceptions import MissingConfigurationParameterError
from connect.processors_toolkit.configuration.mixins import WithConfigurationHelper
from connect.processors_toolkit.logger.mixins import WithBoundedLogger

from caas_ext.process.purchase import CONFIG_ASSET_ACTIVATION_TPL


class HealthCheckCustomEvent(CustomEventFlow, WithBoundedLogger, WithConfigurationHelper):
    def __init__(self, client, logger, config):
        self.client = client
        self.logger = logger
        self.config = config
        self.to_check = [
            CONFIG_ASSET_ACTIVATION_TPL,
            'CAT_API_KEY',
            'CAT_API_URL',
            'MY_APP_NAME',
        ]

    def handle(self, request: dict) -> CustomEventResponse:
        self.logger.info(get_environment())
        missing = []
        for key in self.to_check:
            try:
                self.configuration(key)
            except MissingConfigurationParameterError as e:
                missing.append(e.parameter)

        if len(missing) > 0:
            code = 'INVALID_CONFIGURATION'
            message = 'Invalid configuration.'
            details = [f'Missing configuration {key} parameter.' for key in missing]

        else:
            code = 'CONFIGURATION_OK'
            message = 'The configuration is correct.'
            details = []

        return CustomEventResponse.done(
            http_status=200,
            body={'code': code, 'message': message, 'details': details},
        )
