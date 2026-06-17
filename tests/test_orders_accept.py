import allure
from api.orders_client import OrdersClient
from helpers.generations import get_order_payload
from data import messages


class TestAcceptOrder:

    @allure.title("Успешное принятие заказа")
    def test_accept_order_success(self, courier_create, clean_up_order):
        order_client = OrdersClient()
        
        payload = get_order_payload(["BLACK"])

        response_order = order_client.create_order(payload)
        track_number = response_order.json().get("track")

        clean_up_order["track"] = track_number

        response_track = order_client.get_order_by_track(track_number)
        orderid = response_track.json().get("order").get("id")

        courierId = courier_create['id']

        response = order_client.accept_order(orderid, courierId)

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Нельзя принять заказ, если не указать id курьера")
    def test_accept_order_without_courier_id_returns_error(self, clean_up_order):
        order_client = OrdersClient()
        
        payload = get_order_payload(["BLACK"])

        response_order = order_client.create_order(payload)
        track_number = response_order.json().get("track")

        clean_up_order["track"] = track_number

        response_track = order_client.get_order_by_track(track_number)
        orderid = response_track.json().get("order").get("id")

        courier_id_missing = None

        response = order_client.accept_order(orderid, courier_id_missing)

        assert response.status_code == 400
        assert response.json().get("message") == messages.ACCEPT_ORDER_WITHOUT_ID_COURIER_ERROR

    @allure.title("Попытка принять заказ с несуществующим ID курьера")
    def test_accept_order_invalid_courier_id_returns_error(self, clean_up_order):
        order_client = OrdersClient()
        
        payload = get_order_payload(["BLACK"])

        response_order = order_client.create_order(payload)
        track_number = response_order.json().get("track")

        clean_up_order["track"] = track_number

        response_track = order_client.get_order_by_track(track_number)
        orderid = response_track.json().get("order").get("id")

        invalid_courierId = 999999

        response = order_client.accept_order(orderid, invalid_courierId)

        assert response.status_code == 404
        assert response.json().get("message") == messages.ACCEPT_ORDER_WITH_INVALID_ID_COURIER_ERROR
