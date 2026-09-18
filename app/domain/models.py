from pydantic import BaseModel, Field
from enum import Enum
from decimal import Decimal

class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class Product(BaseModel):
    id: int  = Field(..., gt=0, description="Id must greater than 0")
    name: str
    price: Decimal = Field(..., gt=0, description="Price must greater than 0")
    stock: int = Field(..., ge=0, description="Stock must greater than 0")

class Order(BaseModel):
    id: int  = Field(..., gt=0, description="Id must greater than 0")
    product_id: int = Field(..., gt=0, description="Product id must greater than 0")
    quantity: int = Field(..., gt=0, description="Quantity must greater than 0")
    status : OrderStatus = OrderStatus.PENDING
    total: Decimal = Field(..., gt=0, description="Total must greater than 0")
