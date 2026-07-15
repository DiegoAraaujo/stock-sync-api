from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.orders.models import Order
from app.orders.schemas import OrderCreate
from app.products.models import Product


def get_all(db: Session):
    return db.query(Order).all()


def get_by_id(db: Session, order_id: int) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def create(db: Session, data: OrderCreate) -> Order:
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.quantity < data.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient stock. Available: {product.quantity}"
        )

    product.quantity -= data.quantity

    order = Order(product_id=data.product_id, quantity=data.quantity)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order