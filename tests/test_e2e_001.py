from jsonschema import validate
import pytest
import requests
import allure
from schemas import BOOKING_SCHEMA

BASE_URL = "https://restful-booker.herokuapp.com"

@allure.feature("Booking")
@allure.story("Полный цикл бронирования: авторизация → создание → обновление → удаление")
class TestBooking:

    @allure.title("Получить токен авторизации")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_token(self, auth_token):
        with allure.step("Проверяем что токен получен"):
            assert auth_token is not None

    @allure.title("Создать новую бронь")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_booking_id(self, create_booking_id):
        with allure.step("Проверяем что booking_id получен"):
            assert create_booking_id is not None

    @allure.title("Получить бронь по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_booking_id(self, create_booking_id):
        with allure.step("Формируем URL с booking_id"):
            url = f"{BASE_URL}/booking/{create_booking_id}"
        with allure.step("Отправляем GET запрос"):
            r = requests.get(url)
        with allure.step("Проверяем статус код"):
            assert r.status_code == 200
        with allure.step("Проверяем firstname == John"):
            data = r.json()
            assert data["firstname"] == "John"

    @allure.title("Валидировать схему ответа")
    @allure.severity(allure.severity_level.NORMAL)
    def test_validate(self, create_booking_id):
        with allure.step("Формируем URL с booking_id"):
            url = f"{BASE_URL}/booking/{create_booking_id}"

        with allure.step("Отправляем GET запрос"):
            r = requests.get(url)

        with allure.step("Валидируем схему ответа"):
            data = r.json()
            validate(instance=data, schema=BOOKING_SCHEMA)

    @allure.title("Обновить бронь (полное обновление)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update(self, auth_token, create_booking_id):
        with allure.step("Формируем URL с booking_id"):
            url = f"{BASE_URL}/booking/{create_booking_id}"

        with allure.step("Подготавливаем payload с обновлёнными данными"):
            payload = {
                "firstname": "Updated",
                "lastname": "Doe",
                "totalprice": 100,
                "depositpaid": True,
                "bookingdates": {
                    "checkin": "2026-01-01",
                    "checkout": "2026-01-05"
                }
            }

        with allure.step("Отправляем PUT запрос с токеном в cookies"):
            cookies = {"token": auth_token}
            r = requests.put(url, json=payload, cookies=cookies)

        with allure.step("Проверяем статус код 200"):
            assert r.status_code == 200

        with allure.step("Проверяем firstname == Updated"):
            data = r.json()
            assert data["firstname"] == "Updated"

    @allure.title("Проверить обновление")
    @allure.severity(allure.severity_level.NORMAL)
    def test_verify_update(self, create_booking_id):
        with allure.step("Подготавливаем URL бронирования по ID"):
            url = f"{BASE_URL}/booking/{create_booking_id}"
            r = requests.get(url)
        with allure.step("Проверяем, что status_code == 200"):
            assert r.status_code == 200
            data = r.json()
        with allure.step("Проверяем firstname == Updated"):
            assert data["firstname"] == "Updated"

    @allure.title("Частично обновить бронь")
    @allure.severity(allure.severity_level.NORMAL)
    def test_patch_task(self, auth_token, create_booking_id):
        with allure.step("Создаём URL для запроса бронирования по ID"):
            url = f"{BASE_URL}/booking/{create_booking_id}"
            payload = {"totalprice": 200}
            cookies = {"token": auth_token}
            r = requests.patch(url, json=payload, cookies=cookies)
        with allure.step("Проверяем, что status_code == 200"):
            assert r.status_code == 200
        data = r.json()
        with allure.step("Проверяем, что totalprice == 200"):
            assert data["totalprice"] == 200
        with allure.step("Проверяем, что lastname == Doe"):
            assert data["lastname"] == "Doe"

    @allure.title("Удалить бронь")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_task(self, auth_token, create_booking_id):
        with allure.step("Получаем endpoint бронирования по ID"):
            url = f"{BASE_URL}/booking/{create_booking_id}"
            cookies = {"token": auth_token}
        with allure.step("Отправляем DELETE-запрос с авторизационным токеном в cookies"):
            r = requests.delete(url, cookies=cookies)
        with allure.step("Проверяем, что status_code == 201"):
            assert r.status_code == 201

    @allure.title("Проверить удаление")
    @allure.severity(allure.severity_level.NORMAL)
    def test_verify_delete(self, create_booking_id):
        with allure.step("Формируем URL для обращения к бронированию по ID"):
            url = f"{BASE_URL}/booking/{create_booking_id}"
        with allure.step("Отправляем GET запрос"):
            r = requests.get(url)
        with allure.step("Проверяем, что status_code == 404"):
            assert r.status_code == 404

    @allure.title("Проверить время ответа")
    @allure.severity(allure.severity_level.MINOR)
    def test_response_time(self,create_booking_id):
        with allure.step("Формируем URL с booking_id"):
            url = f"{BASE_URL}/booking/{create_booking_id}"
        with allure.step("Отправляем GET запрос"):
            r = requests.get(url)
        with allure.step("Проверяем, что время ответа меньше 2 секунд"):
            assert r.elapsed.total_seconds() < 2.0

    @allure.title("Проверить заголовок ответа")
    @allure.severity(allure.severity_level.MINOR)
    def test_response_headers(self, create_booking_id):
        with allure.step("Формируем URL с booking_id"):
            url = f"{BASE_URL}/booking/{create_booking_id}"
        with allure.step("Отправляем GET запрос"):
            r = requests.get(url)
        with allure.step("Проверяем Content-Type == text/plain"):
            assert "text/plain" in r.headers["Content-Type"]








