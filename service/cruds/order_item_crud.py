from sqlalchemy.orm import Session
from service import models
from service.pydantic_models import order_item_py_models


def create_order_item(db: Session, order_id: int, order_item_request: order_item_py_models.OrderItemRequest):
    db_order_item = models.OrderItem(
        order_id=order_id,
        product_id=order_item_request.product_id,
        quantity=order_item_request.quantity
    )
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)
    return db_order_item