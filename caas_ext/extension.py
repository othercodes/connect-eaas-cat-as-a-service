# -*- coding: utf-8 -*-
#
# Copyright (c) 2021, Unay Santisteban
# All rights reserved.
#
from connect.processors_toolkit.requests import RequestBuilder
from connect.processors_toolkit.application import Application
from connect.eaas.extension import (
    CustomEventResponse,
    ProcessingResponse,
    ProductActionResponse,
    ValidationResponse,
)


class CatAsAServiceExtension(Application):
    def process_asset_purchase_request(self, request):
        self.make('purchase_flow').process(RequestBuilder(request))

    def process_asset_change_request(self, request):
        self.logger.info(f"Obtained request with id {request['id']}")
        return ProcessingResponse.done()

    def process_asset_cancel_request(self, request):
        self.logger.info(f"Obtained request with id {request['id']}")
        return ProcessingResponse.done()

    def validate_asset_purchase_request(self, request):
        self.logger.info(f"Obtained request with id {request['id']}")
        return ValidationResponse.done(request)

    def validate_asset_change_request(self, request):
        self.logger.info(f"Obtained request with id {request['id']}")
        return ValidationResponse.done(request)

    def execute_product_action(self, request):
        self.logger.info(f"Obtained product custom action with following data: {request}")
        return ProductActionResponse.done()

    def process_product_custom_event(self, request):
        self.logger.info(f"Obtained custom event with following data: {request}")
        return CustomEventResponse.done()
