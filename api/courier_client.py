import requests
import allure
import data.urls
from api.base_client import BaseClient


class CourierClient(BaseClient):
    
    @allure.step("Регистрация нового курьера")
    def register_courier(self, login, password, first_name):
        body = {
            "login": login,
            "password": password,
            "first_name": first_name
        }
        url = f"{self.base_url}{data.urls.COURIER_URL}"
        
        return requests.post(url, json=body, headers=self.headers)

    @allure.step("Логин курьера в систему")
    def login_courier(self, login, password):
        body = {
            "login": login,
            "password": password
        }
        url = f"{self.base_url}{data.urls.LOGIN_COURIER_URL}"
        
        return requests.post(url, json=body, headers=self.headers)
    
    

    @allure.step("Удаление курьера по ID")
    def delete_courier(self, courier_id):
        url = f"{self.base_url}{data.urls.COURIER_URL}/{courier_id}"
        
        return requests.delete(url, headers=self.headers)