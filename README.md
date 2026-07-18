# Hermes TraceLab

Hermes TraceLab is currently a bounded lifecycle-observability experiment for the
pinned Hermes synchronous agent loop.

The Phase 0 spike rejected the original outcome-to-invocation binding-debugger
hypothesis for the audited Hermes surface: the runtime does not expose
independent executor-owned attempt, raw-outcome, normalized-result, and
binding-decision identities. The current release target is therefore downgraded
to observing and measuring Hermes tool lifecycle correlation, hook timing,
result transformation visibility, delivery association, trace completeness, and
instrumentation overhead.

The original binding-debugger and session-isolation ideas remain documented as
rejected/deferred hypotheses, not current implementation claims.

## Status

The repository is closing the architecture hypothesis and feasibility-spike
stage. The owner decision recorded in `spike/go-no-go.md` authorizes a
downgraded Phase 1A lifecycle-observability MVP only. The project must not claim
to be a binding debugger for the pinned Hermes path.

## Scope

- Hermes is the runtime base; this project does not use HelloAgents as its implementation base.
- Tool work is limited to lifecycle correlation in the pinned synchronous agent loop.
- Binding mismatch diagnosis is explicitly out of scope for the current release.
- Session diagnosis is deferred until a separate session authority/resource-ownership audit.
- Replay is not part of the current lifecycle-observability release.
- Recorder failures produce INCONCLUSIVE, not a Hermes violation.

## Repository map

- docs/: scope, assumptions, invariants, and replay contracts.
- spike/: feasibility-spike notes and acceptance evidence.
- src/tracelab/: implementation package; core modules are added only after the spike gate.
- tests/: fixtures, fidelity checks, family tests, and negative controls.
- evaluation/: case tables and measurement notes.
- reports/: reviewed example reports.

## Development

Create an environment and install development dependencies:

    python -m venv .venv
    . .venv/bin/activate
    python -m pip install -e '.[dev]'

Run the checks:

    pytest
    ruff check .

## Evidence vocabulary

The project distinguishes SUT_VIOLATION, RECORDER_FAILURE, INCOMPLETE_TRACE, INCONCLUSIVE, and CONTROL_PASS. No report may claim a repaired Hermes bug from a trace-only or mutation-only case.
