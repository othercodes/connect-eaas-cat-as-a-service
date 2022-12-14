# -*- coding: utf-8 -*-
#
# Copyright (c) 2021, Unay Santisteban
# All rights reserved.
#
import os
from logging import LoggerAdapter
from typing import Dict, Type, Union, Optional

import toml
from connect.client import AsyncConnectClient, ConnectClient
from connect.processors_toolkit.application import Application, Dependencies
from connect.processors_toolkit.application.dispatcher import WithDispatcher

from caas_ext.process.cancel import CancelFlow
from caas_ext.validations.purchase import ValidatePurchaseFlow
from cats.orders.infrastructure.http import HTTPOrderRepository

from caas_ext.process.purchase import PurchaseFlow
from caas_ext.custom_events.health_check import HealthCheckCustomEvent
from caas_ext.services.providers import (
    provide_ot_span_exporter,
    provide_ot_span_processor,
    provide_ot_tracer,
    provide_ot_observer,
)
from cats.subscriptions.infrastructure.http import HTTPSubscriptionRepository


class CatExtension(Application, WithDispatcher):
    def routes(self) -> Dict[str, Type]:
        return {
            'product.custom-event.health-check': HealthCheckCustomEvent,
            'asset.process.purchase': PurchaseFlow,
            'asset.process.cancel': CancelFlow,
            'asset.validate.purchase': ValidatePurchaseFlow,
        }

    def dependencies(self) -> Dependencies:
        dependencies = Dependencies()
        dependencies.to_instance('extension_name', 'cat_as_a_service')
        dependencies.to_class('order_repository', HTTPOrderRepository)
        dependencies.to_class('subscription_repository', HTTPSubscriptionRepository)
        dependencies.provider('ot_observer', provide_ot_observer)
        dependencies.provider('ot_tracer', provide_ot_tracer)
        dependencies.provider('ot_span_processor', provide_ot_span_processor)
        dependencies.provider('ot_span_exporter', provide_ot_span_exporter)

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
