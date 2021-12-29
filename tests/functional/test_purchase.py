from connect.devops_testing import asserts, fixtures

from caas_ext.extension import CatAsAServiceExtension


def __test_processor_should_approve_request(sync_client_factory, logger, config):
    request = fixtures.make_request_builder()
    request.with_id('PR-7582-9599-4095-001')
    request.with_type('purchase')
    request.with_status('pending')
    request.with_asset_id('AS-7582-9599-4095')
    request.with_asset_param('CAT_SUBSCRIPTION_ID', '')
    request.with_asset_param('CATEGORIES', {
        "1": False,
        "4": True,
        "5": True,
        "7": False,
        "14": False,
        "15": False
    })
    request.with_asset_param('ORDER_TYPE', 'RANDOM')
    request.with_asset_item('PRD-568-313-088-0001', 'MPN-CAT-IMG', '10')
    request = request.build()

    client = sync_client_factory([])

    extension = CatAsAServiceExtension(client, logger, config)
    result = extension.process_asset_purchase_request(request)

    asserts.task_response_status(result, 'success')
    asserts.request_status(request, 'approved')
    asserts.asset_status(request, 'active')