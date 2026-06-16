import requests
import allure
import data.urls
from api.base_client import BaseClient

class OrdersClient(BaseClient):
    @allure.step("Отправка POST-запроса на создание заказа")
    def create_order(self, payload):
        return requests.post(f"{self.base_url}{data.urls.CREATED_ORDER_URL}", json=payload, headers=self.headers)

    @allure.step("Отправка PUT-запроса на отмену заказа")
    def cancel_order(self, track):
        return requests.put(f"{self.base_url}{data.urls.CANCEL_ORDER_URL}", params={"track": track}, headers=self.headers)

    @allure.step("Отправка GET-запроса на получение списка заказов")
    def get_orders_list(self):
        return requests.get(f"{self.base_url}{data.urls.GET_ORDERS_LIST}", headers=self.headers)
    