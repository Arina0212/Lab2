from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Address, Product, Order, OrderItem
from datetime import datetime

connect_url = "sqlite:///lab2.db"
engine = create_engine(connect_url, echo=True)
SessionFactory = sessionmaker(bind=engine)

def seed_data():
    with SessionFactory() as session:
        # ОЧИСТКА СУЩЕСТВУЮЩИХ ДАННЫХ
        session.query(OrderItem).delete()
        session.query(Order).delete()
        session.query(Product).delete()
        session.query(Address).delete()
        session.query(User).delete()
        session.commit()
        
        current_time = datetime.now()
        
        # Создание пользователей
        users_data = [
            {"username": "john_doe", "email": "john@example.com", "description": "Regular customer"},
            {"username": "jane_smith", "email": "jane@example.com", "description": "VIP client"},
            {"username": "bob_wilson", "email": "bob@example.com", "description": "New customer"},
            {"username": "alice_brown", "email": "alice@example.com", "description": "Wholesale buyer"},
            {"username": "charlie_davis", "email": "charlie@example.com", "description": "International client"}
        ]
        
        users = []
        for user_data in users_data:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                description=user_data["description"],
                created_at=current_time,
                updated_at=current_time
            )
            session.add(user)
            users.append(user)
        
        session.commit()
        
        # Создание адресов
        addresses_data = [
            {"street": "123 Main Street", "city": "New York", "state": "NY", "zip_code": "10001", "country": "USA"},
            {"street": "456 Oxford Street", "city": "London", "state": "", "zip_code": "W1D 1BS", "country": "UK"},
            {"street": "789 Champs-Élysées", "city": "Paris", "state": "", "zip_code": "75008", "country": "France"},
            {"street": "321 Alexanderplatz", "city": "Berlin", "state": "", "zip_code": "10178", "country": "Germany"},
            {"street": "654 Ginza Street", "city": "Tokyo", "state": "", "zip_code": "104-0061", "country": "Japan"}
        ]
        
        addresses = []
        for i, user in enumerate(users):
            address_info = addresses_data[i]
            address = Address(
                user_id=user.id,
                street=address_info["street"],
                city=address_info["city"],
                state=address_info["state"],
                zip_code=address_info["zip_code"],
                country=address_info["country"],
                is_primary=True,
                created_at=current_time,
                updated_at=current_time
            )
            session.add(address)
            addresses.append(address)
        
        session.commit()
        
        # Создание 5 продуктов
        products_data = [
            {"name": "Laptop", "description": "High-performance laptop", "price": "999.99"},
            {"name": "Smartphone", "description": "Latest smartphone model", "price": "699.99"},
            {"name": "Tablet", "description": "Portable tablet device", "price": "399.99"},
            {"name": "Headphones", "description": "Wireless noise-canceling headphones", "price": "199.99"},
            {"name": "Smartwatch", "description": "Fitness tracking smartwatch", "price": "249.99"}
        ]
        
        products = []
        for product_data in products_data:
            product = Product(
                name=product_data["name"],
                description=product_data["description"],
                price=product_data["price"],
                created_at=current_time,
                updated_at=current_time
            )
            session.add(product)
            products.append(product)
        
        session.commit()
        
        # Создание 5 заказов
        orders_data = [
            {"user_id": users[0].id, "address_id": addresses[0].id, "total_amount": "1199.98", "status": "completed"},
            {"user_id": users[1].id, "address_id": addresses[1].id, "total_amount": "899.98", "status": "shipped"},
            {"user_id": users[2].id, "address_id": addresses[2].id, "total_amount": "649.98", "status": "processing"},
            {"user_id": users[3].id, "address_id": addresses[3].id, "total_amount": "199.99", "status": "pending"},
            {"user_id": users[4].id, "address_id": addresses[4].id, "total_amount": "1249.97", "status": "completed"}
        ]
        
        orders = []
        for order_data in orders_data:
            order = Order(
                user_id=order_data["user_id"],
                address_id=order_data["address_id"],
                total_amount=order_data["total_amount"],
                status=order_data["status"],
                created_at=current_time,
                updated_at=current_time
            )
            session.add(order)
            orders.append(order)
        
        session.commit()
        
        # Создание элементов заказов
        order_items_data = [
            {"order_id": orders[0].id, "product_id": products[0].id, "quantity": "1", "price": "999.99"},
            {"order_id": orders[0].id, "product_id": products[3].id, "quantity": "1", "price": "199.99"},
            {"order_id": orders[1].id, "product_id": products[1].id, "quantity": "1", "price": "699.99"},
            {"order_id": orders[1].id, "product_id": products[3].id, "quantity": "1", "price": "199.99"},
            {"order_id": orders[2].id, "product_id": products[2].id, "quantity": "1", "price": "399.99"},
            {"order_id": orders[2].id, "product_id": products[4].id, "quantity": "1", "price": "249.99"},
            {"order_id": orders[3].id, "product_id": products[3].id, "quantity": "1", "price": "199.99"},
            {"order_id": orders[4].id, "product_id": products[0].id, "quantity": "1", "price": "999.99"},
            {"order_id": orders[4].id, "product_id": products[4].id, "quantity": "1", "price": "249.99"},
        ]
        
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=item_data["order_id"],
                product_id=item_data["product_id"],
                quantity=item_data["quantity"],
                price=item_data["price"],
                created_at=current_time
            )
            session.add(order_item)
        
        session.commit()
        print("✅ Данные успешно добавлены в базу!")
        print(f"📊 Создано: {len(users)} пользователей, {len(addresses)} адресов, {len(products)} продуктов, {len(orders)} заказов")

if __name__ == "__main__":
    seed_data()