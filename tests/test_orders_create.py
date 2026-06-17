import pytest
import allure
from api.orders_client import OrdersClient
from helpers.order_data_generator import generate_random_order_payload


class TestCreateOrder:

    @pytest.mark.parametrize("color_list", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    @allure.title("Успешное создание заказа с разными цветами")
    def test_create_order_success(self, color_list, clean_up_order):
        client = OrdersClient()
        
        request_body = generate_random_order_payload(color_list)
        response = client.create_order(request_body)
        
        assert response.status_code == 201
        assert "track" in response.json()

        clean_up_order["track"] = response.json().get("track")
