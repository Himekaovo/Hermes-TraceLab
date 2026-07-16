# Hermes TraceLab MVP Specification

## Current Build Target

The current release only covers:

```text
Phase 0: Hermes Execution-Path Spike
Phase 1: Tool Outcome Binding Trace MVP
```

Phase 1 is gated by Phase 0. It must not start unless Phase 0 produces an
explicit GO or user-approved CONDITIONAL GO.

## Current Non-Goals

This release does not implement:

- Session Isolation detector family.
- Failure Attribution Control Plane.
- Agent-as-a-Judge.
- GEPA or DSPy skill evolution.
- Automatic `SKILL.md` edits.
- Skill shadow/canary deployment.
- Memory Graph.
- Graphiti, HippoRAG, or Neo4j integration.
- Learned memory reranking.
- Full agent replay.
- Automatic source repair.

## Phase 0 Questions

Phase 0 answers only F1-F4.

### F1: Lifecycle Identity Observability

Can the real Hermes production path expose stable invocation, attempt, and raw
outcome identities without the recorder inventing them?

### F2: Independent Binding Seam

Is there a real production decision point where the raw outcome producer and
selected target invocation can be independently observed?

### F3: Recorder Fidelity Verifiability

Can the recorder prove it did not manufacture, omit, or mutate key evidence?

### F4: Real Component Replayability

Can captured production input be replayed through the real Hermes component,
rather than replaying a modified trace file?

## Phase 0 Required Artifacts

```text
spike/execution-path.md
spike/identity-ownership.md
spike/instrumentation-seams.md
spike/f1-f4-results.md
spike/go-no-go.md
```

## Release Gate

```text
GO:
  F1 = SUPPORTED
  F2 = SUPPORTED
  F3 = SUPPORTED
  F4 = SUPPORTED or PARTIALLY_SUPPORTED

CONDITIONAL GO:
  F1 = SUPPORTED
  F2 = PARTIALLY_SUPPORTED
  F3 = SUPPORTED
  F4 = PARTIALLY_SUPPORTED

NO-GO:
  Missing SUT, rejected binding seam, rejected recorder fidelity,
  rejected replay, or insufficient evidence.
```

## Current Phase 0 Result

No real Hermes runtime repository, commit, or entrypoint is currently bound to
this TraceLab repository. The Phase 0 decision is therefore
`NO_GO_MISSING_SUT`.

This is an intentional conservative result, not a project failure. It prevents
TraceLab from fabricating lifecycle identity, binding seams, or replay claims.
