from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.products.models import Product
from app.products.schemas import ProductCreate, ProductUpdate, StockUpdate


def get_all(db: Session):
    return db.query(Product).all()


def get_by_id(db: Session, product_id: int) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def create(db: Session, data: ProductCreate) -> Product:
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update(db: Session, product_id: int, data: ProductUpdate) -> Product:
    product = get_by_id(db, product_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def update_stock(db: Session, product_id: int, data: StockUpdate) -> Product:
    product = get_by_id(db, product_id)
    product.quantity = data.quantity
    db.commit()
    db.refresh(product)
    return product


def delete(db: Session, product_id: int) -> None:
    product = get_by_id(db, product_id)
    db.delete(product)
    db.commit()