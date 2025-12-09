from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class UserListResponse(BaseModel):
    users: List[UserResponse]
    total_count: int


class ProductBase(BaseModel):
    name: str
    price: float
    quantity: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    quantity: int | None = None


class Product(ProductBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class OrderBase(BaseModel):
    customer_name: str
    total_amount: float


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class Order(OrderBase):
    id: int
    created_at: datetime
    items: List[OrderItem] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class OrderReport(BaseModel):
    report_at: datetime
    order_id: int
    count_product: int

    model_config = ConfigDict(from_attributes=True)
