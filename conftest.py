import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture
def auth_token():
    url = f"{BASE_URL}/auth"
    payload = {"username": "admin", "password": "password123"}
    r = requests.post(url, json=payload)
    data = r.json()
    return data["token"]

@pytest.fixture(scope="module")
def create_booking_id():
    url = f"{BASE_URL}/booking"
    payload = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-01-01", "checkout": "2026-01-05"},
    }
    r = requests.post(url, json=payload)
    data = r.json()
    return data["bookingid"]


