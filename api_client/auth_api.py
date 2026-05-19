import allure
import requests
from config import BASE_URL


class AuthApi:

    @allure.step("POST /auth — получаем токен")
    def get_token(self, username, password):
        return requests.post(f"{BASE_URL}/auth",
                           json={"username": username,
                                 "password": password})