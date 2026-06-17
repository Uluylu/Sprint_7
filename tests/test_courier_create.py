import allure
from api.courier_client import CourierClient
from data import messages
from helpers.generations import generate_random_string


class TestCreateCourier:

    @allure.title("Успешное создание курьера со всеми обязательными полями")
    def test_courier_create_success(self, courier_cleanup):
        client = CourierClient()
        
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        courier_cleanup.extend([login, password])

        response = client.register_courier(login, password, first_name)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

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

        password = generate_random_string(10)
        first_name = generate_random_string(10)

        response = client.register_courier(None, password, first_name)

        assert response.status_code == 400
        assert response.json().get('message') == messages.CREATE_COURIER_INSUFFICIENT_DATA_ERROR

    @allure.title("Нельзя создать курьера, если не указать поле с паролем")
    def test_create_courier_without_password_field_fails(self):
        client = CourierClient()

        login = generate_random_string(10)
        first_name = generate_random_string(10)

        response = client.register_courier(login, None, first_name)

        assert response.status_code == 400
        assert response.json().get('message') == messages.CREATE_COURIER_INSUFFICIENT_DATA_ERROR
