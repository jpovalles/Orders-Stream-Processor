from sqlalchemy import Column, Integer, String
from .conn import Base

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True)
    status = Column(String(100))
    type = Column(String(100))

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    product = Column(String(100))
    product_qty = Column(Integer)