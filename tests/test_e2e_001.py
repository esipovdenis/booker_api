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

    @allure.title("TC_E2E_001 — Полный цикл бронирования")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_e2e_001(self, auth_token):
        # Шаг 1 — токен получен
        assert auth_token is not None, "Токен авторизации не получен"

        # Шаг 2 — создать бронь
        r = booking_api.create_booking(test_data["valid_booking"])
        booking_api.check_status_code(r, 200)
        booking_api.check_booking_id_exists(r)
        booking_id = r.json()["bookingid"]

        # Шаг 3 — получить бронь
        r = booking_api.get_booking(booking_id)
        booking_api.check_status_code(r, 200)
        booking_api.check_firstname(r, "John")

        # Шаг 4 — валидация схемы
        booking_api.validate_schema(r, BOOKING_SCHEMA)

        # Шаг 5 — обновить бронь
        r = booking_api.update_booking(booking_id, test_data["updated_booking"], auth_token)
        booking_api.check_status_code(r, 200)
        booking_api.check_firstname(r, "Updated")

        # Шаг 6 — проверить обновление
        r = booking_api.get_booking(booking_id)
        booking_api.check_firstname(r, "Updated")

        # Шаг 7 — частичное обновление
        r = booking_api.patch_booking(booking_id, {"totalprice": 200}, auth_token)
        booking_api.check_status_code(r, 200)
        booking_api.check_totalprice(r, 200)
        booking_api.check_lastname(r, "Doe")

        # Шаг 8 — удалить бронь
        r = booking_api.delete_booking(booking_id, auth_token)
        booking_api.check_status_code(r, 201)

        # Шаг 9 — проверить удаление
        r = booking_api.get_booking(booking_id)
        booking_api.check_status_code(r, 404)