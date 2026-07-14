# Hermes TraceLab

Hermes TraceLab is designed as a focused provenance and captured-input replay debugger for two classes of Hermes harness failures:

1. Outcome-to-invocation binding mismatches under retries or repeated tool calls.
2. Foreign session history entering prompt assembly when the expected session ID is already known.

The planned MVP separates executor-boundary observations from binding decisions, validates recorder fidelity, produces family-specific slices, and re-executes bounded components under captured inputs.

## Status

The repository is in the architecture hypothesis and feasibility-spike stage. The first implementation gate is to prove that Hermes exposes independent producer-lineage and binding-decision evidence. Until that gate passes, the project must not claim to be a binding debugger.

## Scope

- Hermes is the runtime base; this project does not use HelloAgents as its implementation base.
- Tool diagnosis is limited to synchronous agent-loop cases in the supported fixture boundary.
- Session diagnosis is structural and limited to session-history resource lineage.
- Replay means captured-input component replay, not deterministic whole-agent replay.
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
