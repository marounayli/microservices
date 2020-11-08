from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, relationship
from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, DateTime
from sqlalchemy.sql.schema import ForeignKey, PrimaryKeyConstraint
import enum

from sqlalchemy.sql.sqltypes import DateTime

class PaymentType(enum.enum):
    cash = 'CASH'
    credit = 'CREDIT'
    cheque = 'CHEQUE'

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address = Column(String)
    countryCode = Column(Integer)
    email = Column(String)

    # Defining relationships
    order = relationship("Order")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)   
    productDescription = Column(String)
    pricePerUnit = Column(Float)
    currency = Column(String)
    quantityAvailable = Column(Integer)

    # Defining relationships
    order = relationship("Order", uselist=False, back_populates="products")


class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

    # Defining relationships
    product = relationship("Product", back_populates="orders")
    payment = relationship("Payment", uselist=False, back_populates='orders')
    shipment = relationship("Shipment", uselist=False, back_populates='orders')


class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    paymentType = Column(Enum(PaymentType))
    paymentSuccesful = Column(Boolean)

    # Defining relationships
    order = relationship("Order", back_populates='payments')



class Shipment(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    unitWeight = Column(Float)
    unitDimension = Column(String)
    estimatedArrival = Column(DateTime)
    initiatedTime = Column(DateTime)
    initiated = Column(Boolean)
    arrived = Column(Boolean)

    # Defining relationships
    order = relationship("Order", back_populates='shipments')

    
    