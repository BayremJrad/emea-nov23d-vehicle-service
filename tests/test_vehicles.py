"""Contract tests for the Vehicle Service API.

These mirror the tests defined in the Vehicle Service Collection:
 - Status codes are one of 200/201/204 for happy paths.
 - "Retrieve a vehicle" returns an object with the full vehicle schema and
   correct field types, and the id matches the requested id.
 - "Create a vehicle" returns a vehicle whose `vin` is a string.
"""

import pytest

from app.main import EXPECTED_API_KEY, create_app

AUTH = {"X-API-Key": EXPECTED_API_KEY}

VEHICLE_FIELDS = {
    "id": int,
    "nickName": str,
    "vin": str,
    "make": str,
    "model": str,
    "year": str,
    "miles": int,
}


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


def _assert_vehicle_contract(vehicle):
    for field, expected_type in VEHICLE_FIELDS.items():
        assert field in vehicle, f"missing field: {field}"
        assert isinstance(vehicle[field], expected_type), f"wrong type for {field}"


def test_requires_api_key(client):
    resp = client.get("/vehicles")
    assert resp.status_code == 401


def test_get_all_vehicles(client):
    resp = client.get("/vehicles", headers=AUTH)
    assert resp.status_code == 200
    body = resp.get_json()
    assert isinstance(body, list)
    for vehicle in body:
        _assert_vehicle_contract(vehicle)


def test_retrieve_a_vehicle_contract(client):
    resp = client.get("/vehicles/1", headers=AUTH)
    assert resp.status_code == 200
    body = resp.get_json()
    _assert_vehicle_contract(body)
    assert body["id"] == 1


def test_retrieve_missing_vehicle_returns_404(client):
    resp = client.get("/vehicles/9999", headers=AUTH)
    assert resp.status_code == 404
    assert "message" in resp.get_json()


def test_create_a_vehicle(client):
    payload = {
        "nickName": "Night Rider",
        "vin": "JN8AZ2KR1AT169594",
        "make": "Nissan",
        "model": "Cube",
        "year": "2010",
        "miles": 42000,
    }
    resp = client.post("/vehicles", json=payload, headers=AUTH)
    assert resp.status_code == 201
    body = resp.get_json()
    assert isinstance(body["vin"], str)
    assert body["id"]


def test_create_missing_required_attribute_returns_400(client):
    resp = client.post("/vehicles", json={"make": "Nissan"}, headers=AUTH)
    assert resp.status_code == 400
    assert "message" in resp.get_json()


def test_create_duplicate_vin_returns_409(client):
    resp = client.post(
        "/vehicles",
        json={
            "nickName": "Dup",
            "vin": "4M2DV11W4RDJ53329",
            "make": "Mercury",
            "model": "Villager",
            "year": "1994",
        },
        headers=AUTH,
    )
    assert resp.status_code == 409


def test_update_a_vehicle(client):
    resp = client.patch("/vehicles/1", json={"miles": 159999}, headers=AUTH)
    assert resp.status_code == 200
    assert resp.get_json()["miles"] == 159999


def test_delete_a_vehicle(client):
    create = client.post(
        "/vehicles",
        json={
            "nickName": "Temp",
            "vin": "TEMPVIN1234567890",
            "make": "Test",
            "model": "Model",
            "year": "2020",
        },
        headers=AUTH,
    )
    vehicle_id = create.get_json()["id"]
    resp = client.delete(f"/vehicles/{vehicle_id}", headers=AUTH)
    assert resp.status_code == 204
