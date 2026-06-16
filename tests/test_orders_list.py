import allure
from api.orders_client import OrdersClient


class TestOrderList:

    @allure.title("В тело ответа возвращается список заказов")
    def test_get_orders_list_returns_list_success(self):
        order = OrdersClient()

        response = order.get_orders_list()
        
        assert response.status_code == 200

        response_body = response.json()

        assert "orders" in response_body
        assert isinstance(response_body.get("orders"), list)
        assert len(response_body.get("orders")) > 0
