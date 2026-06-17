import allure
import random
import string
from api.courier_client import CourierClient
from data import messages
from helpers.generations import generate_random_string


class TestCourierDelete:

    @allure.title("Успешное удаление курьера")
    def test_courier_delete_success(self):
        client = CourierClient()
        
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        client.register_courier(login, password, first_name)

        login_response = client.login_courier(login, password)
        id_courier = login_response.json().get('id')

        delete_response = client.delete_courier(id_courier)

        assert delete_response.status_code == 200
        assert delete_response.json() == {"ok": True}

    @allure.title("Попытка удаления курьера без указания ID")
    def test_delete_courier_without_id_returns_error(self):
        client = CourierClient()
    
        response = client.delete_courier("") 
    
        assert response.status_code == 404
        assert response.json().get("message") == messages.DELETE_COURIER_WITHOUT_ID_ERROR

    @allure.title("Попытка удаления курьера с несуществующим ID")
    def test_delete_courier_with_invalid_id_returns_error(self):
        client = CourierClient()
    
        response = client.delete_courier(9999999) 
    
        assert response.status_code == 404
        assert response.json().get("message") == messages.DELETE_COURIER_WITH_INVALID_ID_ERROR
        