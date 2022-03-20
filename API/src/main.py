import crud, models, schemas

from database import SessionLocal
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# USERS

@app.get("/users/", response_model=List[schemas.User])
def read_all_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)

@app.get("/user/{uid}/", response_model=schemas.User)
def read_user_by_uid(uid: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_uid(db, uid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_uid(db, user.uid)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return crud.create_user(db=db, user=user)

@app.delete("/user/{uid}/")
def delete_user_by_uid(uid: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_uid(db, uid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {'Deleted user with uid': uid}

# CABINETS

@app.get("/cabinets/", response_model=List[schemas.Cabinet])
def read_all_cabinets(db: Session = Depends(get_db)):
    return crud.get_all_cabinets(db)

@app.get("/cabinet/{id}/", response_model=schemas.Cabinet)
def read_cabinet_by_id(id: str, db: Session = Depends(get_db)):
    db_cabinet = crud.get_cabinet_by_id(db, id)
    if db_cabinet is None:
        raise HTTPException(status_code=404, detail="Cabinet not found")
    return db_cabinet

@app.post("/cabinet/", response_model=schemas.Cabinet)
def create_cabinet(cabinet: schemas.CabinetCreate, db: Session = Depends(get_db)):
    db_cabinet = crud.get_cabinet_by_id(db, cabinet.id)
    if db_cabinet:
        raise HTTPException(status_code=400, detail="Cabinet already exists")
    return crud.create_cabinet(db, cabinet)

@app.delete("/cabinet/{id}/")
def delete_cabinet_by_id(id: str, db: Session = Depends(get_db)):
    db_cabinet = crud.get_cabinet_by_id(db, id)
    if db_cabinet is None:
        raise HTTPException(status_code=404, detail="Cabinet not found")
    db.delete(db_cabinet)
    db.commit()
    return {'Deleted cabinet with id': id}

# CATEGORIES

@app.get("/categories/", response_model=List[schemas.Category]) # reads all root categories
def read_root_categories(db: Session = Depends(get_db)):
    return crud.get_root_categories(db)

@app.get("/categories/subcategories/{parent_id}/", response_model=List[schemas.Category]) # reads all sub-categories of a category
def read_sub_categories(parent_id: int, db: Session = Depends(get_db)):
    parent_category = crud.get_category_by_id(db, parent_id)
    if not parent_category:
        raise HTTPException(status_code=404, detail="Parent category not found")
    return crud.get_sub_categories(db, parent_id)

@app.post("/category/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_title(db, category.title)
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    if category.parent_id is not None:
        db_parent_category = crud.get_category_by_id(db, category.parent_id)
        if db_parent_category is None:
            raise HTTPException(status_code=404, detail="Parent category not found")
    return crud.create_category(db, category)

@app.delete("/category/{id}/")
def delete_category_by_id(id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_id(db, id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return {'Deleted category with id': id}

# ITEMS

@app.get("/items/", response_model=List[schemas.Item])
def read_all_items(db: Session = Depends(get_db)):
    return crud.get_all_items(db)

@app.get("/item/{id}/", response_model=schemas.Item)
def read_item_by_id(id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_id(db, id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/categories/{category_id}/items/", response_model=List[schemas.Item]) # reads all items under a category
def read_all_items(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.get_items_by_category_id(db, category_id)

@app.post("/item/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    if item.category_id is not None:
        db_category = crud.get_category_by_id(db, item.category_id)
        if not db_category:
            raise HTTPException(status_code=404, detail="Category not found")
    db_item = crud.get_item_by_title(db, item.title)
    if db_item:
        raise HTTPException(status_code=400, detail="Item already exists")
    return crud.create_item(db, item)

@app.delete("/item/{id}/")
def delete_item_by_id(id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_id(db, id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {'Deleted item with id': id}

# ORDER REQUESTS

@app.get("/order-requests/", response_model=List[schemas.OrderRequest])
def read_all_order_requests(db: Session = Depends(get_db)):
    return crud.get_all_order_requests(db)

@app.get("/order-requests/item/{id}/", response_model=List[schemas.OrderRequest])
def read_order_requests_by_item_id(id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_id(db, id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.get_order_requests_by_item_id(db, id)

@app.get("/order-requests/user/{uid}/", response_model=List[schemas.OrderRequest])
def read_order_requests_by_user_id(uid: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_uid(db, uid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_order_requests_by_user_id(db, uid)

@app.get("/order-requests/state/{state}/", response_model=List[schemas.OrderRequest])
def read_order_requests_by_state(state: int, db: Session = Depends(get_db)):
    return crud.get_order_requests_by_state(db, state)

@app.post("/order-request/", response_model=schemas.OrderRequest)
def create_order_request(order_request: schemas.OrderRequestCreate, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_id(db, order_request.item_id)
    db_user = crud.get_user_by_uid(db, order_request.user_id)
    if db_item is None or db_user is None:
        raise HTTPException(status_code=404, detail="Item or user not found")
    db_order_request = crud.get_order_requests_by_item_and_user_id(db, order_request.item_id, order_request.user_id)
    if db_order_request:
        raise HTTPException(status_code=400, detail="Order already requested by this user")
    return crud.create_order_request(db, order_request)

@app.delete("/order-request/{id}/")
def delete_order_request_by_id(id: int, db: Session = Depends(get_db)):
    db_order_request = crud.get_order_request_by_id(db, id)
    if db_order_request is None:
        raise HTTPException(status_code=404, detail="Order request not found")
    db.delete(db_order_request)
    db.commit()
    return {'Deleted order request with id': id}

# STORAGE UNITS

@app.get("/storage-unit/{id}/", response_model=schemas.StorageUnit)
def read_storage_unit_by_id(id: int, db: Session = Depends(get_db)):
    db_storage_unit = crud.get_storage_unit_by_id(db, id)
    if db_storage_unit is None:
        raise HTTPException(status_code=404, detail="Storage unit not found")
    return db_storage_unit

@app.get("/storage-units/cabinet/{cabinet_id}/", response_model=List[schemas.StorageUnit])
def read_storage_units_by_cabinet_id(cabinet_id: str, db: Session = Depends(get_db)):
    db_cabinet = crud.get_cabinet_by_id(db, cabinet_id)
    if db_cabinet is None:
        raise HTTPException(status_code=404, detail="Cabinet not found")
    return crud.get_storage_units_by_cabinet_id(db, cabinet_id)    

@app.post("/storage-unit/", response_model=schemas.StorageUnit)
def create_storage_unit(storage_unit: schemas.StorageUnitCreate, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_id(db, storage_unit.item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if storage_unit.cabinet_id is not None:
        db_cabinet = crud.get_cabinet_by_id(db, storage_unit.cabinet_id)
        if db_cabinet is None:
            raise HTTPException(status_code=404, detail="Cabinet not found")
    db_storage_unit = crud.get_storage_unit_by_id(db, storage_unit.id)
    if db_storage_unit:
        raise HTTPException(status_code=400, detail="Storage unit ID already assigned")
    return crud.create_storage_unit(db, storage_unit)

@app.delete("/storage-unit/{id}/")
def delete_storage_unit_by_id(id: int, db: Session = Depends(get_db)):
    db_storage_unit = crud.get_storage_unit_by_id(db, id)
    if db_storage_unit is None:
        raise HTTPException(status_code=404, detail="Storage unit not found")
    db.delete(db_storage_unit)
    db.commit()
    return {'Deleted storage unit with id': id}

# CABINETS UNLOCK ATTEMPTS

@app.get("/unlock-attempts/", response_model=List[schemas.CabinetUnlockAttempt])
def read_all_unlock_attempts(db: Session = Depends(get_db)):
    return crud.get_all_unlock_attempts(db)

@app.get("/unlock-attempts/cabinet/{cabinet_id}/", response_model=List[schemas.CabinetUnlockAttempt])
def read_unlock_attempts_by_cabinet_id(cabinet_id: str, db: Session = Depends(get_db)):
    db_cabinet = crud.get_cabinet_by_id(db, cabinet_id)
    if db_cabinet is None:
        raise HTTPException(status_code=404, detail="Cabinet not found")
    return crud.get_unlock_attempts_by_cabinet_id(db, cabinet_id)

@app.get("/unlock-attempts/user/{uid}/", response_model=List[schemas.CabinetUnlockAttempt])
def read_unlock_attempts_by_user_id(uid: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_uid(db, uid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_unlock_attempts_by_user_id(db, uid)

@app.get("/unlock-attempts/cabinet/{cabinet_id}/user/{uid}/", response_model=List[schemas.CabinetUnlockAttempt])
def read_unlock_attempts_by_cabinet_and_user_id(cabinet_id, uid: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_uid(db, uid)
    db_cabinet = crud.get_cabinet_by_id(db, cabinet_id)
    if db_user is None or db_cabinet is None:
        raise HTTPException(status_code=404, detail="User or cabinet not found")
    return crud.get_unlock_attempts_by_cabinet_and_user_id(db, cabinet_id, uid)

@app.post("/unlock-attempt/", response_model=schemas.CabinetUnlockAttempt)
def create_unlock_attempt(unlock_attempt: schemas.CabinetUnlockAttemptCreate , db: Session = Depends(get_db)):
    db_user = crud.get_user_by_uid(db, unlock_attempt.user_id)
    db_cabinet = crud.get_cabinet_by_id(db, unlock_attempt.cabinet_id)
    if db_user is None or db_cabinet is None:
        raise HTTPException(status_code=404, detail="User or cabinet not found")
    return crud.create_unlock_attempt(db, unlock_attempt)

@app.delete("/unlock-attempts/days/{n}/")
def delete_unlock_attempts_older_than(n: int, db: Session = Depends(get_db)):
    db.execute(f"delete from cabinets_unlock_attempts where date < now() - interval '{n} days';")
    db.commit()
    return {'Deleted all cabinets unlock attempts older than number of days': n}