import requests
import random
import allure
from data_to_use import TestData


class TestChangeUserData:

    @allure.description('Удаление пользователя')
    def delete_user(self, random_user_registration):
        token = {'Authorization': random_user_registration}
        requests.delete(TestData.USER, headers=token)

    @allure.description('Изменение данных авторизованного пользователя')
    def test_change_auth_user_success(self, random_user_registration):
        new_payload = {"email": f"user{random.randint(1, 9999)}@yandex.ru",
                       "password": f"wo{random.randint(1, 9999)}rd",
                       "name": f"Thisis{random.randint(1, 9999)}"}
        token = {'Authorization': random_user_registration}
        response = requests.patch(TestData.USER, headers=token, json=new_payload)
        assert response.status_code == 200 and '"success":true' in response.text
        self.delete_user(random_user_registration)

    @allure.description('Изменение данных неавторизованного пользователя')
    def test_change_not_auth_user_fail(self):
        # используются incorrect данные, чтобы не использовать больше констант
        new_payload = {"email": TestData.INCORRECT_LOGIN,
                       "password": TestData.INCORRECT_PASSWORD,
                       "name": TestData.INCORRECT_NAME}
        response = requests.patch(TestData.USER, data=new_payload)
        assert response.status_code == 401 and response.text == '{"success":false,"message":"You should be authorised"}'
