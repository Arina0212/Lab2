import json

from app.models import Order
from app.schemas import OrderCreate


class OrderRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def get_all(self):
        with self.session_factory() as session:
            orders = session.query(Order).all()
            return [order.to_dict() for order in orders]

    def create(self, order_data: OrderCreate):
        with self.session_factory() as session:
            # Сериализуем items в JSON строку
            items_json = json.dumps(
                [item.dict() for item in order_data.items], ensure_ascii=False
            )

            order = Order(
                customer_name=order_data.customer_name,
                items=items_json,
                total_amount=order_data.total_amount,
                status=order_data.status,
            )

            session.add(order)
            session.commit()
            session.refresh(order)
            return order.to_dict()

    def get_by_id(self, order_id: int):
        with self.session_factory() as session:
            order = session.query(Order).filter(Order.id == order_id).first()
            return order.to_dict() if order else None
