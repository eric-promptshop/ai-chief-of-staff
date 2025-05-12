"""
Unit tests for the health endpoint.
"""
from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)

def test_health_endpoint():
    """Test that the health endpoint returns 200 and expected data."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "name" in data
    assert "version" in data 