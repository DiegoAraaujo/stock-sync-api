from fastapi import FastAPI
from app.database import engine, Base
from app.products import models as product_models
from app.orders import models as order_models
from app.sync import models as sync_models

Base.metadata.create_all(bind=engine)

from app.products.router import router as products_router
from app.orders.router import router as orders_router
from app.sync.router import router as sync_router

app = FastAPI(title="Stock Sync API")

app.include_router(products_router)
app.include_router(orders_router)
app.include_router(sync_router)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "stock-sync-api"}