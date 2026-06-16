import random


def generate_random_order_payload(color_list):
    first_names = ["Алексей", "Олег", "Иван", "Виктор", "Дмитрий", "Александр"]
    last_names = ["Петров", "Иванов", "Смирнов", "Кузнецов", "Парфенов", "Ерофеев"]
    streets = ["Ленина", "Пушкина", "Мира", "Арбат", "Заречная", "Кукушкина"]

    random_phone = f"+79{random.randint(100000000, 999999999)}"

    payload = {
        "firstName": random.choice(first_names),
        "lastName": random.choice(last_names),
        "address": f"ул. {random.choice(streets)}, д. {random.randint(1, 150)}",
        "metroStation": random.randint(1, 10),
        "phone": random_phone,
        "rentTime": random.randint(1, 7),
        "deliveryDate": "2026-07-12",
        "comment": "Позвонить за час до доставки",
        "color": color_list
    }

    return payload