import base64
import os

import pytest


@pytest.fixture
def cf_get_unauthorized_request():
    return {
        "Records": [
            {
                "cf": {
                    "config": {"distributionId": "EXAMPLE"},
                    "request": {
                        "uri": "/test",
                        "method": "GET",
                        "clientIp": "2001:cdba::3257:9652",
                        "headers": {
                            "user-agent": [
                                {"key": "User-Agent", "value": "test-agent"}
                            ],
                            "host": [{"key": "Host", "value": "d123.cf.net"}],
                        },
                    },
                }
            }
        ]
    }


@pytest.fixture
def cf_invalid_credentials_request(cf_get_unauthorized_request):

    request = cf_get_unauthorized_request.copy()

    auth_header = "Basic " + base64.b64encode(b"test:invalid").decode("utf-8")

    request["Records"][0]["cf"]["request"]["headers"]["authorization"] = [
        {
            "key": "Authorization",
            "value": auth_header,
        }
    ]

    return request


@pytest.fixture
def cf_valid_credentials_request(cf_get_unauthorized_request):

    request = cf_get_unauthorized_request.copy()

    auth_header = "Basic " + base64.b64encode(b"test:test").decode("utf-8")

    request["Records"][0]["cf"]["request"]["headers"]["authorization"] = [
        {
            "key": "Authorization",
            "value": auth_header,
        }
    ]

    return request


@pytest.fixture
def test_store():
    path = os.path.abspath(__file__)
    os.environ["CREDENTIALS_STORE"] = os.path.dirname(path) + "/.passwd"
