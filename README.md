# Hermes TraceLab

Hermes TraceLab is a provenance-driven diagnostic foundation for auditable
agent evolution. The current release is deliberately narrow: it investigates
whether a real Hermes runtime exposes enough lifecycle identity, binding,
recorder-fidelity, and replay seams to build a trustworthy Tool Outcome Binding
Trace MVP.

## Current Scope

This branch restarts the repository from the project plan and does not reuse the
previous bootstrap content.

Current release target:

- Phase 0: Hermes Execution-Path Spike
- Phase 1: Tool Outcome Binding Trace MVP, only if Phase 0 returns GO

Current Phase 0 result:

- Hermes runtime is not bound in this repository yet.
- F1-F4 are marked `UNKNOWN`.
- The release gate is `NO_GO_MISSING_SUT`.
- Phase 1 must not start until a real Hermes runtime repository, commit, and
  entrypoint are provided.

## Repository Layout

```text
PROJECT_VISION.md        Long-term Trace / Skill / Memory vision
MVP_SPEC.md              Current release scope and acceptance criteria
docs/                    Stable contracts and boundaries
spike/                   Phase 0 investigation artifacts
src/tracelab/            Minimal Phase 0 decision helpers
tests/                   Unit tests for release-gate logic
```

## Verify

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'
```

## Gate Rule

Do not proceed to the next phase until the user has reviewed the current phase
artifacts and explicitly approved continuing.
