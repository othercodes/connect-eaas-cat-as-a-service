from connect.eaas.extension import CustomEventResponse
from connect.processors_toolkit.application.contracts import CustomEventFlow
from connect.processors_toolkit.logger.mixins import WithBoundedLogger

from caas_ext.services.connect.configuration.exceptions import MissingConfigurationParameterError
from caas_ext.services.connect.configuration.mixins import WithConfigurationHelper

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
        configuration = self.validate_configuration()

        sections = [
            configuration
        ]

        service = 'ok'
        for section in sections:
            if 'invalid' in section['status']:
                service = 'failure'

        return CustomEventResponse.done(
            http_status=200,
            body={
                'service': service,
                'configuration': configuration
            },
        )

    def validate_configuration(self) -> dict:
        missing = []
        for key in self.to_check:
            try:
                self.configuration(key)
            except MissingConfigurationParameterError as e:
                missing.append(e.parameter)

        if len(missing) > 0:
            return {
                'status': 'invalid',
                'issues': [f'Missing configuration {key} parameter.' for key in missing],
            }

        return {
            'status': 'valid',
            'issues': [],
        }
