#!/usr/bin/env python3
"""Deterministic Phase 2 submission metadata/evidence validator."""
import hashlib, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]

REQUIRED = [
    "PHASE2_SUBMISSION_README.md",
    "PHASE2_FINAL_CERTIFICATION.md",
    "phase2_evidence/PHASE2_DELIVERABLE_REPORT.md",
    "phase2_evidence/PHASE2_PRODUCTION_READINESS.md",
    "phase2_evidence/PHASE2_COMMIT_RECORD.md",
    "phase2_evidence/E2E_VERIFICATION.json",
    "phase2_evidence/REGISTRY_E2E.json",
    "phase2_evidence/REGISTRY_RUNTIME_E2E.json",
    "phase2_source/phase2_observability.py",
    "phase2_source/test_phase2_hardening.py",
    "phase2_source/phase2_e2e_verification.py",
    "phase2_source/phase2_registry_runtime_e2e.py",
]
checks = {p: (ROOT / p).is_file() for p in REQUIRED}

json_evidence = {}
for rel in ["phase2_evidence/E2E_VERIFICATION.json",
            "phase2_evidence/REGISTRY_E2E.json",
            "phase2_evidence/REGISTRY_RUNTIME_E2E.json"]:
    try:
        json_evidence[rel] = json.loads((ROOT/rel).read_text(encoding="utf-8"))
        checks[rel + ":json_valid"] = True
    except Exception:
        checks[rel + ":json_valid"] = False

checks["e2e_passed"] = json_evidence.get("phase2_evidence/E2E_VERIFICATION.json", {}).get("passed") is True
checks["registry_e2e_passed"] = json_evidence.get("phase2_evidence/REGISTRY_E2E.json", {}).get("passed") is True
checks["runtime_registry_e2e_passed"] = json_evidence.get("phase2_evidence/REGISTRY_RUNTIME_E2E.json", {}).get("passed") is True

# Scan committed submission text for obvious credential assignments.
credential_re = re.compile(r'(?i)(api[_-]?key|password|secret|bearer)\s*[:=]\s*["\']?[A-Za-z0-9_\-]{12,}')
checks["no_credential_like_values"] = not any(
    credential_re.search(p.read_text(encoding="utf-8", errors="ignore"))
    for p in ROOT.rglob("*") if p.is_file() and p.suffix in {".md",".json",".py",".txt"}
)

metadata = {
    "phase": "2",
    "artifact": "DRF Runtime Participation Proof",
    "required_files": REQUIRED,
    "checks": checks,
    "passed": all(checks.values()),
    "upstream_commits": {
        "svacs_runtime": "30a305506b26677190a7d4bd8271543edcd91ad6",
        "capability_registry": "6980ce5721385639e864eb6e082c836f83c625cb",
    },
}
metadata["content_digest"] = hashlib.sha256(
    json.dumps(metadata, sort_keys=True).encode()
).hexdigest()

out = ROOT / "phase2_evidence" / "PHASE2_METADATA_VALIDATION.json"
out.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
print(json.dumps(metadata, indent=2))
raise SystemExit(0 if metadata["passed"] else 1)
