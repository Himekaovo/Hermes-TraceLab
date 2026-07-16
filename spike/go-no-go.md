# Phase 0 Go/No-Go

## Decision

```text
NO_GO_MISSING_SUT
```

## Decision Matrix

```text
F1 = UNKNOWN
F2 = UNKNOWN
F3 = UNKNOWN
F4 = UNKNOWN
```

The current repository can host TraceLab, but it does not yet bind the real
Hermes runtime required for Phase 0.

## What This Allows

- Keep the TraceLab project documentation.
- Keep minimal Phase 0 release-gate helpers and tests.
- Bind a real Hermes runtime in the next user-approved step.
- Re-run Phase 0 once the runtime repository, commit, and entrypoint are known.

## What This Blocks

- Do not start Phase 1 Tool Outcome Binding Trace MVP.
- Do not implement a producer-target mismatch detector.
- Do not claim component replay.
- Do not fabricate `BindingDecision`.
- Do not use fixture truth as detector input.

## Required User Review

The next stage may begin only after the user confirms the SUT binding details:

```text
Hermes repository URL or local path:
Hermes commit SHA:
Runtime entrypoint:
Command to run a minimal tool-calling session:
```

Until then, the correct project state is a conservative Phase 0 stop.
