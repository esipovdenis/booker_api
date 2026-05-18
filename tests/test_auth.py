import allure
import requests
import json
import os

BASE_URL = "https://restful-booker.herokuapp.com"
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT_DIR, "data", "test_data.json")) as f:
    test_data = json.load(f)

@allure.feature("Auth")
@allure.story("Авторизация с валидными и невалидными данными")
class TestAuth:

    @allure.title("TC_AUTH_001 - Получение токена с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_001_valid_login(self):
        url = f"{BASE_URL}/auth"
        payload = {"username": "admin", "password": "password123"}
        with allure.step("Отправляем POST /auth с валидными данными"):
            r = requests.post(url, json=payload)
        with allure.step("Проверяем статус код 200 и наличие токена"):
            assert r.status_code == 200
            data = r.json()
            assert "token" in data
        with allure.step("Проверяем, что token не пустой"):
            assert len(data["token"]) > 0

    @allure.title("TC_AUTH_002 - Получение токена с неверным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_002_login_wrong_password(self):
        url = f"{BASE_URL}/auth"
        payload = {"username": "admin", "password": "password555"}
        with allure.step("Отправляем POST с неверным паролем"):
            r = requests.post(url, json=payload)
        with allure.step("Проверяем ответ сервера"):
            assert r.status_code == 200
            data = r.json()
            assert "token" not in data
            assert "reason" in data

    @allure.title("TC_AUTH_003 - Получение токена с несуществующим пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_003_login_fake_user(self):
        url = f"{BASE_URL}/auth"
        payload = {"username": "anton", "password": "password123"}
        with allure.step("Отправляем POST с несуществующем пользователем"):
            r = requests.post(url, json=payload)
        with allure.step("Проверяем что токен отсутствует и есть reason"):
            assert r.status_code == 200
            data = r.json()
            assert "token" not in data
            assert "reason" in data

    @allure.title("TC_AUTH_004 - Использование токена для защищённого запроса")
    @allure.severity(allure.severity_level.NORMAL)
    def test_004_use_valid_token(self):
        r_auth = requests.post(f"{BASE_URL}/auth",
                               json={"username": "admin", "password": "password123"})
        token = r_auth.json()["token"]

        payload = test_data["valid_booking"]
        r_booking = requests.post(f"{BASE_URL}/booking", json=payload)
        bookingid = r_booking.json()["bookingid"]

        updated_payload = test_data["valid_booking"].copy()
        updated_payload["firstname"] = "Updated"

        cookies = {"token": token}
        with allure.step("Отправляем PUT запрос с валидным токеном"):
            r = requests.put(f"{BASE_URL}/booking/{bookingid}",
                             json=updated_payload,
                             cookies=cookies)

        with allure.step("Проверяем что токен работает и статус 200"):
            assert r.status_code == 200

        with allure.step("Проверяем что бронь обновилась"):
            data = r.json()
            assert data["firstname"] == "Updated"

    @allure.title("TC_AUTH_005 - Использование неверного токена")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_005_update_invalid_token(self):
        with allure.step("Отправляем PUT запрос с невалидным токеном"):
            payload = test_data["valid_booking"]
            r_task = requests.post(f"{BASE_URL}/booking", json=payload)
            cookies = {"token": "this_is_not_a_real_token"}
        with allure.step("Отправляем PUT запрос с невалидным токеном"):
            bookingid = r_task.json()["bookingid"]
            r = requests.put(f"{BASE_URL}/booking/{bookingid}",
                             json=payload,  # ← вместо большого словаря
                             cookies=cookies)
        with allure.step("Проверяем что сервер вернул 403 Forbidden"):
            assert r.status_code == 403

    @allure.title("TC_AUTH_006 - Запрос без токена к защищённому эндпоинту")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_006_update_no_token(self):
        with allure.step("Отправляем PUT запрос без токена"):
            payload = test_data["valid_booking"]
            r_task = requests.post(f"{BASE_URL}/booking",json=payload)
            bookingid = r_task.json()["bookingid"]

            r = requests.put(f"{BASE_URL}/booking/{bookingid}",
                         json=payload)
        with allure.step("Проверяем что сервер вернул 403 Forbidden"):
            assert r.status_code == 403

    @allure.title("TC_AUTH_007 - Валидация формата токена")
    @allure.severity(allure.severity_level.NORMAL)
    def test_007_token_format(self):
        url = f"{BASE_URL}/auth"
        payload = {"username": "admin", "password": "password123"}
        with allure.step("Отправляем POST /auth с валидными данными"):
            r = requests.post(url, json=payload)
        with allure.step("Проверяем статус код 200 и наличие токена"):
            assert r.status_code == 200
            data = r.json()
            assert "token" in data
        with allure.step("Проверяем, что token не пустой"):
            assert len(data["token"]) > 0
        with allure.step("Проверяем, что token является строкой"):
            assert isinstance(data["token"], str)


    @allure.title("TC_AUTH_008 - Повторное получение токена (идемпотентность)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_008_token_idempotent(self):
        url = f"{BASE_URL}/auth"
        payload = {"username": "admin", "password": "password123"}
        with allure.step("Отправляем POST /auth с валидными данными"):
            r1 = requests.post(url, json=payload)
        with allure.step("Проверяем статус код 200 и наличие токена"):
            assert r1.status_code == 200
            data = r1.json()
            assert "token" in data
        with allure.step("Отправляем POST /auth с валидными данными"):
            r2 = requests.post(url, json=payload)
        with allure.step("Проверяем статус код 200 и наличие токена"):
            assert r2.status_code == 200
            data = r2.json()
            assert "token" in data
        token_1 = r1.json()["token"]
        token_2 = r2.json()["token"]
        with allure.step("Проверяем первый токен — строка и не пустой"):
            assert len(token_1) > 0
            assert isinstance(token_1, str)
        with allure.step("Проверяем второй токен — строка и не пустой"):
            assert len(token_2) > 0
            assert isinstance(token_2, str)



