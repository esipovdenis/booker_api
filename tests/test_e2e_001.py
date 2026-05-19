from jsonschema import validate
import pytest
import allure
import json
import os
from schemas import BOOKING_SCHEMA
from config import BASE_URL
from api_client.booking_api import BookingApi

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT_DIR, "data", "test_data.json")) as f:
    test_data = json.load(f)

booking_api = BookingApi()


@allure.feature("Booking")
@allure.story("Полный цикл бронирования: авторизация → создание → обновление → удаление")
class TestBooking:

    @allure.title("Получить токен авторизации")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_token(self, auth_token):
        assert auth_token is not None

    @allure.title("Создать новую бронь")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_booking_id(self, auth_token):
        r = booking_api.create_booking(test_data["valid_booking"])
        assert r.status_code == 200
        data = r.json()
        assert "bookingid" in data

    @allure.title("Получить бронь по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_booking_id(self, auth_token):
        r_create = booking_api.create_booking(test_data["valid_booking"])
        booking_id = r_create.json()["bookingid"]
        r = booking_api.get_booking(booking_id)
        assert r.status_code == 200
        data = r.json()
        assert data["firstname"] == "John"

    @allure.title("Валидировать схему ответа")
    @allure.severity(allure.severity_level.NORMAL)
    def test_validate(self, auth_token):
        r_create = booking_api.create_booking(test_data["valid_booking"])
        booking_id = r_create.json()["bookingid"]
        r = booking_api.get_booking(booking_id)
        data = r.json()
        validate(instance=data, schema=BOOKING_SCHEMA)

    @allure.title("Обновить бронь (полное обновление)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update(self, auth_token):
        r_create = booking_api.create_booking(test_data["valid_booking"])
        booking_id = r_create.json()["bookingid"]
        r = booking_api.update_booking(booking_id, test_data["updated_booking"], auth_token)
        assert r.status_code == 200
        data = r.json()
        assert data["firstname"] == "Updated"

    @allure.title("Проверить обновление")
    @allure.severity(allure.severity_level.NORMAL)
    def test_verify_update(self, auth_token):
        r_create = booking_api.create_booking(test_data["valid_booking"])
        booking_id = r_create.json()["bookingid"]
        booking_api.update_booking(booking_id, test_data["updated_booking"], auth_token)
        r = booking_api.get_booking(booking_id)
        assert r.status_code == 200
        data = r.json()
        assert data["firstname"] == "Updated"

    @allure.title("Частично обновить бронь")
    @allure.severity(allure.severity_level.NORMAL)
    def test_patch_task(self, auth_token):
        r_create = booking_api.create_booking(test_data["valid_booking"])
        booking_id = r_create.json()["bookingid"]
        r = booking_api.patch_booking(booking_id, {"totalprice": 200}, auth_token)
        assert r.status_code == 200
        data = r.json()
        assert data["totalprice"] == 200
        assert data["lastname"] == "Doe"

    @allure.title("Удалить бронь")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_task(self, auth_token):
        r_create = booking_api.create_booking(test_data["valid_booking"])
        booking_id = r_create.json()["bookingid"]
        r = booking_api.delete_booking(booking_id, auth_token)
        assert r.status_code == 201

    @allure.title("Проверить удаление")
    @allure.severity(allure.severity_level.NORMAL)
    def test_verify_delete(self, auth_token):
        r_create = booking_api.create_booking(test_data["valid_booking"])
        booking_id = r_create.json()["bookingid"]
        booking_api.delete_booking(booking_id, auth_token)
        r = booking_api.get_booking(booking_id)
        assert r.status_code == 404

    @allure.title("Проверить время ответа")
    @allure.severity(allure.severity_level.MINOR)
    def test_response_time(self, auth_token):
        r_create = booking_api.create_booking(test_data["valid_booking"])
        booking_id = r_create.json()["bookingid"]
        r = booking_api.get_booking(booking_id)
        assert r.elapsed.total_seconds() < 2.0

    @allure.title("Проверить заголовок ответа")
    @allure.severity(allure.severity_level.MINOR)
    def test_response_headers(self, auth_token):
        r_create = booking_api.create_booking(test_data["valid_booking"])
        booking_id = r_create.json()["bookingid"]
        r = booking_api.get_booking(booking_id)
        assert "application/json" in r.headers["Content-Type"]