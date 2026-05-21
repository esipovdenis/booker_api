import pytest
import json
import os
import allure
from api_client.auth_api import AuthApi
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(ROOT_DIR, "data", "test_data.json")) as f:
    test_data = json.load(f)

auth_api = AuthApi()

@pytest.fixture
@allure.title("Получить токен авторизации")
def auth_token():
    r = auth_api.get_token(
        test_data["credentials"]["username"],
        test_data["credentials"]["password"]
    )
    return r.json()["token"]

