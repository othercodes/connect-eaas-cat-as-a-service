from logging import Logger
from typing import Dict

from connect.client import ConnectClient
from connect.eaas.extension import ValidationResponse
from connect.processors_toolkit.application.contracts import ValidationFlow
from connect.processors_toolkit.requests import RequestBuilder

from caas_ext.services.connect.api.mixins import WithAssetHelper
from caas_ext.services.connect.configuration.mixins import WithConfigurationHelper
from caas_ext.messages import (
    HIGH_LEVEL_OPERATION_START,
    BUSINESS_TRANSACTION_START,
    BUSINESS_TRANSACTION_END_OK,
    HIGH_LEVEL_OPERATION_END_OK,
)
from caas_ext.services.providers import Observer


class ValidatePurchaseFlow(ValidationFlow, WithAssetHelper, WithConfigurationHelper):
    def __init__(
            self,
            client: ConnectClient,
            logger: Logger,
            config: Dict[str, str],
            ot_observer: Observer,
    ):
        self.client = client
        self.logger = logger
        self.config = config
        self.observer = ot_observer

    def validate(self, request: RequestBuilder) -> ValidationResponse:
        with self.observer.tracer.start_as_current_span('connect.validation.purchase'):
            self.logger.info(HIGH_LEVEL_OPERATION_START.format(
                request_type=request.type(),
                request_status=request.status(),
                actor_id=request.asset().asset_tier_customer("id"),
                actor_type=request.asset().asset_tier_customer("type"),
            ))

            with self.observer.tracer.start_as_current_span("transaction.validate_order_parameters"):
                self.logger.info(BUSINESS_TRANSACTION_START.format(
                    process_name="creating sub account in Zoom",
                    actor_id=request.asset().asset_tier_customer("id"),
                    actor_type=request.asset().asset_tier_customer("type"),
                ))

                self.logger.info("Purchase order parameters are valid!.")

                self.logger.info(BUSINESS_TRANSACTION_END_OK.format(
                    process_name="creating sub account in Zoom",
                    actor_id=request.asset().asset_tier_customer("id"),
                    actor_type=request.asset().asset_tier_customer("type"),
                ))

            self.logger.info(HIGH_LEVEL_OPERATION_END_OK.format(
                request_type=request.type(),
                request_status=request.status(),
                actor_id=request.asset().asset_tier_customer("id"),
                actor_type=request.asset().asset_tier_customer("type"),
            ))

        return ValidationResponse.done(request.raw())
