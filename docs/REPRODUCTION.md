# Reproduction Instructions

## Prerequisites

- Python environment with the supplied repositories' dependencies installed.
- FastAPI, Uvicorn, Requests, SQLAlchemy, Pandas and Pytest available.

## 1. Apply the focused SVACS changes

Copy the contents of:

`focused_code_packet/bhiv-svacs-unified-core/`

into the matching paths of the supplied `bhiv-svacs-unified-core` repository.

Alternatively apply:

`patches/runtime-participation-proof.patch`

## 2. Start the Capability Registry Foundation

From the registry repository:

```powershell
cd bhiv-Capability-Registry-Foundation
uvicorn app.main:app --host 127.0.0.1 --port 8001
```

Check:

```powershell
Invoke-RestMethod http://127.0.0.1:8001/health
```

## 3. Start the SVACS runtime

In a second terminal:

```powershell
cd bhiv-svacs-unified-core
$env:CAPABILITY_REGISTRY_URL="http://127.0.0.1:8001"
uvicorn main:app --host 127.0.0.1 --port 8000
```

The startup hook submits the runtime through the existing registry `/modules` contract.

## 4. Validate

```powershell
Invoke-RestMethod http://127.0.0.1:8000/
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/api/participation
Invoke-RestMethod http://127.0.0.1:8000/api/participation/discovery
Invoke-RestMethod http://127.0.0.1:8000/api/participation/provenance
Invoke-RestMethod http://127.0.0.1:8001/modules
```

Run the focused tests:

```powershell
python -m pytest tests/test_runtime_participation.py -q
```

## Expected behavior

- First registration against a clean registry: `REGISTERED` with underlying registry response `200`.
- Repeated registration: `DUPLICATE_ALREADY_REGISTERED` with underlying registry response `409`.
- Invalid version such as `1.0`: registry rejects with `400`.
- Unavailable registry: adapter reports `REGISTRY_UNAVAILABLE`.
- Health: runtime reports `healthy`.
- Discovery: `SVACS Unified Core runtime` appears in registry output.
