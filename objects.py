from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, DateTime
from sqlalchemy.sql.schema import ForeignKey
import enum
from app import db
from sqlalchemy.sql.sqltypes import DateTime

# create an engine

class PaymentType(enum.Enum):
    cash = 'CASH'
    credit = 'CREDIT'
    cheque = 'CHEQUE'


class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address = Column(String)
    countryCode = Column(Integer)
    email = Column(String)

    # Defining relationships
    order = relationship("Order")

class Product(db.Model):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)   
    productDescription = Column(String)
    pricePerUnit = Column(Float)
    currency = Column(String)
    quantityAvailable = Column(Integer)

    # Defining relationships
    order = relationship("Order", uselist=False, back_populates="product")

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

    # Defining relationships
    product = relationship("Product", back_populates="order")
    payment = relationship("Payment", uselist=False, back_populates='order')
    shipment = relationship("Shipment", uselist=False, back_populates='order')


class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    paymentType = Column(Enum(PaymentType))
    paymentSuccesful = Column(Boolean)

    # Defining relationships
    order = relationship("Order", back_populates='payment')



class Shipment(db.Model):
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
    order = relationship("Order", back_populates='shipment')


