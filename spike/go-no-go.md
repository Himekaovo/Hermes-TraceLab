# Phase 0 Go/No-Go Decision

## Decision date

2026-07-18

## Audited target

- Repository: `NousResearch/hermes-agent`
- Commit: `444b5e96fa2829c29cfd7ecdc84d89f83a1441da`
- Surface: pinned synchronous Hermes agent-loop tool path
- TraceLab branch: `feat/bootstrap-skeleton`

## Verdict

```text
Original Phase 1 Tool Binding Debugger: NO-GO
Downgraded Phase 1A Lifecycle Observability: CONDITIONAL GO
```

## Reason

The pinned Hermes surface supports lifecycle correlation through Hermes-owned
keys such as `session_id`, `task_id`, `turn_id`, `api_request_id`, and
`tool_call_id`, but it does not expose the independent evidence contract needed
by the original binding-debugger claim.

The audited source does not establish:

- executor-owned `attempt_id` for each actual tool execution attempt;
- executor-created `raw_outcome_id` at terminal outcome formation;
- independently observable `normalized_result_id`;
- production `binding_decision_id` representing a later candidate-selection
  decision;
- `raw_outcome_id -> normalized_result_id -> binding_decision_id` lineage.

Therefore the original invariant is not supported on this surface:

```text
producer_invocation(raw_outcome)
==
binding_decision.selected_invocation
```

## TB gate results

| Gate | Result |
|---|---|
| TB-F1 Attempt Identity | NOT SATISFIED |
| TB-F2 Origin Capture | NOT SATISFIED |
| TB-F3 Binding Capture | NOT SATISFIED |
| TB-F4 Lineage Continuity | NOT SATISFIED |
| TB-F5 Fault Discriminability | NOT RUN |

## Selected next path

Proceed only with **Phase 1A Lifecycle Observability** for the pinned Hermes path.

Authorized Phase 1A scope:

- turn and tool-call lifecycle correlation;
- `session_id`, `task_id`, `turn_id`, `api_request_id`, and `tool_call_id`
  propagation;
- middleware, pre-hook, dispatch, handler completion, post-hook,
  transformation, and final-delivery observations;
- post-hook-visible result versus final-delivered result comparison;
- sequential and concurrent lifecycle controls;
- recorder completeness and malformed-event handling;
- instrumentation overhead and non-interference measurement.

## Deferred alternative

A new audit may be opened later for another Hermes surface, such as an
asynchronous gateway, subagent route, or result-routing layer. That audit must
repeat the evidence check before reviving any binding-debugger claim.

## Explicitly unauthorized for Phase 1A

- outcome-to-invocation binding mismatch diagnosis;
- executor attempt provenance claims;
- independent raw-outcome provenance claims;
- public `BindingDecision` identity schema;
- SUT binding violation reports;
- backward slicing;
- captured-input repair replay;
- Session family detector;
- Skill Control work;
- Memory Control work;
- any implementation that relies on trace JSON mutation to simulate provenance.

## Required Phase 1A gates

| Gate | Requirement |
|---|---|
| LO-F1 Correlation Key Observability | Supported lifecycle observations preserve Hermes-owned correlation keys without recorder regeneration. |
| LO-F2 Lifecycle Boundary Observability | Required dispatch, handler-completion, post-hook, transformation, and final-delivery observations are present for supported fixture runs. |
| LO-F3 Recorder Fidelity | Dropped, duplicated, malformed, or impossible recorder events produce `RECORDER_FAILURE` or `INCONCLUSIVE`, never `SUT_VIOLATION`. |
| LO-F4 Final-Delivery Visibility | When `transform_tool_result` changes a result, TraceLab distinguishes post-hook-visible content from final-delivered content. |
| LO-F5 Non-Interference | Instrumentation does not materially alter call order, result order, or terminal status within the declared fixture boundary. |
| LO-F6 Complex Controls | Sequential repeated calls, concurrent completion reordering, handler failure, and transformation controls preserve correct `tool_call_id` correlation. |

## Phase 0 closure

Phase 0 is closed as a successful feasibility investigation with a negative
binding-debugger result. Phase 1A may start only under the downgraded lifecycle
observability scope above.
