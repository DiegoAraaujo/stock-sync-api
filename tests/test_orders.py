def create_product(client, quantity=10):
    response = client.post(
        "/products/",
        json={
            "name": "Estante",
            "category": "Sala",
            "price": 450,
            "quantity": quantity,
        },
    )
    return response.json()["id"]


def test_create_order_success(client):
    product_id = create_product(client, quantity=10)

    response = client.post("/orders/", json={"product_id": product_id, "quantity": 4})
    assert response.status_code == 201
    assert response.json()["quantity"] == 4

    product_response = client.get(f"/products/{product_id}")
    assert product_response.json()["quantity"] == 6


def test_create_order_insufficient_stock(client):
    product_id = create_product(client, quantity=2)

    response = client.post("/orders/", json={"product_id": product_id, "quantity": 5})
    assert response.status_code == 400
    assert "Insufficient stock" in response.json()["detail"]


def test_create_order_product_not_found(client):
    response = client.post("/orders/", json={"product_id": 999, "quantity": 1})
    assert response.status_code == 404


def test_order_does_not_reduce_stock_on_failure(client):
    product_id = create_product(client, quantity=3)

    client.post("/orders/", json={"product_id": product_id, "quantity": 10})

    product_response = client.get(f"/products/{product_id}")
    assert product_response.json()["quantity"] == 3
