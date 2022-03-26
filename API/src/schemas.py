import datetime

from fastapi import Body, Form
from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    uid: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    class Config:
        orm_mode = True

class CabinetBase(BaseModel):
    id: str
    description: Optional[str] = None

class CabinetCreate(CabinetBase):
    pass

class Cabinet(CabinetBase):
    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    title: str
    description: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: Optional[float] = None
    link: Optional[str] = None
    category_id: Optional[int] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True

class OrderRequestBase(BaseModel):
    item_id: int
    user_id: str

class OrderRequestCreate(OrderRequestBase):
    pass

class OrderRequest(OrderRequestBase):
    id: int
    date: datetime.datetime
    state: int

    class Config:
        orm_mode = True

class StorageUnitBase(BaseModel):
    id: int
    state: Optional[int] = 0
    verified: Optional[bool] = False
    item_id: int
    cabinet_id: Optional[str] = None

class StorageUnitCreate(StorageUnitBase):
    pass

class StorageUnit(StorageUnitBase):

    class Config:
        orm_mode = True

class CabinetUnlockAttemptBase(BaseModel):
    user_id: str
    cabinet_id: str
    granted: Optional[bool] = False

class CabinetUnlockAttemptCreate(CabinetUnlockAttemptBase):
    pass

class CabinetUnlockAttempt(CabinetUnlockAttemptBase):
    id: int
    date: datetime.datetime

    class Config:
        orm_mode = True