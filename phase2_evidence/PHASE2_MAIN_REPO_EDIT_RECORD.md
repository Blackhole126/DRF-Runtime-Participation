# Phase 2 Main-Repository Edit Record

## Purpose
This record identifies the upstream implementation repositories and the exact Phase 2 changes represented in the submission evidence. The DRF submission package is not claiming write access to those repositories.

## `bhiv-svacs-unified-core`
Commit:
`30a305506b26677190a7d4bd8271543edcd91ad6`

Changes:
- Structured runtime observability and metrics.
- Safe HTTP error boundary and telemetry error sanitization.
- Runtime participation/discovery status surface.
- Existing pipeline-stage adapter restoration required for the live chain.
- Deterministic registry/storage path hardening.
- Unit/integration/E2E verification support.
- Existing `POST /modules` / `GET /modules` Capability Registry contract preserved.

## `bhiv-Capability-Registry-Foundation`
Commit:
`6980ce5721385639e864eb6e082c836f83c625cb`

Changes:
- Required registration-field validation.
- Optional API-key access boundary for mutating operations.
- Request-ID/response timing traceability.
- Safe unexpected-exception boundary.
- Health/status exposure of contract/auth configuration.
- Phase 2 security and E2E verification.

## Access limitation
These upstream repositories are not writable from the current submission workflow. The commits are therefore recorded as implementation references/evidence, not as a claim that Mohit's DRF submission pushed them.

## Contract safety
No parallel registry, new authority, or undocumented runtime contract was introduced.
