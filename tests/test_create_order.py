import requests
import allure
from data_to_use import TestData


class TestCreateOrder:

    @allure.description('Создание заказа авторизованным пользователем с ингредиентами')
    def test_order_create_auth_user_with_ingridients_success(self, login, ingredients_ids_to_get):
        payload = {"ingredients": [ingredients_ids_to_get[0], ingredients_ids_to_get[2]]}
        token = {'Authorization': login}
        response = requests.post(TestData.ORDERS, headers=token, json=payload)
        assert response.status_code == 200 and 'order' in response.text

    @allure.description('Создание заказа не авторизованным пользователем с ингредиентами')
    def test_order_create_not_auth_user_with_ingridients_success(self, ingredients_ids_to_get):
        payload = {"ingredients": [ingredients_ids_to_get[0], ingredients_ids_to_get[2]]}
        response = requests.post(TestData.ORDERS, json=payload)
        assert response.status_code == 200 and 'order' in response.text

    @allure.description('Создание заказа без ингредиентов')
    def test_order_create_without_ingredients_fail(self):
        payload = {"ingredients": []}
        response = requests.post(TestData.ORDERS, json=payload)
        assert response.status_code == 400 and response.text == ('{"success":false,"message":"Ingredient ids must be '
                                                                 'provided"}')

    @allure.description('Создание заказа с неверным хешем ингредиентов')
    def test_order_create_with_invalid_hash_ingredients_fail(self):
        payload = {"ingredients": ['3', '4']}
        response = requests.post(TestData.ORDERS, json=payload)
        assert response.status_code == 500 and 'Internal Server Error' in response.text
