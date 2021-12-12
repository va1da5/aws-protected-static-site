from lambda_function import lambda_handler


def test_lambda_handler(cf_get_unauthorized_request):
    response = lambda_handler(cf_get_unauthorized_request, None)
    assert "Unauthorized" in response["body"]


def test_lambda_handler_with_bad_credentials(
    test_store, cf_invalid_credentials_request
):
    response = lambda_handler(cf_invalid_credentials_request, None)
    assert "Unauthorized" in response["body"]


def test_lambda_handler_with_valid_credentials(
    test_store, cf_valid_credentials_request
):
    response = lambda_handler(cf_valid_credentials_request, None)
    assert "clientIp" in response
