import pytest
import requests
import random
from data_to_use import TestData


@pytest.fixture
def random_user_registration():
    payload = {"email": f"user{random.randint(1, 9999)}@yandex.ru",
               "password": f"wo{random.randint(1, 9999)}rd",
               "name": f"Thisis{random.randint(1, 9999)}"}
    response = requests.post(TestData.REGISTER, json=payload).json()
    reg_token = response.get("accessToken")
    return reg_token


@pytest.fixture
def login():
    payload = {"email": TestData.EMAIL,
               "password": TestData.PASSWORD,
               "name": TestData.NAME}
    response = requests.post(TestData.LOGIN, data=payload).json()
    login_token = response.get("accessToken")
    return login_token


@pytest.fixture
def ingredients_ids_to_get():
    response = requests.get(TestData.INGREDIENTS)
    return [ingredient["_id"] for ingredient in response.json()["data"]]
