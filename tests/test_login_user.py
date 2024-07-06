import requests
import allure
from data_to_use import TestData


class TestLoginUser:

    @allure.description('Логин под существующим пользователем')
    def test_existing_user_login_success(self):
        payload = {"email": TestData.EMAIL,
                   "password": TestData.PASSWORD,
                   "name": TestData.NAME}
        response = requests.post(TestData.LOGIN, json=payload)
        assert response.status_code == 200 and '"success":true' in response.text

    @allure.description('Логин с неверным логином и паролем')
    def test_incorrect_cred_login_fail(self):
        payload = {"email": TestData.INCORRECT_LOGIN,
                   "password": TestData.INCORRECT_PASSWORD}
        response = requests.post(TestData.LOGIN, json=payload)
        assert response.status_code == 401 and response.text == ('{"success":false,"message":"email or password are '
                                                                 'incorrect"}')
