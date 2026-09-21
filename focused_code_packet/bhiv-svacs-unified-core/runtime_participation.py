"""
Runtime participation adapter for the existing SVACS Runtime.

This adapter uses only the Capability Registry Foundation's existing REST contract:
POST /modules
GET  /modules
GET  /health

No registry schema is changed and no parallel registry is introduced.
"""
import os
import json
from datetime import datetime, timezone
from typing import Any, Dict

import requests

RUNTIME_IDENTITY = "SVACS Unified Core runtime"
RUNTIME_VERSION = "1.0.0"
RUNTIME_CATEGORY = "Runtime Execution Infrastructure"
RUNTIME_OWNER = "BHEX project owner/team (exact named owner not established)"
AUTHORITY_BOUNDARY = (
    "Owns only SVACS runtime execution/state/replay/telemetry for its documented chain; "
    "does not own registry governance, sovereign core authority, or unrelated application decisions."
)
COMPATIBILITY = "Capability Registry Foundation REST API /modules schema v1.0.0; semantic version x.y.z required."
REGISTRY_URL = os.getenv("CAPABILITY_REGISTRY_URL", "http://127.0.0.1:8001").rstrip("/")
REGISTRATION_TIMEOUT_SECONDS = float(os.getenv("REGISTRY_TIMEOUT_SECONDS", "5"))

_state: Dict[str, Any] = {
    "status": "NOT_ATTEMPTED",
    "registry_url": REGISTRY_URL,
    "last_attempt_utc": None,
    "response_status": None,
    "response_body": None,
    "error": None,
    "registry_record": None,
}


def registration_payload() -> Dict[str, str]:
    """Return the exact payload supported by the existing canonical registry schema."""
    metadata = {
        "stable_identity": RUNTIME_IDENTITY,
        "owner": RUNTIME_OWNER,
        "capability_scope": "Deterministic runtime execution, state, replay, provenance, telemetry and orchestration surfaces for the SVACS chain.",
        "authority_boundary": AUTHORITY_BOUNDARY,
        "compatibility": COMPATIBILITY,
        "provenance_note": "Runtime trace/provenance remains runtime-side because the existing registry schema has no structured provenance or trace fields.",
    }
    return {
        "name": RUNTIME_IDENTITY,
        "description": json.dumps(metadata, sort_keys=True),
        "category": RUNTIME_CATEGORY,
        "version": RUNTIME_VERSION,
        "author": RUNTIME_OWNER,
    }


def current_state() -> Dict[str, Any]:
    return dict(_state)


def _record_response(status: int, body: Any) -> Dict[str, Any]:
    _state.update(
        {
            "last_attempt_utc": datetime.now(timezone.utc).isoformat(),
            "response_status": status,
            "response_body": body,
            "error": None,
        }
    )
    if status == 200:
        _state["status"] = "REGISTERED"
        _state["registry_record"] = body
    elif status == 409:
        _state["status"] = "DUPLICATE_ALREADY_REGISTERED"
        _state["registry_record"] = discover_self()
    else:
        _state["status"] = "REJECTED"
    return current_state()


def register_runtime() -> Dict[str, Any]:
    """Submit the existing runtime through the existing /modules contract."""
    payload = registration_payload()
    _state["registry_url"] = REGISTRY_URL
    try:
        response = requests.post(
            f"{REGISTRY_URL}/modules",
            json=payload,
            timeout=REGISTRATION_TIMEOUT_SECONDS,
        )
        try:
            body = response.json()
        except ValueError:
            body = {"raw": response.text}
        return _record_response(response.status_code, body)
    except requests.RequestException as exc:
        _state.update(
            {
                "status": "REGISTRY_UNAVAILABLE",
                "last_attempt_utc": datetime.now(timezone.utc).isoformat(),
                "response_status": None,
                "response_body": None,
                "error": f"{type(exc).__name__}: {exc}",
                "registry_record": None,
            }
        )
        return current_state()


def discover_self() -> Any:
    """Discover this participant through the registry's existing GET /modules API."""
    try:
        response = requests.get(
            f"{REGISTRY_URL}/modules",
            timeout=REGISTRATION_TIMEOUT_SECONDS,
        )
        if response.status_code != 200:
            return {"status": "DISCOVERY_FAILED", "http_status": response.status_code}
        modules = response.json()
        for module in modules:
            if module.get("name") == RUNTIME_IDENTITY:
                return module
        return None
    except requests.RequestException as exc:
        return {"status": "REGISTRY_UNAVAILABLE", "error": f"{type(exc).__name__}: {exc}"}


def provenance_sample() -> Dict[str, Any]:
    """Read an existing runtime trace without manufacturing a new trace."""
    candidates = [
        "runtime_proof_logs/runtime/single_trace_runtime.json",
        "runtime/single_trace_runtime.json",
        "single_trace_full_proof.json",
    ]
    for relative in candidates:
        if os.path.exists(relative):
            with open(relative, encoding="utf-8") as f:
                data = json.load(f)
            return {"source": relative, "trace": data}
    return {"source": None, "trace": None}
