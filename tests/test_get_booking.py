import allure
import requests
import json
import os
from schemas import BOOKING_SCHEMA, BOOKINGS_LIST_SCHEMA
from jsonschema import validate

BASE_URL = "https://restful-booker.herokuapp.com"

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT_DIR, "data", "test_data.json")) as f:
    test_data = json.load(f)

@allure.feature("Booking")
@allure.story("Получение броней - GET Booking API")
class TestGetBooking:
    @allure.title("TC_GET_001 - Получение всех броней")
    @allure.severity(allure.severity_level.NORMAL)
    def test_001_get_all_tasks(self):
        r = requests.get(f"{BASE_URL}/booking")
        with allure.step("Проверяем статус код 200"):
            assert r.status_code == 200
        with allure.step("Проверяем что ответ непустой список"):
            data = r.json()
            assert isinstance(data, list)
            assert len(data) > 0


    @allure.title("TC_GET_002 - Фильтрация по firstname")
    @allure.severity(allure.severity_level.NORMAL)
    def test_002_filter_firstname(self):
        params = {"firstname": "John"}
        r = requests.get(f"{BASE_URL}/booking", params=params)
        with allure.step("Проверяем статус код 200"):
            assert r.status_code == 200
        with allure.step("Проверяем что ответ непустой список"):
            data = r.json()
            assert isinstance(data, list)
            assert len(data) > 0

    @allure.title("TC_GET_003 - Фильтрация по lastname")
    @allure.severity(allure.severity_level.NORMAL)
    def test_003_filter_lastname(self):
        params = {"lastname": "Doe"}
        r = requests.get(f"{BASE_URL}/booking", params=params)
        with allure.step("Проверяем статус код 200"):
            assert r.status_code == 200
        with allure.step("Проверяем что ответ непустой список"):
            data = r.json()
            assert isinstance(data, list)
            assert len(data) > 0

    @allure.title("TC_GET_004 - Фильтрация по датам (checkin/checkout)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_004_filter_by_dates(self):
        payload = test_data["valid_booking"]
        requests.post(f"{BASE_URL}/booking", json=payload)

        params = {
            "checkin": "2026-01-01",
            "checkout": "2026-01-05"
        }
        r = requests.get(f"{BASE_URL}/booking", params=params)

        with allure.step("Проверяем статус код 200"):
            assert r.status_code == 200

        with allure.step("Проверяем что ответ непустой список"):
            data = r.json()
            assert isinstance(data, list)

    @allure.title("TC_GET_005 - Получение существующей брони по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_005_get_task_by_id(self):
        payload = test_data["valid_booking"]
        r_create = requests.post(f"{BASE_URL}/booking", json=payload)
        bookingid = r_create.json()["bookingid"]
        r = requests.get(f"{BASE_URL}/booking/{bookingid}")
        with allure.step("Проверяем статус код 200"):
            assert r.status_code == 200

        with allure.step("Проверяем firstname == John"):
            data = r.json()
            assert data["firstname"] == "John"

    @allure.title("TC_GET_006 - Получение несуществующей брони по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_006_get_nonexistent_booking(self):
        r = requests.get(f"{BASE_URL}/booking/999999")
        with allure.step("Проверяем статус код 404"):
            assert r.status_code == 404

    @allure.title("TC_GET_007 - Валидация схемы ответа списка броней")
    @allure.severity(allure.severity_level.NORMAL)
    def test_007_bookings_list_schema(self):
        r = requests.get(f"{BASE_URL}/booking")
        data = r.json()
        with allure.step("Валидируем схему списка броней"):
            validate(instance=data, schema=BOOKINGS_LIST_SCHEMA)

    @allure.title("TC_GET_008 - Валидация схемы ответа одной брони")
    @allure.severity(allure.severity_level.NORMAL)
    def test_008_booking_schema(self):
        payload = test_data["valid_booking"]
        r_create = requests.post(f"{BASE_URL}/booking", json=payload)
        bookingid = r_create.json()["bookingid"]
        r = requests.get(f"{BASE_URL}/booking/{bookingid}")
        data = r.json()
        with allure.step("Валидируем схему списка броней"):
            validate(instance=data, schema=BOOKING_SCHEMA)

    @allure.title("TC_GET_009 - Проверка заголовков ответа")
    @allure.severity(allure.severity_level.NORMAL)
    def test_009_booking_schema(self):
        r = requests.get(f"{BASE_URL}/booking")
        with allure.step("Проверяем наличие Content-Type и Content-Length в headers"):
            assert "Content-Type" in r.headers
            assert "Content-Length" in r.headers

    @allure.title("TC_GET_010 - Проверка времени ответа")
    @allure.severity(allure.severity_level.NORMAL)
    def test_010_response_time(self):
        r = requests.get(f"{BASE_URL}/booking")
        with allure.step("Проверяем, что время ответа меньше 2 секунд"):
            assert r.elapsed.total_seconds() < 2.0










