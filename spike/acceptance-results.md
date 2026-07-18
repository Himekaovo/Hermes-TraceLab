# Feasibility Spike: Acceptance Results

## Baseline

- Upstream: NousResearch/hermes-agent
- Commit: 444b5e96fa2829c29cfd7ecdc84d89f83a1441da
- Inspection date: 2026-07-14
- Python requirement: >=3.11,<3.14
- No Hermes source changes
- No TraceLab runtime instrumentation
- No SUT mutation fixture

## Tool Binding acceptance table

| Criterion | Result | Evidence judgment |
|---|---|---|
| TB-F1 Attempt Identity | NOT SATISFIED | No executor-owned attempt_id is created for every actual tool attempt. task_id, turn_id, and tool_call_id have different ownership and scope. |
| TB-F2 Origin Capture | NOT SATISFIED | No independent executor boundary emits attempt_id -> raw_outcome_id. Handler completion can be observed, but it does not establish the proposed origin identity. |
| TB-F3 Binding Capture | NOT SATISFIED | Hermes propagates tool_call_id and restores concurrent results by original call index; the inspected path has no later production binder selecting among candidate invocations. |
| TB-F4 Lineage Continuity | NOT SATISFIED | The required raw_outcome_id -> normalized_result_id -> binding_decision_id chain does not exist as independently observable Hermes facts. |
| TB-F5 Fault Discriminability | NOT RUN | SUT-level mutation and negative control were not created because the prerequisite evidence contract failed. |

## What is established

The pinned source supports observing a tool lifecycle:

model tool call
-> middleware/pre-hook
-> registry dispatch
-> handler completion
-> result normalization/transformation
-> post-hook
-> tool result message append

The source also supports correlation using session_id, task_id, turn_id, api_request_id, and tool_call_id, subject to their actual ownership and scope.

## What is not established

This spike does not establish:

- outcome-to-invocation binding mismatch diagnosis;
- executor retry attempt identity;
- independent producer lineage;
- independent binder decision lineage;
- complete session history provenance;
- graph or backward-slice correctness;
- replay-based repair evidence.

## Decision

The original Tool family claim is downgraded to lifecycle observability for the pinned Hermes path.

Stop conditions apply:

- do not implement graph, backward slice, replay, or Session family;
- do not create a permanent recorder or public identity schema;
- do not claim a Hermes bug has been diagnosed or fixed.

## Recorded next decision

The owner has selected:

- Lifecycle Observability MVP for the pinned Hermes synchronous path.

This decision is recorded in `spike/go-no-go.md`. A new audit target, such as
an asynchronous gateway, subagent route, or result-routing candidate-selection
surface, is deferred.

Phase 1A is conditional on the downgraded lifecycle-observability scope. It may
not implement graph, backward slice, binding detector, replay-based repair,
Session family, Skill Control, or Memory Control work.
