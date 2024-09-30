from sqlalchemy.orm import Session
from uuid import UUID
from service import models
from service.pydantic_models import order_py_models


def get_orders(db: Session):
    return db.query(models.Order).all()

def get_order_by_id(db: Session, id: UUID):
    return db.query(models.Order).filter(models.Order.id == id).first()

def create_order(db: Session):
    db_order = models.Order()
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def edit_order(db: Session, id: int, status: str):
    db_order = db.query(models.Order).filter(models.Order.id==id).one()
    db_order.status = status
    db.commit()
    db.refresh(db_order)
    return db_order