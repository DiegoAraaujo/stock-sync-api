from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class StockSyncWebhook(BaseModel):
    product_id: int
    new_quantity: int
    source: str


class SyncLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: Optional[int]
    previous_quantity: Optional[int]
    new_quantity: Optional[int]
    source: str
    success: bool
    error_message: Optional[str]
    created_at: datetime
