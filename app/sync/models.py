from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class SyncLog(Base):
    __tablename__ = "sync_logs"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=True)
    previous_quantity = Column(Integer, nullable=True)
    new_quantity = Column(Integer, nullable=True)
    source = Column(String, nullable=False)
    success = Column(Boolean, nullable=False)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())