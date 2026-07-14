# Architecture Hypothesis v0.1

## Purpose

This document records the assumptions that the feasibility spike must test. It is not a final class design, public API, graph schema, or replay implementation plan.

## Supported claims

The first claim is limited to outcome-to-invocation binding mismatches under retries or repeated tool calls. The second claim is limited to foreign session history entering prompt assembly when an expected session ID is already known.

## Core trust boundary hypothesis

The tool family requires two independently produced observations:

- executor-boundary observation: each execution attempt produces a raw outcome;
- binding-boundary observation: Hermes records which invocation a normalized result is actually bound to.

A recorder must not manufacture both sides after the run and call the result lineage.

## Identity ownership hypotheses

| Identity | Owner | Creation point | Rule |
| --- | --- | --- | --- |
| invocation_id | harness dispatcher | logical call accepted | one logical invocation |
| attempt_id | retry controller or executor wrapper | before each actual execution | every retry gets a new ID |
| raw_outcome_id | executor wrapper | terminal outcome formed | never reused |
| normalized_result_id | normalization or assembly boundary | normalized result constructed | one result gets one ID |
| binding_decision_id | binder | binding choice made | one decision gets one ID |

Downstream components may reference upstream identities but may not overwrite them. The recorder records facts; it is not the authority that creates lifecycle identities after the fact.

## Tool lineage hypothesis

The minimum lineage must be observable as:

    ToolAttempt -> RawOutcome -> NormalizedToolResult -> BindingDecision

For the supported synchronous loop, the expected invariant is:

    invocation(producer_attempt(raw_outcome)) == binding_decision.selected_invocation

This invariant must be confirmed against Hermes source behavior before it is treated as a detector rule.

## Session lineage hypothesis

The entrypoint or fixture supplies expected_session_id. The loader observation must record the session ownership of the resources actually read. The session-history fragment is valid only when every source resource belongs to the expected session.

This is a structural scope check. It does not prove that contamination changed model behavior.

## Failure semantics hypothesis

The system must distinguish:

- SUT_VIOLATION: observed Hermes behavior violates a supported invariant;
- RECORDER_FAILURE: recorder failed to capture a required boundary or identity;
- INCOMPLETE_TRACE: run ended before required evidence was complete;
- INCONCLUSIVE: evidence is insufficient for a diagnosis;
- CONTROL_PASS: a legal complex control satisfies the invariant.

If recorder fidelity fails, the diagnosis must be INCONCLUSIVE.

## Feasibility acceptance criteria

- F1: every actual attempt has a unique, non-reused attempt_id;
- F2: executor boundary independently records attempt_id to raw_outcome_id;
- F3: binding boundary independently records normalized_result_id to selected_invocation_id;
- F4: raw outcome, normalized result, and binding decision form a continuous immutable lineage;
- F5: an injected binding-policy fault is detected while a structurally similar legal retry control remains clean.

## Downgrade rules

- F1 or F2 failure: downgrade to lifecycle observability; remove the binding-debugger claim.
- F3 failure: keep outcome provenance only; do not diagnose final binding targets.
- F4 failure: stop the tool binding family.
- F5 failure: stop before graph, slice, or replay work.

## Required next artifact

The next artifact is spike/execution-path.md, based on the real Hermes call path. No implementation module should be designed as if the conceptual normalizer or binder is present until that path is verified.
