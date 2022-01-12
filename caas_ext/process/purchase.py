from logging import Logger
from typing import Dict

from connect.client import ConnectClient
from connect.eaas.extension import ProcessingResponse
from connect.processors_toolkit.application.contracts import ProcessingFlow
from connect.processors_toolkit.api.mixins import WithAssetHelper, WithProductHelper
from connect.processors_toolkit.configuration.mixins import WithConfigurationHelper
from connect.processors_toolkit.requests import RequestBuilder

from caas_ext.connect.sources import ConnectOrderSource

from cats.orders.application.services import OrderCreator
from cats.orders.domain.contracts import OrderRepository

CONFIG_ASSET_ACTIVATION_TPL = 'SUBSCRIPTION_ACTIVATION_TPL'


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
        self.logger.info(f"Processing purchase request with id {request.id()}")

        order = self.order_creator.create(ConnectOrderSource(request))
        self.logger.info('New order with id {id} created.'.format(id=order.id.value))

        asset = request.asset()
        asset.with_asset_param('CAT_SUBSCRIPTION_ID', order.id.value)
        request.with_asset(asset)

        # commit the parameter update into connect platform
        self.update_asset_parameters_request(request)

        # approve the asset request
        self.approve_asset_request(request, self.configuration(CONFIG_ASSET_ACTIVATION_TPL))

        return ProcessingResponse.done()
