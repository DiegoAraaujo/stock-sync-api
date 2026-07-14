from fastapi import FastAPI
from app.database import engine, Base
from app.products import models as product_models
from app.orders import models as order_models
from app.sync import models as sync_models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Stock Sync API")


@app.get("/")
def health_check():
    return {"status": "ok", "service": "stock-sync-api"}