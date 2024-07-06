import pytest
import requests
import random
import allure
from data_to_use import TestData


class TestUserCreate:

    @allure.description('Удаление пользователя')
    def delete_user(self, access_token):
        token = {'Authorization': access_token}
        requests.delete(TestData.USER, headers=token)

    @allure.description('Создание уникального пользователя')
    def test_new_user_create_success(self):
        payload = {"email": f"user{random.randint(1, 9999)}@yandex.ru",
                   "password": f"wo{random.randint(1, 9999)}rd",
                   "name": f"Thisis{random.randint(1, 9999)}"}
        response = requests.post(TestData.REGISTER, json=payload)
        response_json = response.json()
        assert response.status_code == 200 and '"success":true' in response.text
        self.delete_user(response_json.get("accessToken"))

    @allure.description('Создание пользователя, который уже зарегистрирован')
    def test_same_user_create_fail(self):
        payload = {"email": TestData.EMAIL,
                   "password": TestData.PASSWORD,
                   "name": TestData.NAME}
        response = requests.post(TestData.REGISTER, json=payload)
        assert response.status_code == 403 and response.text == '{"success":false,"message":"User already exists"}'

    @allure.description('Создание пользователя и не заполнение одного из обязательных полей')
    @pytest.mark.parametrize('email, password, name', [
        (f"user{random.randint(1, 9999)}@yandex.ru", "", f"Thisis{random.randint(1, 9999)}"),
        ("", f"wo{random.randint(1, 9999)}rd", f"Thisis{random.randint(1, 9999)}"),
        (f"user{random.randint(1, 9999)}@yandex.ru", f"wo{random.randint(1, 9999)}rd", "")])
    def test_user_without_needed_field_create_fail(self, email, password, name):
        payload = {"email": email,
                   "password": password,
                   "name": name}
        response = requests.post(TestData.REGISTER, data=payload)
        assert response.status_code == 403 and response.text == ('{"success":false,"message":"Email, password and name '
                                                                 'are required fields"}')
