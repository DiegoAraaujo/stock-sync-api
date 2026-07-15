from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.sync import service
from app.sync.schemas import StockSyncWebhook, SyncLogResponse

router = APIRouter(tags=["sync"])


@router.post("/webhooks/stock", response_model=SyncLogResponse, status_code=201)
def stock_webhook(data: StockSyncWebhook, db: Session = Depends(get_db)):
    return service.process_stock_webhook(db, data)


@router.get("/logs/sync", response_model=list[SyncLogResponse])
def list_sync_logs(only_errors: bool = False, db: Session = Depends(get_db)):
    return service.get_logs(db, only_errors)