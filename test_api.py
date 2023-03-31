from fastapi.testclient import TestClient
from strongmind import app

client = TestClient(app)

def test_db_empty():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"toppings":[],"pizzas":[]}

def test_valid_add_topping():
    response = client.post("/addTopping/ham")
    assert response.status_code == 200
    assert response.json() == { "id": 1, "title": "ham"}

def test_invalid_add_topping():
    response = client.post("/addTopping/ham")
    assert response.status_code == 200
    assert response.json() == ["Topping not added."]

def test_valid_update_topping():
    response = client.post("/updateTopping/1/pineapple")
    assert response.status_code == 200
    assert response.json() == { "id": 1, "title": "pineapple"}

def test_invalid_update_topping_id():
    response = client.post("/updateTopping/2/pineapple")
    assert response.status_code == 200
    assert response.json() == ["Topping id does not exist in database"]

def test_invalid_update_topping_title():
    response = client.post("/updateTopping/1/pineapple")
    assert response.status_code == 200
    assert response.json() == ["Topping already in database. No changes made"]

def test_valid_delete_topping():
    response = client.post("/deleteTopping/1/")
    assert response.status_code == 200
    assert response.json() == ["Topping deleted"]

def test_invalid_delete_topping_id():
    response = client.post("/deleteTopping/2/")
    assert response.status_code == 200
    assert response.json() == ["Topping id does not exist in database"]

def test_valid_add_pizza():
    response = client.post("/addPizza/david/ham")
    assert response.status_code == 200
    assert response.json() == { "id": 1, "title": "david", "toppings": "ham"}

def test_invalid_add_pizza():
    response = client.post("/addPizza/david/ham")
    assert response.status_code == 200
    assert response.json() == ["Pizza not added."]

def test_valid_update_pizza():
    response = client.post("/updatePizza/1/cody")
    assert response.status_code == 200
    assert response.json() == { "id": 1, "title": "cody", "toppings": "ham"}

def test_invalid_update_pizza_id():
    response = client.post("/updatePizza/2/cody")
    assert response.status_code == 200
    assert response.json() == ["Pizza id does not exist in database"]

def test_invalid_update_pizza_title():
    response = client.post("/updatePizza/1/cody")
    assert response.status_code == 200
    assert response.json() == ["Pizza already in database. No changes made"]

def test_valid_update_pizza_toppings():
    response = client.post("/updatePizzaToppings/1/pineapple")
    assert response.status_code == 200
    assert response.json() == { "id": 1, "title": "cody", "toppings": "pineapple"}

def test_invalid_update_pizza_toppings_id():
    response = client.post("/updatePizzaToppings/2/pineapple")
    assert response.status_code == 200
    assert response.json() == ["Pizza id does not exist in database"]

def test_invalid_update_pizza_toppings():
    response = client.post("/updatePizzaToppings/1/pineapple")
    assert response.status_code == 200
    assert response.json() == ["Those are already the toppings for that pizza. No changes made"]

def test_valid_delete_pizza():
    response = client.post("/deletePizza/1/")
    assert response.status_code == 200
    assert response.json() == ["Pizza deleted"]

def test_invalid_delete_pizza_id():
    response = client.post("/deletePizza/2/")
    assert response.status_code == 200
    assert response.json() == ["Pizza id does not exist in database"]