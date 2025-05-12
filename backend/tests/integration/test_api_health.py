"""
Integration tests for the API health endpoint.
"""
import pytest

@pytest.mark.integration
def test_health_endpoint_integration(client):
    """Test the health endpoint with actual API call."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "name" in data
    assert "version" in data 