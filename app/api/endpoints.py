from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.cache import (
    cache_product,
    cache_products,
    get_cached_product,
    get_cached_products,
    invalidate_products_cache,
)
from app.database import get_db
from datetime import date
from fastapi import Query

router = APIRouter()


def _serialize_product(product: models.Product) -> dict:
    # mode="json" converts datetime to ISO string so payload is JSON-safe
    return schemas.Product.model_validate(product).model_dump(mode="json")


@router.get("/products", response_model=List[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    cached_products = get_cached_products()
    if cached_products is not None:
        return cached_products

    products = db.query(models.Product).all()
    serialized_products = [_serialize_product(product) for product in products]
    cache_products(serialized_products)
    return serialized_products


@router.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    cached_product = get_cached_product(product_id)
    if cached_product is not None:
        return cached_product

    product = (
        db.query(models.Product).filter(models.Product.id == product_id).first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    serialized_product = _serialize_product(product)
    cache_product(product_id, serialized_product)
    return serialized_product


@router.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    serialized_product = _serialize_product(db_product)
    cache_product(db_product.id, serialized_product)
    invalidate_products_cache()
    return serialized_product


@router.put("/products/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int, product_update: schemas.ProductUpdate, db: Session = Depends(get_db)
):
    db_product = (
        db.query(models.Product).filter(models.Product.id == product_id).first()
    )
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    serialized_product = _serialize_product(db_product)
    cache_product(product_id, serialized_product)
    invalidate_products_cache()
    return serialized_product


@router.get("/orders", response_model=List[schemas.Order])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return orders


@router.post("/orders", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(
        customer_name=order.customer_name, total_amount=order.total_amount
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:
        db_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price,
        )
        db.add(db_item)

    db.commit()
    return db_order


@router.get("/report", response_model=List[schemas.OrderReport])
def get_report(
    report_at: date = Query(..., description="Дата отчета в формате YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    reports = (
        db.query(models.OrderReport)
        .filter(models.OrderReport.report_at == report_at)
        .all()
    )
    return reports
