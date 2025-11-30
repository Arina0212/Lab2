from app.models import Product
from app.schemas import ProductCreate


class ProductRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def get_all(self):
        with self.session_factory() as session:
            products = session.query(Product).all()
            return [product.to_dict() for product in products]

    def create(self, product_data: ProductCreate):
        with self.session_factory() as session:
            product = Product(
                name=product_data.name,
                price=product_data.price,
                quantity=product_data.quantity,
                status=product_data.status,
            )

            session.add(product)
            session.commit()
            session.refresh(product)
            return product.to_dict()

    def get_by_id(self, product_id: int):
        with self.session_factory() as session:
            product = session.query(Product).filter(Product.id == product_id).first()
            return product.to_dict() if product else None
