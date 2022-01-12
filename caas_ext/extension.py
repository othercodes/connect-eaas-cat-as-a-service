# -*- coding: utf-8 -*-
#
# Copyright (c) 2021, Unay Santisteban
# All rights reserved.
#
from typing import Dict, Type

from connect.processors_toolkit.application import Application, Dependencies
from connect.processors_toolkit.application.dispatcher import WithDispatcher

from cats.orders.infrastructure.http import HTTPOrderRepository

from caas_ext.process.purchase import PurchaseFlow
from caas_ext.custom_events.health_check import HealthCheckCustomEvent


class CatExtension(Application, WithDispatcher):
    def routes(self) -> Dict[str, Type]:
        return {
            'product.custom-event.health-check': HealthCheckCustomEvent,
            'asset.process.purchase': PurchaseFlow,
        }

    def dependencies(self) -> Dependencies:
        dependencies = Dependencies()
        dependencies.to_class('order_repository', HTTPOrderRepository)

        return dependencies

    def process_asset_purchase_request(self, request):
        return self.dispatch_process(request)

    def process_asset_change_request(self, request):
        return self.dispatch_process(request)

    def process_asset_cancel_request(self, request):
        return self.dispatch_process(request)

    def validate_asset_purchase_request(self, request):
        return self.dispatch_validation(request)

    def validate_asset_change_request(self, request):
        return self.dispatch_validation(request)

    def execute_product_action(self, request):
        return self.dispatch_action(request)

    def process_product_custom_event(self, request):
        return self.dispatch_custom_event(request)
