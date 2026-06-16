import allure
import random
import string
from api.courier_client import CourierClient
from data import messages


class TestCreateCourier:

    def generate_random_string(self, length):
            letters = string.ascii_lowercase
            random_string = ''.join(random.choice(letters) for i in range(length))
            return random_string

    @allure.title("Успешное создание курьера со всеми обязательными полями")
    def test_courier_create_success(self):
        client = CourierClient()
        
        login = self.generate_random_string(10)
        password = self.generate_random_string(10)
        first_name = self.generate_random_string(10)

        response = client.register_courier(login, password, first_name)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        login_response = client.login_courier(login, password)
        id_courier = login_response.json().get('id')

        if id_courier:
            client.delete_courier(id_courier)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_dublicate_courier_fails(self, courier_create):
        client = CourierClient()

        existing_login = courier_create['login']
        existing_password = courier_create['password']
        existing_name = courier_create['firstName']

        dublicate_courier = client.register_courier(existing_login, existing_password, existing_name)

        assert dublicate_courier.status_code == 409
        assert dublicate_courier.json().get('message') == messages.CREATE_COURIER_DUPLICATE_ERROR

    @allure.title("Нельзя создать курьера, если не указать поле с логином")
    def test_create_courier_without_login_field_fails(self):
        client = CourierClient()

        password = self.generate_random_string(10)
        first_name = self.generate_random_string(10)

        response = client.register_courier(None, password, first_name)

        assert response.status_code == 400
        assert response.json().get('message') == messages.CREATE_COURIER_INSUFFICIENT_DATA_ERROR

    @allure.title("Нельзя создать курьера, если не указать поле с паролем")
    def test_create_courier_without_password_field_fails(self):
        client = CourierClient()

        login = self.generate_random_string(10)
        first_name = self.generate_random_string(10)

        response = client.register_courier(login, None, first_name)

        assert response.status_code == 400
        assert response.json().get('message') == messages.CREATE_COURIER_INSUFFICIENT_DATA_ERROR
