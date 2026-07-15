from sqlalchemy.orm import Session
from app.sync.models import SyncLog
from app.sync.schemas import StockSyncWebhook
from app.products.models import Product


def process_stock_webhook(db: Session, data: StockSyncWebhook) -> SyncLog:
    product = db.query(Product).filter(Product.id == data.product_id).first()

    if not product:
        log = SyncLog(
            product_id=data.product_id,
            previous_quantity=None,
            new_quantity=data.new_quantity,
            source=data.source,
            success=False,
            error_message=f"Product {data.product_id} not found",
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    previous_quantity = product.quantity
    product.quantity = data.new_quantity

    log = SyncLog(
        product_id=product.id,
        previous_quantity=previous_quantity,
        new_quantity=data.new_quantity,
        source=data.source,
        success=True,
        error_message=None,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_logs(db: Session, only_errors: bool = False):
    query = db.query(SyncLog)
    if only_errors:
        query = query.filter(SyncLog.success == False)
    return query.order_by(SyncLog.created_at.desc()).all()