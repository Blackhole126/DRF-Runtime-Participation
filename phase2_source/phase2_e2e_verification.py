"""Deterministic E2E verification of the existing SVACS runtime chain."""
import json, hashlib, os, sys
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); sys.path.insert(0, ROOT)
from orchestration.live_pipeline import run_pipeline

def canonical_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()

def run():
    first=run_pipeline(risk_level="LOW")
    second=run_pipeline(risk_level="HIGH")
    checks={
      "approved_flow_completed": first.get("rajya_verdict",{}).get("status") == "APPROVED",
      "rejected_flow_blocked": second.get("rajya_verdict",{}).get("status") == "REJECTED",
      "execution_id_present": bool(first.get("execution_id")) and bool(second.get("execution_id")),
      "trace_id_present": bool(first.get("trace_id")) and bool(second.get("trace_id")),
      "contract_version_present": bool(first.get("contract_version")),
    }
    report={"phase":"2","verification":"E2E","checks":checks,"passed":all(checks.values()),
            "approved_execution_id":first.get("execution_id"),"approved_trace_id":first.get("trace_id"),
            "rejected_execution_id":second.get("execution_id"),"rejected_trace_id":second.get("trace_id")}
    report["evidence_digest"]=canonical_digest(report)
    os.makedirs(os.path.join(ROOT,"reports","phase2"),exist_ok=True)
    with open(os.path.join(ROOT,"reports","phase2","E2E_VERIFICATION.json"),"w") as f: json.dump(report,f,indent=2)
    print(json.dumps(report,indent=2)); return 0 if report["passed"] else 1
if __name__ == "__main__": raise SystemExit(run())
