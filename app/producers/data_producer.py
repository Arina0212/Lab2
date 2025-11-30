import json
import time

import pika


def send_to_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    # Объявляем очереди
    channel.queue_declare(queue="products")
    channel.queue_declare(queue="orders")

    # Тестовые данные товаров
    products = [
        {"name": "Ноутбук", "price": 50000.0, "quantity": 10},
        {"name": "Мышь", "price": 1500.0, "quantity": 50},
        {"name": "Клавиатура", "price": 3000.0, "quantity": 30},
        {"name": "Монитор", "price": 20000.0, "quantity": 15},
        {"name": "Наушники", "price": 5000.0, "quantity": 25},
    ]

    # Тестовые данные заказов
    orders = [
        {
            "customer_name": "Иван Иванов",
            "items": [
                {"product_id": 1, "quantity": 1, "price": 50000.0},
                {"product_id": 2, "quantity": 2, "price": 1500.0},
            ],
            "total_amount": 53000.0,
        },
        {
            "customer_name": "Петр Петров",
            "items": [
                {"product_id": 3, "quantity": 1, "price": 3000.0},
                {"product_id": 5, "quantity": 1, "price": 5000.0},
            ],
            "total_amount": 8000.0,
        },
        {
            "customer_name": "Сергей Сергеев",
            "items": [
                {"product_id": 4, "quantity": 2, "price": 20000.0},
                {"product_id": 2, "quantity": 1, "price": 1500.0},
            ],
            "total_amount": 41500.0,
        },
    ]

    # Отправляем товары
    for product in products:
        channel.basic_publish(
            exchange="",
            routing_key="products",
            body=json.dumps(product, ensure_ascii=False),
        )
        print(f"Товар отправлен: {product}")
        time.sleep(1)

    # Отправляем заказы
    for order in orders:
        channel.basic_publish(
            exchange="",
            routing_key="orders",
            body=json.dumps(order, ensure_ascii=False),
        )
        print(f"Заказ отправлен: {order}")
        time.sleep(1)

    connection.close()
    print("Все тестовые данные отправлены!")


if __name__ == "__main__":
    send_to_rabbitmq()
