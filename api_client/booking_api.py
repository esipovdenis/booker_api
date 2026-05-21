import allure
import requests
from config import BASE_URL


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
        assert r.status_code == expected_code

    @allure.step("Валидировать схему ответа")
    def validate_schema(self, data, schema):
        from jsonschema import validate
        validate(instance=data, schema=schema)