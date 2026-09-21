import json
from unittest.mock import patch, Mock
import runtime_participation as rp


def test_registration_payload_matches_existing_registry_schema():
    payload = rp.registration_payload()
    assert set(payload) == {"name", "description", "category", "version", "author"}
    assert payload["version"] == "1.0.0"
    metadata = json.loads(payload["description"])
    assert "authority_boundary" in metadata
    assert "provenance_note" in metadata


@patch("runtime_participation.requests.post")
def test_valid_registration(mock_post):
    response = Mock(status_code=200)
    response.json.return_value = {"id": 1, **rp.registration_payload()}
    mock_post.return_value = response
    result = rp.register_runtime()
    assert result["status"] == "REGISTERED"
    assert result["response_status"] == 200


@patch("runtime_participation.discover_self")
@patch("runtime_participation.requests.post")
def test_duplicate_registration(mock_post, mock_discover):
    response = Mock(status_code=409)
    response.json.return_value = {"detail": "Module already exists."}
    mock_post.return_value = response
    mock_discover.return_value = {"id": 1, "name": rp.RUNTIME_IDENTITY}
    result = rp.register_runtime()
    assert result["status"] == "DUPLICATE_ALREADY_REGISTERED"
    assert result["response_status"] == 409


@patch("runtime_participation.requests.post")
def test_invalid_registration_rejection(mock_post):
    response = Mock(status_code=400)
    response.json.return_value = {"detail": "Invalid version format. Use x.y.z"}
    mock_post.return_value = response
    result = rp.register_runtime()
    assert result["status"] == "REJECTED"
    assert result["response_status"] == 400


@patch("runtime_participation.requests.post")
def test_registry_unavailable(mock_post):
    import requests
    mock_post.side_effect = requests.ConnectionError("connection refused")
    result = rp.register_runtime()
    assert result["status"] == "REGISTRY_UNAVAILABLE"
    assert "connection refused" in result["error"]
