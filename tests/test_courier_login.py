import allure
import random
import string
from api.courier_client import CourierClient
from data import messages


class TestLoginCourier:

    def generate_random_string(self, length):
            letters = string.ascii_lowercase
            random_string = ''.join(random.choice(letters) for i in range(length))
            return random_string

    @allure.title("Успешная авторизация курьера")
    def test_login_success(self, courier_create):
        client = CourierClient()
        
        login = courier_create['login']
        password = courier_create['password']

        authorization_courier = client.login_courier(login, password)

        assert authorization_courier.status_code == 200
        assert authorization_courier.json().get("id") == courier_create["id"]

    @allure.title("Нельзя авторизоваться, если не указать логин")
    def test_login_without_login_field_fails(self):
        client = CourierClient()
        
        password = self.generate_random_string(10)

        authorization_courier = client.login_courier(None, password)

        assert authorization_courier.status_code == 400
        assert authorization_courier.json().get('message') == messages.AUTHORIZATION_COURIER_INSUFFICIENT_DATA_ERROR

    @allure.title("Нельзя авторизоваться, если не указать пароль")
    def test_login_without_password_field_fails(self):
        client = CourierClient()
        
        login = self.generate_random_string(10)

        authorization_courier = client.login_courier(login, "")

        assert authorization_courier.status_code == 400
        assert authorization_courier.json().get('message') == messages.AUTHORIZATION_COURIER_INSUFFICIENT_DATA_ERROR

    @allure.title("Нельзя авторизоваться, если неправильно указан логин")
    def test_login_with_non_existent_login_field_courier_fails(self, courier_create):
        client = CourierClient()
        
        login = self.generate_random_string(10)
        password = courier_create['password']

        authorization_courier = client.login_courier(login, password)

        assert authorization_courier.status_code == 404
        assert authorization_courier.json().get('message') == messages.AUTHORIZATION_COURIER_ACCOUNT_NOT_FOUND_ERROR

    @allure.title("Нельзя авторизоваться, если неправильно указан пароль")
    def test_login_with_non_existent_password_field_courier_fails(self, courier_create):
        client = CourierClient()
        
        login = courier_create['login']
        password = self.generate_random_string(10)

        authorization_courier = client.login_courier(login, password)

        assert authorization_courier.status_code == 404
        assert authorization_courier.json().get('message') == messages.AUTHORIZATION_COURIER_ACCOUNT_NOT_FOUND_ERROR
        