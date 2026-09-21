import json, os
from unittest.mock import patch
import requests
import phase2_observability as obs
import runtime_participation as rp


def test_safe_error_redacts_secret():
    value = obs.sanitize_error("authorization=Bearer-secret api_key=abc123")
    assert "abc123" not in value and "REDACTED" in value

@patch("runtime_participation.requests.post")
def test_registry_timeout_is_safe(mock_post):
    mock_post.side_effect = requests.Timeout("timed out")
    result = rp.register_runtime()
    assert result["status"] == "REGISTRY_UNAVAILABLE"
    assert result["response_body"] is None


def test_metrics_are_numeric():
    snap = obs.metrics_snapshot()
    assert all(isinstance(v, int) and v >= 0 for v in snap.values())
