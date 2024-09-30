from sqlalchemy.orm import Session
from uuid import UUID
from service import models
from datetime import datetime
from service.pydantic_models import product_py_models


def get_products(db: Session):
    return db.query(models.Product).all()


def get_product_by_name(db: Session, name: str):
    return db.query(models.Product).filter(models.Product.name == name).first()

def check_quantity(db: Session, order_items: list):
    for element in order_items:
        db_product = get_product_by_id(db, id=element.product_id)
        if db_product.quantity < element.quantity:
            return element.product_id
    return False

def get_product_by_id(db: Session, id: UUID):
    return db.query(models.Product).filter(models.Product.id == id).first()

def create_product(db: Session, product_request: product_py_models.ProductRequest):
    db_product = models.Product(
        name=product_request.name,
        description=product_request.description,
        price=product_request.price,
        quantity=product_request.quantity
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product



def delete_product(db: Session, id: int):
    db_product = db.query(models.Product).filter(models.Product.id==id).one()
    db.delete(db_product)
    db.commit()
    return True

def edit_product(db: Session, id: int, product_request: product_py_models.ProductRequest):
    db_product = db.query(models.Product).filter(models.Product.id==id).one()
    db_product.name = product_request.name
    db_product.description = product_request.description
    db_product.price = product_request.price
    db_product.quantity = product_request.quantity
    db.commit()
    db.refresh(db_product)
    return db_product

def decrease_quantity(db: Session, id: int, quantity: int):
    db_product = get_product_by_id(db=db, id=id)
    db_product.quantity -= quantity
    db.commit()
    db.refresh(db_product)
    return db_product
