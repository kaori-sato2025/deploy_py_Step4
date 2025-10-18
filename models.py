from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "product_master"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    price = Column(Integer)

class Purchase(Base):
    __tablename__ = "purchase_history"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(255))
    name = Column(String(255))
    price = Column(Integer)
    purchased_at = Column(String)