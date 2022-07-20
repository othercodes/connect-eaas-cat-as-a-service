from logging import Logger
from typing import Dict

from connect.client import ConnectClient
from connect.eaas.extension import ProcessingResponse
from connect.processors_toolkit.application.contracts import ProcessingFlow
from connect.processors_toolkit.requests import RequestBuilder

from caas_ext.connect.api.mixins import WithAssetHelper, WithProductHelper
from caas_ext.connect.configuration.exceptions import MissingConfigurationParameterError
from caas_ext.connect.configuration.mixins import WithConfigurationHelper
from caas_ext.connect.sources import ConnectOrderSource
from caas_ext.messages import (
    HIGH_LEVEL_OPERATION_START,
    BUSINESS_TRANSACTION_START,
    RESCHEDULING_PROCESS,
    BUSINESS_TRANSACTION_END_OK,
    HIGH_LEVEL_OPERATION_END_OK,
    MISSING_CONFIGURATION_PARAMETER,
)
from cats.orders.application.services import OrderCreator
from cats.orders.domain.contracts import OrderRepository
from cats.shared.infrastructure.exceptions import (
    CatConnectionTimeout,
    CatServerError,
)

CONFIG_ASSET_ACTIVATION_TPL = 'SUBSCRIPTION_ACTIVATION_TPL'
CAT_SUBSCRIPTION_ID = 'CAT_SUBSCRIPTION_ID'


class PurchaseFlow(ProcessingFlow, WithAssetHelper, WithProductHelper, WithConfigurationHelper):
    def __init__(
            self,
            client: ConnectClient,
            logger: Logger,
            config: Dict[str, str],
            order_repository: OrderRepository,
    ):
        self.client = client
        self.logger = logger
        self.config = config
        self.order_creator = OrderCreator(order_repository)

    def process(self, request: RequestBuilder) -> ProcessingResponse:
        self.logger.info(HIGH_LEVEL_OPERATION_START.format(
            request_type=request.type(),
            request_status=request.status(),
            actor_id=request.asset().asset_tier_customer("id"),
            actor_type=request.asset().asset_tier_customer("type"),
        ))

        try:
            # first retrieve the asset activation template, if not found,
            # raise an error and reschedule the request.
            asset_activation_template = self.configuration(CONFIG_ASSET_ACTIVATION_TPL)

        except MissingConfigurationParameterError as e:
            self.logger.error(MISSING_CONFIGURATION_PARAMETER.format(
                parameter=e.parameter,
            ))

            self.logger.warning(RESCHEDULING_PROCESS.format(
                timeout=3600,
                reason=str(e),
            ))
            return ProcessingResponse.slow_process_reschedule(countdown=3600)

        try:
            self.logger.info(BUSINESS_TRANSACTION_START.format(
                process_name="creating sub account in Zoom",
                actor_id=request.asset().asset_tier_customer("id"),
                actor_type=request.asset().asset_tier_customer("type"),
            ))

            order = self.order_creator.create(ConnectOrderSource(request))
            self.logger.info('New order with id {id} created.'.format(id=order.id.value))

            self.logger.info(BUSINESS_TRANSACTION_END_OK.format(
                process_name="creating sub account in Zoom",
                actor_id=request.asset().asset_tier_customer("id"),
                actor_type=request.asset().asset_tier_customer("type"),
            ))

        except (CatServerError, CatConnectionTimeout) as e:
            self.logger.warning(RESCHEDULING_PROCESS.format(
                timeout=3600,
                reason=str(e),
            ))

            return ProcessingResponse.slow_process_reschedule(countdown=3600)

        asset = request.asset()
        asset.with_asset_param(CAT_SUBSCRIPTION_ID, order.id.value)
        request.with_asset(asset)

        # commit the parameter update into connect platform
        self.update_asset_parameters_request(request)

        # approve the asset request
        self.approve_asset_request(request, asset_activation_template)

        self.logger.info(HIGH_LEVEL_OPERATION_END_OK.format(
            request_type=request.type(),
            request_status=request.status(),
            actor_id=request.asset().asset_tier_customer("id"),
            actor_type=request.asset().asset_tier_customer("type"),
        ))

        return ProcessingResponse.done()
