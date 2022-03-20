from database import Base
from sqlalchemy import ForeignKey, Integer, String, Float, Column, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = 'users'
    uid = Column(String(11), primary_key=True)
    firstname = Column(String)
    lastname = Column(String)

    order_requests = relationship("OrderRequest", backref="user") # we can call exampleOrderRequest.user and exampleUser.order_requests
    cabinets_unlock_attempts = relationship("CabinetUnlockAttempt", backref="user") # we can call exampleCabinetUnlockAttempt.user and exampleUser.cabinets_unlock_attempts

class Cabinet(Base):
    __tablename__ = 'cabinets'
    id = Column(String, primary_key=True)
    description = Column(String)

    cabinet_unlock_attempts = relationship("CabinetUnlockAttempt", backref="cabinet") # we can call exampleCabinetUnlockAttempt.cabinet and exampleCabinet.cabinet_unlock_attempts
    storage_units = relationship("StorageUnit", backref="cabinet") # we can call exampleStorageUnit.cabinet and exampleCabinet.storage_units

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String)
    parent_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)

    category = relationship("Category", remote_side=[id]) # exampleCategory.category returns the category's parent
    items = relationship("Item", backref="category") # we can call exampleItem.category and exampleCategory.items

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String)
    price = Column(Float)
    link = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL'))

class OrderRequest(Base):
    __tablename__ = 'order_requests'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    state = Column(Integer, default=0)
    item_id = Column(Integer, ForeignKey('items.id', ondelete='CASCADE'))
    user_id = Column(String, ForeignKey('users.uid', ondelete='CASCADE'))

    item = relationship("Item", backref="orders") # we can call exampleItem.orders and exampleOrder.item

class StorageUnit(Base):
    __tablename__ = 'storage_units'
    id = Column(Integer, primary_key=True)
    state = Column(Integer, default=0)
    verified = Column(Boolean, default=False)
    item_id = Column(Integer, ForeignKey('items.id', ondelete='SET NULL'))
    cabinet_id = Column(String, ForeignKey('cabinets.id', ondelete='SET NULL'))

    item = relationship("Item", backref="storage_units") # we can call exampleItem.storage_units and exampleStorageUnit.item

class CabinetUnlockAttempt(Base):
    __tablename__ = 'cabinets_unlock_attempts'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    granted = Column(Boolean, default=False)
    user_id = Column(String, ForeignKey('users.uid', ondelete='CASCADE'))
    cabinet_id = Column(String, ForeignKey('cabinets.id', ondelete='CASCADE'))