from connect.eaas.extension import ProcessingResponse
from connect.toolkit.requests import RequestBuilder

from caas_ext.connect.sources import ConnectOrderSource
from caas_ext.flows import Flow
from cats_as_a_service.orders.domain.services import order_builder


class PurchaseFlow(Flow):
    def process(self, request: RequestBuilder) -> ProcessingResponse:
        self.logger.info(f"Processing purchase request with id {request.id()}")

        # request decomposition (with parameter validation)
        order = order_builder(ConnectOrderSource(request))

        print(order)

        return ProcessingResponse.done()
