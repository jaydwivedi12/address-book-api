import os
import tempfile

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.base import Base
from app.db.session import engine


# Use a temporary database for testing
@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_create_address():
    response = client.post(
        "/api/v1/addresses",
        json={
            "name": "Home",
            "latitude": 12.9716,
            "longitude": 77.5946,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Home"
    assert "id" in data


def test_get_addresses():
    response = client.get("/api/v1/addresses")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_find_nearby_address():
    response = client.get(
        "/api/v1/addresses/nearby",
        params={
            "latitude": 12.9716,
            "longitude": 77.5946,
            "distance_km": 5,
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)