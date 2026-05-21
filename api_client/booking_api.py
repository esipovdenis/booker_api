import allure
import requests
import urllib3
from jsonschema import validate
from config import BASE_URL

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BookingApi:

    @allure.step("Создать новую бронь")
    def create_booking(self, payload):
        return requests.post(f"{BASE_URL}/booking", json=payload, verify=False)

    @allure.step("Получить бронь с ID {booking_id}")
    def get_booking(self, booking_id):
        return requests.get(f"{BASE_URL}/booking/{booking_id}", verify=False)

    @allure.step("Обновить бронь с ID {booking_id}")
    def update_booking(self, booking_id, payload, token):
        return requests.put(f"{BASE_URL}/booking/{booking_id}",
                           json=payload,
                           cookies={"token": token},
                           verify=False)

    @allure.step("Частично обновить бронь с ID {booking_id}")
    def patch_booking(self, booking_id, payload, token):
        return requests.patch(f"{BASE_URL}/booking/{booking_id}",
                             json=payload,
                             cookies={"token": token},
                             verify=False)

    @allure.step("Удалить бронь с ID {booking_id}")
    def delete_booking(self, booking_id, token):
        return requests.delete(f"{BASE_URL}/booking/{booking_id}",
                              cookies={"token": token},
                              verify=False)

    @allure.step("Проверить статус код {expected_code}")
    def check_status_code(self, r, expected_code):
        assert r.status_code == expected_code, \
            f"Ожидался статус {expected_code}, получен {r.status_code}"

    @allure.step("Проверить наличие bookingid в ответе")
    def check_booking_id_exists(self, r):
        assert "bookingid" in r.json(), \
            "bookingid отсутствует в ответе"

    @allure.step("Проверить firstname == {expected_firstname}")
    def check_firstname(self, r, expected_firstname):
        assert r.json()["firstname"] == expected_firstname, \
            f"Ожидался firstname {expected_firstname}, получен {r.json()['firstname']}"

    @allure.step("Проверить totalprice == {expected_price}")
    def check_totalprice(self, r, expected_price):
        assert r.json()["totalprice"] == expected_price, \
            f"Ожидался totalprice {expected_price}, получен {r.json()['totalprice']}"

    @allure.step("Проверить lastname == {expected_lastname}")
    def check_lastname(self, r, expected_lastname):
        assert r.json()["lastname"] == expected_lastname, \
            f"Ожидался lastname {expected_lastname}, получен {r.json()['lastname']}"

    @allure.step("Валидировать схему ответа")
    def validate_schema(self, r, schema):
        validate(instance=r.json(), schema=schema)