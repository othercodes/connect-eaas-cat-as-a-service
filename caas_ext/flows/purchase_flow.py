from logging import Logger
from plistlib import Dict

from connect.client import ConnectClient
from connect.eaas.extension import ProcessingResponse
from connect.processors_toolkit.requests import RequestBuilder
from connect.processors_toolkit.mixin import WithAssetHelper, WithProductHelper

from caas_ext.connect.sources import ConnectOrderSource

from cats_as_a_service.orders.application.services import OrderCreator
from cats_as_a_service.orders.domain.contracts import OrderRepository

CONFIG_ASSET_ACTIVATION_TPL = 'SUBSCRIPTION_ACTIVATION_TEMPLATE'


class PurchaseFlow(ProcessingFlow, WithAssetHelper, WithProductHelper):
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

        order_id = self.order_creator.create(ConnectOrderSource(request))

        # update the asset model parameter
        asset = request.asset()
        asset.with_asset_param('CAT_SUBSCRIPTION_ID', order_id.value)
        request.with_asset(asset)

        # commit the parameter update into connect platform
        self.update_asset_parameters_request(request)

        # approve the asset request
        self.approve_asset_request(request, self.config.get(CONFIG_ASSET_ACTIVATION_TPL))

        return ProcessingResponse.done()
