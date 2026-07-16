# Phase 0 Instrumentation Seams

## Candidate Seams

| Seam | Needed fields | Mutation risk | Recorder risk | Replay feasibility | Status |
| --- | --- | --- | --- | --- | --- |
| Tool-call parse | invocation candidate, parsed tool name, arguments | Medium | Medium | Unknown | UNKNOWN |
| Invocation creation | `invocation_id`, parent run/session | Low if read-only | Medium | Unknown | UNKNOWN |
| Attempt creation | `attempt_id`, `invocation_id`, retry index if present | Low if read-only | Medium | Unknown | UNKNOWN |
| Executor completion | `attempt_id`, raw result/error, `raw_outcome_id` | Medium | High | Unknown | UNKNOWN |
| Normalization | `raw_outcome_id`, `normalized_result_id` | Medium | Medium | Unknown | UNKNOWN |
| Binding decision | producer outcome, selected target invocation | High | High | Unknown | UNKNOWN |
| Prompt/history assembly | selected result, target invocation/session | Medium | Medium | Unknown | UNKNOWN |

## Current Finding

No seam can be marked `SUPPORTED` until a real Hermes runtime is bound and
inspected. In particular, TraceLab must not create a synthetic
`BindingDecision` if Hermes has no independent binding seam.

## Required Evidence For Each Seam

```text
Location:
Owner:
Observed fields:
Mutation risk:
Recorder risk:
Replay feasibility:
Status: SUPPORTED | PARTIALLY_SUPPORTED | REJECTED | UNKNOWN
```
