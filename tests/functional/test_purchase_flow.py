from connect.devops_testing import fixtures, asserts
from connect.processors_toolkit.application import Dependencies

from caas_ext.extension import CatAsAServiceExtension
from cats.orders.domain.contracts import OrderRepository
from cats.orders.domain.models import Order


class FakeOrderRepository(OrderRepository):
    def save(self, order: Order) -> None:
        assert isinstance(order, Order)


def test_processor_should_approve_request(logger, response_factory, sync_client_factory, test_path):
    dependencies = Dependencies()
    dependencies.to_instance('order_repository', FakeOrderRepository())

    builder = fixtures.make_request_builder().from_file(test_path('/functional/test_purchase_data/request.json'))

    on_server = builder.build()
    initial = builder.build()

    builder.with_asset_param('CAT_SUBSCRIPTION_ID', 'AS-8790-0160-2196')
    after_update = builder.build()

    client = sync_client_factory([
        response_factory(value=on_server),  # get request by id to check difference
        response_factory(value=after_update),  # response on post request asset params
    ])

    config = {'ACTIVATION_TPL': 'TPL-123-456-789'}

    extension = CatAsAServiceExtension(client, logger, config, dependencies)
    response = extension.process_asset_purchase_request(initial)

    asserts.task_response_status(response, 'success')
