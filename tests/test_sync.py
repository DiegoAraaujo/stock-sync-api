def create_product(client, quantity=10):
    response = client.post(
        "/products/",
        json={
            "name": "Armário",
            "category": "Cozinha",
            "price": 1200,
            "quantity": quantity,
        },
    )
    return response.json()["id"]


def test_webhook_updates_existing_product(client):
    product_id = create_product(client, quantity=10)

    response = client.post(
        "/webhooks/stock",
        json={"product_id": product_id, "new_quantity": 30, "source": "erp-odoo"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["previous_quantity"] == 10
    assert data["new_quantity"] == 30

    product_response = client.get(f"/products/{product_id}")
    assert product_response.json()["quantity"] == 30


def test_webhook_logs_error_for_missing_product(client):
    response = client.post(
        "/webhooks/stock",
        json={"product_id": 9999, "new_quantity": 15, "source": "erp-odoo"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["success"] is False
    assert "not found" in data["error_message"]


def test_list_sync_logs(client):
    product_id = create_product(client)
    client.post(
        "/webhooks/stock",
        json={"product_id": product_id, "new_quantity": 5, "source": "erp-odoo"},
    )
    client.post(
        "/webhooks/stock",
        json={"product_id": 9999, "new_quantity": 5, "source": "erp-odoo"},
    )

    response = client.get("/logs/sync")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_filter_only_error_logs(client):
    product_id = create_product(client)
    client.post(
        "/webhooks/stock",
        json={"product_id": product_id, "new_quantity": 5, "source": "erp-odoo"},
    )
    client.post(
        "/webhooks/stock",
        json={"product_id": 9999, "new_quantity": 5, "source": "erp-odoo"},
    )

    response = client.get("/logs/sync?only_errors=true")
    assert response.status_code == 200
    logs = response.json()
    assert len(logs) == 1
    assert logs[0]["success"] is False
