from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    category: str
    price: Decimal
    quantity: int = 0


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[Decimal] = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    price: Decimal
    quantity: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class StockUpdate(BaseModel):
    quantity: int