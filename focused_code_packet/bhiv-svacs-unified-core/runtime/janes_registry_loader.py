import json
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_REGISTRY_PATH = _PROJECT_ROOT / "maritime_knowledge" / "janes_runtime_registry.json"

with _REGISTRY_PATH.open("r", encoding="utf-8") as f:
    REGISTRY = json.load(f)


def get_vessel_metadata(mmsi):
    for vessel in REGISTRY:
        if "mmsi" in vessel and str(vessel["mmsi"]) == str(mmsi):
            return vessel

    return {
        "vessel_class": "UNKNOWN",
        "signature_profile": "UNKNOWN",
        "propulsion_metadata": "UNKNOWN",
        "operational_role": "UNKNOWN"
    }
