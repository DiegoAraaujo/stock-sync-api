from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.products import service
from app.products.schemas import ProductCreate, ProductUpdate, ProductResponse, StockUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return service.get_all(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return service.get_by_id(db, product_id)


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    return service.create(db, data)


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    return service.update(db, product_id, data)


@router.put("/{product_id}/stock", response_model=ProductResponse)
def update_stock(product_id: int, data: StockUpdate, db: Session = Depends(get_db)):
    return service.update_stock(db, product_id, data)


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    service.delete(db, product_id)