def test_create_product(client):
    response = client.post("/products/", json={
        "name": "Cadeira Gamer",
        "category": "Escritório",
        "price": 799.90,
        "quantity": 5
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Cadeira Gamer"
    assert data["quantity"] == 5


def test_list_products(client):
    client.post("/products/", json={
        "name": "Mesa", "category": "Escritório", "price": 300, "quantity": 3
    })
    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_product_not_found(client):
    response = client.get("/products/999")
    assert response.status_code == 404


def test_update_stock(client):
    create_response = client.post("/products/", json={
        "name": "Monitor", "category": "Escritório", "price": 900, "quantity": 2
    })
    product_id = create_response.json()["id"]

    response = client.put(f"/products/{product_id}/stock", json={"quantity": 20})
    assert response.status_code == 200
    assert response.json()["quantity"] == 20


def test_delete_product(client):
    create_response = client.post("/products/", json={
        "name": "Teclado", "category": "Escritório", "price": 150, "quantity": 8
    })
    product_id = create_response.json()["id"]

    delete_response = client.delete(f"/products/{product_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404