from logging import Logger
from typing import Dict

from connect.client import ConnectClient
from connect.eaas.extension import ProcessingResponse
from connect.processors_toolkit.application.contracts import ProcessingFlow
from connect.processors_toolkit.requests import RequestBuilder
from opentelemetry import baggage

from caas_ext.services.connect.api.mixins import WithAssetHelper
from caas_ext.services.connect.configuration.mixins import WithConfigurationHelper
from caas_ext.messages import (
    HIGH_LEVEL_OPERATION_START,
    BUSINESS_TRANSACTION_START,
    BUSINESS_TRANSACTION_END_OK,
    HIGH_LEVEL_OPERATION_END_OK,
)
from caas_ext.services.connect.sources import ConnectSubscriptionSource
from caas_ext.services.providers import Observer
from cats.shared.domain.models import ID
from cats.subscriptions.domain.contracts import SubscriptionRepository


class CancelFlow(ProcessingFlow, WithAssetHelper, WithConfigurationHelper):
    def __init__(
            self,
            client: ConnectClient,
            logger: Logger,
            config: Dict[str, str],
            subscription_repository: SubscriptionRepository,
            ot_observer: Observer,
    ):
        self.client = client
        self.logger = logger
        self.config = config
        self.observer = ot_observer
        self.subscription_repository = subscription_repository

    def process(self, request: RequestBuilder) -> ProcessingResponse:
        with self.observer.tracer.start_as_current_span('connect.process.cancel') as span:
            parent_ctx = baggage.set_baggage("context", "parent")
            self.logger.info(HIGH_LEVEL_OPERATION_START.format(
                request_type=request.type(),
                request_status=request.status(),
                actor_id=request.asset().asset_tier_customer("id"),
                actor_type=request.asset().asset_tier_customer("type"),
            ))

            with self.observer.tracer.start_as_current_span("transaction.cancel_subscription"):
                self.logger.info(BUSINESS_TRANSACTION_START.format(
                    process_name="cancelling subscription in Cat Service",
                    actor_id=request.asset().asset_tier_customer("id"),
                    actor_type=request.asset().asset_tier_customer("type"),
                ))

                source = ConnectSubscriptionSource(request)
                self.subscription_repository.delete(ID(source.id()))

                self.logger.info(BUSINESS_TRANSACTION_END_OK.format(
                    process_name="cancelling subscription in Cat Service",
                    actor_id=request.asset().asset_tier_customer("id"),
                    actor_type=request.asset().asset_tier_customer("type"),
                ))

            self.logger.info(HIGH_LEVEL_OPERATION_END_OK.format(
                request_type=request.type(),
                request_status=request.status(),
                actor_id=request.asset().asset_tier_customer("id"),
                actor_type=request.asset().asset_tier_customer("type"),
            ))

        return ProcessingResponse.done()
