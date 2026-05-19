import allure
import requests
from config import BASE_URL


class BookingApi:

    @allure.step("POST /booking — создаём бронь")
    def create_booking(self, payload):
        return requests.post(f"{BASE_URL}/booking", json=payload)

    @allure.step("GET /booking/{booking_id} — получаем бронь")
    def get_booking(self, booking_id):
        return requests.get(f"{BASE_URL}/booking/{booking_id}")

    @allure.step("PUT /booking/{booking_id} — обновляем бронь")
    def update_booking(self, booking_id, payload, token):
        return requests.put(f"{BASE_URL}/booking/{booking_id}",
                           json=payload,
                           cookies={"token": token})

    @allure.step("PATCH /booking/{booking_id} — частично обновляем бронь")
    def patch_booking(self, booking_id, payload, token):
        return requests.patch(f"{BASE_URL}/booking/{booking_id}",
                             json=payload,
                             cookies={"token": token})

    @allure.step("DELETE /booking/{booking_id} — удаляем бронь")
    def delete_booking(self, booking_id, token):
        return requests.delete(f"{BASE_URL}/booking/{booking_id}",
                              cookies={"token": token})