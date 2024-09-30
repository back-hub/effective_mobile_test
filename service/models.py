from db.db import Base
from sqlalchemy import Column, ForeignKey, sql, String, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Product(Base):
    __tablename__="product"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)


class Order(Base):
    __tablename__="order"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    created_at = Column(TIMESTAMP, default=sql.func.now())
    status = Column(String, default="В процессе")

    items = relationship("OrderItem", back_populates="order")
    

class OrderItem(Base):
    __tablename__="order_item"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")