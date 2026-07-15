from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.orders import service
from app.orders.schemas import OrderCreate, OrderResponse

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=list[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    return service.get_all(db)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return service.get_by_id(db, order_id)


@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    return service.create(db, data)
