import pytest
from helpers.generations import register_new_courier_and_return_login_password
from api.courier_client import CourierClient
from api.orders_client import OrdersClient

@pytest.fixture(scope="function")
def courier_create():
    client = CourierClient()
    
    courier_data = register_new_courier_and_return_login_password()
    login = courier_data[0]
    password = courier_data[1]
    firstName = courier_data[2]
    
    response_login = client.login_courier(login, password)
    courier_id = response_login.json().get("id")
    
    yield {"login": login, "password": password, "firstName": firstName, "id": courier_id}
    
    if courier_id:
        client.delete_courier(courier_id)

@pytest.fixture
def courier_cleanup():

    courier_credentials = []
    
    yield courier_credentials
    
    if courier_credentials:
        login, password = courier_credentials
        client = CourierClient()
        
        login_response = client.login_courier(login, password)
        if login_response.status_code == 200:
            courier_id = login_response.json().get('id')
            client.delete_courier(courier_id)

@pytest.fixture
def clean_up_order():
    order = OrdersClient()
    order_data = {}
    
    yield order_data
    
    if "track" in order_data:
        order.cancel_order(order_data["track"])
    