from connect.processors_toolkit.application import Dependencies

from cats.orders.infrastructure.http import HTTPOrderRepository


class DependencyProvider:
    def dependencies(self) -> Dependencies:
        dependencies = Dependencies()
        dependencies.to_class('order_repository', HTTPOrderRepository)

        return dependencies
