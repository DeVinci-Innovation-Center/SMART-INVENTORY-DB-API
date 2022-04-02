from app.main import app
from fastapi.testclient import TestClient


client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Smart Inventory"}

def test_create_category():
    response = client.post("/category/", json={"title": "Soft Materials"})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Soft Materials",
        "description": None,
        "parent_id": None
    }

def test_create_subcategory():
    response = client.post("/category/", json={"title": "Silicon", "parent_id": 1})
    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "title": "Silicon",
        "description": None,
        "parent_id": 1
    }

def test_read_category():
    response = client.get("/category/1/")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Soft Materials",
        "description": None,
        "parent_id": None
    }

def test_read_inexistent_category():
    response = client.get("/category/999/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}

def test_create_item():
    response = client.post("/item/", json={"title": "Bobine PLA", "description": "Gris 1kg", "price":19.99, "link": "amazon.fr", "category_id": 1})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Bobine PLA",
        "description": "Gris 1kg",
        "price": 19.99,
        "link": "amazon.fr",
        "category_id": 1
    }

def test_read_item():
    response = client.get("/item/1/")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Bobine PLA",
        "description": "Gris 1kg",
        "price": 19.99,
        "link": "amazon.fr",
        "category_id": 1
    }

def test_read_inexistent_item():
    response = client.get("/item/999/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_create_existing_item():
    response = client.post("/item/", json={"title": "Bobine PLA", "description": "Gris 1kg", "price":19.99, "link": "amazon.fr"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Item already exists"}

def test_delete_category():
    response = client.delete("/category/1/")
    assert response.status_code == 200
    assert response.json() == {'Deleted category with id': 1}
    response = client.get("/category/2/")
    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "title": "Silicon",
        "description": None,
        "parent_id": None
    }
    response = client.get("/item/1/")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Bobine PLA",
        "description": "Gris 1kg",
        "price": 19.99,
        "link": "amazon.fr",
        "category_id": None
    }

def test_delete_item():
    response = client.delete("/item/1/")
    assert response.status_code == 200
    assert response.json() == {'Deleted item with id': 1}

def test_delete_inexistent_item():
    response = client.delete("/item/999/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}