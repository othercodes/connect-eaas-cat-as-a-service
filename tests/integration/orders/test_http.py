from cats_as_a_service.orders.domain.services import order_builder
from cats_as_a_service.orders.infrastructure.http import HTTPOrderRepository


def test_should_successfully_place_order_adding_items(fake_order_source, config):
    order = order_builder(fake_order_source({
        'id': 'AS-0000-0000-0000',
        'order_type': 'ASC',
        'categories': [14, 15],
        'amount': 3,
    }))

    repository = HTTPOrderRepository(api_key=config['api_key'], api_url=config['api_url'])
    repository.save(order)

    assert int(repository._get_favourites(order.id.value).headers.get('pagination-count', 0)) == 3


def test_should_successfully_place_order_removing_items(fake_order_source, config):
    order = order_builder(fake_order_source({
        'id': 'AS-0000-0000-0000',
        'order_type': 'ASC',
        'categories': [14, 15],
        'amount': 0,
    }))

    repository = HTTPOrderRepository(api_key=config['api_key'], api_url=config['api_url'])
    repository.save(order)

    assert int(repository._get_favourites(order.id.value).headers.get('pagination-count', 0)) == 0
