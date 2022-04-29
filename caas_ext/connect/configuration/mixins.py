from typing import Dict

from caas_ext.connect.configuration.exceptions import MissingConfigurationParameterError


class WithConfigurationHelper:
    config: Dict[str, str]

    def configuration(self, key: str) -> str:
        if key not in self.config:
            raise MissingConfigurationParameterError(
                f'Missing configuration parameter with key {key}',
                key,
            )

        return self.config.get(key)
