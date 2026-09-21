import json
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_CANDIDATES = [
    _ROOT / "data" / "janes_runtime_registry.json",
    _ROOT / "janes_runtime_registry.json",
    _ROOT / "maritime_knowledge" / "janes_runtime_registry.json",
]
_REGISTRY_PATH = next((p for p in _CANDIDATES if p.exists()), None)
if _REGISTRY_PATH is None:
    raise FileNotFoundError("No Jane's runtime registry found in approved runtime locations")
with _REGISTRY_PATH.open(encoding="utf-8") as f:
    REGISTRY = json.load(f)


def get_vessel_metadata(mmsi):
    for vessel in REGISTRY:
        if vessel.get("mmsi") == str(mmsi):
            return vessel
    return {"vessel_class":"UNKNOWN","signature_profile":"UNKNOWN","propulsion_metadata":"UNKNOWN","operational_role":"UNKNOWN"}
