import base64
import os
from typing import Any, Mapping, Tuple

from credentials_store import CredentialsStore
from dotenv import load_dotenv

load_dotenv()


def unauthorized() -> Mapping[str, Any]:
    return {
        "status": 401,
        "statusDescription": "Unauthorized",
        "headers": {
            "www-authenticate": [{"key": "WWW-Authenticate", "value": "Basic"}],
            "cache-control": [{"key": "Cache-Control", "value": "max-age=100"}],
            "content-type": [{"key": "Content-Type", "value": "text/html"}],
        },
        "body": "<h1>Unauthorized</h1>",
    }


def parse_credentials(auth_header: str) -> Tuple[str, str]:
    auth_string = auth_header.split(" ")[1]
    user_pass = base64.b64decode(auth_string).decode()
    user, password = user_pass.split(":")
    return user, password


def lambda_handler(event: Mapping[str, Any], context: Any) -> Mapping[str, Any]:

    credentials_file = os.getenv("CREDENTIALS_STORE")

    request = event["Records"][0]["cf"]["request"]
    headers = request["headers"]

    if headers.get("authorization") is None:
        return unauthorized()

    store = CredentialsStore(credentials_file=credentials_file)

    user, password = parse_credentials(headers["authorization"][0]["value"])

    if not store.validate(user, password):
        return unauthorized()

    return request
