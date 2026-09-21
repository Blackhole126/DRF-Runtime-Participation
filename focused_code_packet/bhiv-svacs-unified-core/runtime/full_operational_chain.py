import json
from pathlib import Path
from runtime.ais_runtime_ingestor import ingest_ais_data
from runtime.janes_registry_loader import get_vessel_metadata

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_LOG_DIR = _PROJECT_ROOT / "logs"


def process_runtime_chain():
    events = ingest_ais_data()
    runtime_logs = []

    for event in events:
        metadata = get_vessel_metadata(event["mmsi"])

        geo_stage = {
            "trace_id": event["trace_id"],
            "stage": "geo",
            "status": "completed"
        }

        intelligence_stage = {
            "trace_id": event["trace_id"],
            "stage": "intelligence",
            "alert": "HIGH_SPEED"
            if event["speed"] > 40
            else "NORMAL"
        }

        state_stage = {
            "trace_id": event["trace_id"],
            "stage": "state",
            "state": "ACTIVE"
        }

        final_event = {
            "trace_id": event["trace_id"],
            "runtime_event": event,
            "metadata": metadata,
            "geo": geo_stage,
            "intelligence": intelligence_stage,
            "state": state_stage
        }
        runtime_logs.append(final_event)

    _LOG_DIR.mkdir(parents=True, exist_ok=True)
    with (_LOG_DIR / "full_operational_chain_log.json").open("w", encoding="utf-8") as f:
        json.dump(runtime_logs, f, indent=2)

    return runtime_logs
