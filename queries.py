from sqlalchemy import create_engine, select
from sqlalchemy.orm import selectinload, sessionmaker

from models import Order, OrderItem, Product, User

connect_url = "sqlite:///lab2.db"
engine = create_engine(connect_url, echo=True)
SessionFactory = sessionmaker(bind=engine)


def demo_queries():
    with SessionFactory() as session:
        # Используем selectinload для загрузки связанных данных
        users = (
            session.execute(select(User).options(selectinload(User.addresses)))
            .scalars()
            .all()
        )

        for user in users:
            print(f" {user.username} ({user.email}) - {user.description}")
            for address in user.addresses:
                print(f"    {address.street}, {address.city}, {address.country}")

        # Загружаем заказы с пользователями, адресами и товарами
        orders = (
            session.execute(
                select(Order).options(
                    selectinload(Order.user),
                    selectinload(Order.address),
                    selectinload(Order.order_items).selectinload(OrderItem.product),
                )
            )
            .scalars()
            .all()
        )

        for order in orders:
            print(f"\n Заказ #{order.id[:8]}... - {order.status}")
            print(f"    Пользователь: {order.user.username}")
            print(f"    Адрес доставки: {order.address.street}, {order.address.city}")
            print(f"    Общая сумма: ${order.total_amount}")
            print("    Товары в заказе:")
            for item in order.order_items:
                print(f"      - {item.product.name}: {item.quantity} × ${item.price}")

        products = session.execute(select(Product)).scalars().all()
        for product in products:
            print(f"{product.name}: ${product.price} - {product.description}")


if __name__ == "__main__":
    demo_queries()
