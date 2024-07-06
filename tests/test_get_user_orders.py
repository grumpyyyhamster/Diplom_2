import requests
import allure
from data_to_use import TestData


class TestGetUserOrders:

    @allure.description('Получение списка заказов авторизованного пользователя')
    def test_get_auth_user_orders_success(self, login):
        token = {'Authorization': login}
        response = requests.get(TestData.ORDERS_ALL, headers=token)
        assert response.status_code == 200 and 'orders' in response.text

    @allure.description('Получение списка заказов неавторизованным пользователем')
    def test_get_not_auth_user_orders_fail(self):
        response = requests.get(TestData.ORDERS_ALL)
        assert response.status_code == 200 and 'orders' in response.text
