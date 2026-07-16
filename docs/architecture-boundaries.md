# Architecture Boundaries

Hermes TraceLab separates diagnosis from repair and memory governance.

## Current Release Boundary

The current release may create only a diagnostic foundation:

- observe real execution lifecycle identities;
- validate recorder fidelity;
- detect tool outcome binding violations only when evidence is sufficient;
- produce minimal evidence slices;
- attempt captured-input component replay only against real production code.

## Out of Boundary

The current release must not:

- modify Hermes behavior;
- change skills automatically;
- decide memory writes or retrieval policy;
- let a model judge override deterministic evidence;
- infer missing production identities from trace order, list position, or log
  line number;
- call trace mutation a component replay.

## Dependency Direction

```text
Hermes Runtime
-> TraceLab Recorder
-> Fidelity Validator
-> Detector
-> Evidence Slice
-> Replay
-> Report
```

Skill and Memory systems may consume TraceLab evidence later, but TraceLab must
not depend on those future systems.
