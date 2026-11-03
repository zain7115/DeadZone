"""
DeadZone Backend API Test Suite
Tests all 5 core endpoints against FastAPI application.
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["server"] == "deadzone-backend"

def test_get_active_survey():
    response = client.get("/api/surveys/active")
    assert response.status_code == 200
    data = response.json()
    assert data["surveyId"] == "DZ-2026-10-14"
    assert data["building"] == "North Block"
    assert len(data["measurements"]) >= 5
    assert len(data["heatCells"]) == 96 or len(data["heatCells"]) == 84 or len(data["heatCells"]) > 0

def test_get_map_points():
    response = client.get("/api/surveys/map-points")
    assert response.status_code == 200
    data = response.json()
    assert "points" in data
    assert len(data["points"]) >= 5
    point_ids = [p["id"] for p in data["points"]]
    assert "P-041" in point_ids

def test_add_measurement():
    payload = {
        "point": "P-042",
        "zone": "Testing Lab",
        "rssi": -52.0,
        "latency": 15.0,
        "loss": 0.1,
        "throughput": 95.0,
        "channel": "36 / 5 GHz"
    }
    response = client.post("/api/surveys/measurements", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["measurement"]["point"] == "P-042"
    assert data["measurement"]["status"] == "Good"

def test_add_measurement_validation():
    payload = {"zone": "Nowhere"}  # Missing point and rssi
    response = client.post("/api/surveys/measurements", json=payload)
    assert response.status_code in (400, 422)

def test_optimization_run():
    payload = {
        "coordinates": [
            {"id": "P-041", "x": 23, "y": 25},
            {"id": "P-040", "x": 47, "y": 33}
        ]
    }
    response = client.post("/api/optimization/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert len(data["candidates"]) >= 3
    assert data["candidates"][0]["label"] == "AP-C04"
