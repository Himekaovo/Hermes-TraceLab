# Feasibility Spike: Instrumentation Notes

## Scope discipline

This spike intentionally adds no long-term recorder, public identity schema, detector, replay engine, graph model, session family, or source change to Hermes.

The purpose is to decide whether those components would have a valid evidence boundary. The source audit found a lifecycle seam but not the independent producer/binder pair required by the original claim.

## Candidate observation points

If the owner approves the downgraded lifecycle-observability scope, a bounded experiment may observe:

1. turn context creation
   - session_id
   - task_id
   - turn_id
   - api_request_id when assigned

2. tool dispatch entry
   - tool name
   - tool_call_id
   - session_id
   - task_id
   - turn_id

3. handler completion
   - tool_call_id
   - terminal status
   - duration
   - redacted result metadata or digest

4. post_tool_call
   - the result visible to the post hook
   - hook status and timing

5. final tool-message delivery
   - tool_call_id
   - message append order
   - transformed result metadata or digest

These points can establish a lifecycle trace. They cannot, by themselves, establish executor-owned attempts or a later binder decision.

## Evidence boundaries

The following facts must remain distinct:

- tool_call_id is a provider/model correlation key;
- handler completion is an execution-lifecycle observation;
- post_tool_call is a hook observation;
- transform_tool_result may alter the delivered result;
- message append is a delivery observation;
- registry dispatch is not a binding decision among multiple candidates.

A future recorder must not synthesize attempt_id, raw_outcome_id, normalized_result_id, or binding_decision_id after the fact and present them as Hermes-owned facts.

## Minimal future lifecycle experiment

Only after owner approval:

- use a deterministic local tool fixture;
- run sequential and concurrent tool calls;
- include handler success, handler error, timeout/cancellation if the path supports it;
- record the same correlation keys at each approved observation point;
- compare post-hook and final-delivery observations when result transformation is active;
- measure whether observation changes timing or ordering.

The fixture may provide an external expected lifecycle sequence for evaluation, but the detector must not read fixture ground truth as an input.

## Explicitly forbidden at this stage

- editing trace JSON to manufacture provenance;
- adding expected invocation IDs to detector input;
- calling tool_call_id an executor attempt identity;
- inventing a binder object because the conceptual architecture names one;
- claiming that concurrent result reordering proves binding;
- implementing a permanent recorder before scope approval;
- implementing backward slicing or replay under the rejected binding claim;
- adding Session family support without independent session authority and resource ownership.

## Recorded owner decision

The scope selection is recorded in `spike/go-no-go.md`:

- proceed with lifecycle observability for the pinned Hermes path;
- defer any new source audit of a different Hermes routing surface with a genuine
  candidate-selection boundary.

No production instrumentation should be merged outside the Phase 1A lifecycle
observability scope.
