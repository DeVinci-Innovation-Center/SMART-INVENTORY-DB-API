import models, schemas

from sqlalchemy.orm import Session


# USERS

def get_all_users(db: Session):
    return db.query(models.User).all()

def get_user_by_uid(db: Session, uid: str):
    return db.query(models.User).filter(models.User.uid == uid).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(uid=user.uid, firstname=user.firstname, lastname=user.lastname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# CABINETS

def get_all_cabinets(db: Session):
    return db.query(models.Cabinet).all()

def get_cabinet_by_id(db: Session, id: str):
    return db.query(models.Cabinet).filter(models.Cabinet.id == id).first()

def create_cabinet(db: Session, cabinet: schemas.CabinetCreate):
    db_cabinet = models.Cabinet(id=cabinet.id, description=cabinet.description)
    db.add(db_cabinet)
    db.commit()
    db.refresh(db_cabinet)
    return db_cabinet

# CATEGORIES

def get_category_by_id(db: Session, id: int):
    return db.query(models.Category).filter(models.Category.id == id).first()

def get_category_by_title(db: Session, title: str):
    return db.query(models.Category).filter(models.Category.title == title).first()

def get_root_categories(db: Session):
    return db.query(models.Category).filter(models.Category.parent_id == None).all()

def get_sub_categories(db: Session, parent_id: int):
    return db.query(models.Category).filter(models.Category.parent_id == parent_id).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(title=category.title, description=category.description, parent_id=category.parent_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# ITEMS

def get_all_items(db: Session):
    return db.query(models.Item).all()

def get_item_by_id(db: Session, id: int):
    return db.query(models.Item).filter(models.Item.id == id).first()

def get_item_by_title(db: Session, title: str):
    return db.query(models.Item).filter(models.Item.title == title).first()

def get_items_by_category_id(db: Session, category_id: int):
    return db.query(models.Item).filter(models.Item.category_id == category_id).all()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(title=item.title, description=item.description, price=item.price, link=item.link, category_id=item.category_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# ORDER REQUESTS

def get_all_order_requests(db: Session):
    return db.query(models.OrderRequest).all()

def get_order_request_by_id(db: Session, id: int):
    return db.query(models.OrderRequest).filter(models.OrderRequest.id == id).first()

def get_order_requests_by_item_id(db: Session, item_id: int):
    return db.query(models.OrderRequest).filter(models.OrderRequest.item_id == item_id).all()
    
def get_order_requests_by_user_id(db: Session, uid: str):
    return db.query(models.OrderRequest).filter(models.OrderRequest.user_id == uid).all()

def get_order_requests_by_state(db: Session, state: int):
    return db.query(models.OrderRequest).filter(models.OrderRequest.state == state).all()

def create_order_request(db: Session, order_request: schemas.OrderRequest):
    db_order_request = models.OrderRequest(item_id=order_request.item_id, user_id=order_request.user_id)
    db.add(db_order_request)
    db.commit()
    db.refresh(db_order_request)
    return db_order_request

# STORAGE UNITS

def get_storage_unit_by_id(db: Session, id: int):
    return db.query(models.StorageUnit).filter(models.StorageUnit.id == id).first()

def get_storage_units_by_cabinet_id(db: Session, cabinet_id: str):
    return db.query(models.StorageUnit).filter(models.StorageUnit.cabinet_id == cabinet_id).all()

def create_storage_unit(db: Session, storage_unit: schemas.StorageUnit):
    db_storage_unit = models.StorageUnit(state=storage_unit.state, verified=storage_unit.verified, item_id=storage_unit.item_id, cabinet_id=storage_unit.cabinet_id)
    db.add(db_storage_unit)
    db.commit()
    db.refresh(db_storage_unit)
    return db_storage_unit

# CABINETS UNLOCK ATTEMPTS

def get_all_unlock_attempts(db: Session):
    return db.query(models.CabinetUnlockAttempt).all()

def get_unlock_attempts_by_cabinet_id(db: Session, cabinet_id : str):
    return db.query(models.CabinetUnlockAttempt).filter(models.CabinetUnlockAttempt.cabinet_id == cabinet_id).all()

def get_unlock_attempts_by_user_id(db: Session, user_id : str):
    return db.query(models.CabinetUnlockAttempt).filter(models.CabinetUnlockAttempt.user_id == user_id).all()

def get_unlock_attempts_by_cabinet_and_user_id(db: Session, cabinet_id: str, user_id : str):
    return db.query(models.CabinetUnlockAttempt).filter(models.CabinetUnlockAttempt.cabinet_id == cabinet_id).filter(models.CabinetUnlockAttempt.user_id == user_id).all()

def create_unlock_attempt(db: Session, unlock_attempt: schemas.CabinetUnlockAttempt):
    db_unlock_attempt = models.CabinetUnlockAttempt(granted=unlock_attempt.granted, user_id=unlock_attempt.user_id, cabinet_id=unlock_attempt.cabinet_id)
    db.add(db_unlock_attempt)
    db.commit()
    db.refresh(db_unlock_attempt)
    return db_unlock_attempt