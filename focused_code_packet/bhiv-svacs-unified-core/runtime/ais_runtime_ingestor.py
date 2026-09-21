import pandas as pd
import uuid
import json
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_DATA_PATH = _PROJECT_ROOT / "data" / "ais_runtime_data.csv"
_LOG_DIR = _PROJECT_ROOT / "logs"


def ingest_ais_data():
    print("STEP 1: Reading CSV...")
    df = pd.read_csv(_DATA_PATH)
    print("CSV LOADED SUCCESSFULLY")
    print(df.columns)

    runtime_events = []
    for _, row in df.head(5).iterrows():
        print("Processing Row...")
        event = {
            "trace_id": str(uuid.uuid4()),
            "mmsi": str(row["MMSI"]),
            "timestamp": str(row["BaseDateTime"]),
            "lat": float(row["LAT"]),
            "lon": float(row["LON"]),
            "speed": float(row["SOG"]),
            "vessel_type": str(row["VesselType"])
        }
        runtime_events.append(event)

    print("Creating Logs Folder Output...")
    _LOG_DIR.mkdir(parents=True, exist_ok=True)
    with (_LOG_DIR / "ais_runtime_trace.json").open("w", encoding="utf-8") as f:
        json.dump(runtime_events, f, indent=2)

    print("INGESTION SUCCESS")
    return runtime_events
