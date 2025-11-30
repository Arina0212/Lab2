import json
import time

import pika
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Order, OrderItem, Product


def process_product(product_data: dict, db: Session):
    """Обработка данных товара и сохранение в БД"""
    product = Product(
        name=product_data["name"],
        price=product_data["price"],
        quantity=product_data["quantity"],
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    print(f"Product created: {product.name} (ID: {product.id})")
    return product


def process_order(order_data: dict, db: Session):
    """Обработка данных заказа и сохранение в БД"""
    # Создаем заказ
    order = Order(
        customer_name=order_data["customer_name"],
        total_amount=order_data["total_amount"],
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # Создаем элементы заказа
    for item_data in order_data["items"]:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data["product_id"],
            quantity=item_data["quantity"],
            price=item_data["price"],
        )
        db.add(order_item)

    db.commit()
    print(f"Order created: {order.id} for customer: {order.customer_name}")
    return order


def callback(ch, method, properties, body, db: Session):
    """Callback функция для обработки сообщений"""
    try:
        data = json.loads(body)

        if method.routing_key == "products":
            print(f"Received product: {data}")
            process_product(data, db)
        elif method.routing_key == "orders":
            print(f"Received order: {data}")
            process_order(data, db)

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except (
        json.JSONDecodeError,
        KeyError,
        ValueError,
        IntegrityError,
        SQLAlchemyError,
    ) as e:
        print(f"Error processing message: {e}")
        # Отклоняем сообщение (не переотправляем)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def start_consumer():
    """Запуск потребителя"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    # Объявляем очереди
    channel.queue_declare(queue="products")
    channel.queue_declare(queue="orders")

    # Создаем сессию БД
    db = SessionLocal()

    try:
        # Настраиваем потребление
        channel.basic_consume(
            queue="products",
            on_message_callback=lambda ch, method, properties, body: callback(
                ch, method, properties, body, db
            ),
        )

        channel.basic_consume(
            queue="orders",
            on_message_callback=lambda ch, method, properties, body: callback(
                ch, method, properties, body, db
            ),
        )

        print("Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Consumer stopped")
    finally:
        db.close()
        connection.close()


if __name__ == "__main__":
    start_consumer()
