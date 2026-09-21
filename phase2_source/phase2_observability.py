"""Phase 2 runtime observability, metrics and safe error-boundary helpers."""
import json, os, re, time, uuid
from datetime import datetime, timezone
from threading import Lock

TELEMETRY_DIR = os.getenv("SVACS_TELEMETRY_DIR", "storage/telemetry")
EVENT_FILE = os.path.join(TELEMETRY_DIR, "phase2_events.jsonl")
METRICS_FILE = os.path.join(TELEMETRY_DIR, "phase2_metrics.json")
_lock = Lock()
_metrics = {"requests_total": 0, "requests_failed": 0, "runtime_executions": 0, "runtime_failures": 0, "contract_rejections": 0}
_SECRET_RE = re.compile(r"(?i)(token|password|secret|api[_-]?key|authorization)=[^&\s]+")

def utc_now(): return datetime.now(timezone.utc).isoformat()
def sanitize_error(value): return _SECRET_RE.sub(r"\1=[REDACTED]", str(value))[:500]

def emit_event(event, *, execution_id=None, trace_id=None, status="INFO", error=None):
    os.makedirs(TELEMETRY_DIR, exist_ok=True)
    payload = {"event_id": str(uuid.uuid4()), "timestamp": utc_now(), "event": event, "status": status,
               "execution_id": execution_id, "trace_id": trace_id}
    if error is not None: payload["error"] = sanitize_error(error)
    with _lock:
        with open(EVENT_FILE, "a", encoding="utf-8") as f: f.write(json.dumps(payload, sort_keys=True) + "\n")
    return payload

def increment(metric, amount=1):
    with _lock:
        _metrics[metric] = _metrics.get(metric, 0) + amount
        os.makedirs(TELEMETRY_DIR, exist_ok=True)
        with open(METRICS_FILE, "w", encoding="utf-8") as f: json.dump(_metrics, f, indent=2, sort_keys=True)

def metrics_snapshot(): return dict(_metrics)

def record_request(): increment("requests_total")
def record_request_failure(): increment("requests_failed")
def record_execution(): increment("runtime_executions")
def record_execution_failure(): increment("runtime_failures")
def record_contract_rejection(): increment("contract_rejections")

def safe_runtime_error(exc, *, execution_id=None, trace_id=None):
    record_execution_failure()
    return emit_event("runtime_error_boundary", execution_id=execution_id, trace_id=trace_id, status="FAILED", error=exc)
