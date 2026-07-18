# Architecture Hypothesis v0.1

## Purpose

This document records the assumptions that the feasibility spike must test. It is not a final class design, public API, graph schema, or replay implementation plan.

## Supported claims

The first claim is limited to outcome-to-invocation binding mismatches under retries or repeated tool calls. The second claim is limited to foreign session history entering prompt assembly when an expected session ID is already known.

## Core trust boundary hypothesis

The tool family requires two independently produced observations:

- executor-boundary observation: each execution attempt produces a raw outcome;
- binding-boundary observation: Hermes records which invocation a normalized result is actually bound to.

Separate code locations are insufficient. The executor observation and binding observation must derive their authoritative identities from different lifecycle owners. Neither side may reconstruct its identity from metadata emitted by the other side.

The executor observation must come from attempt-local execution ownership. The binding observation must come from the invocation actually selected by the production binding or assembly path. Neither side may simply copy the same invocation_id field from shared metadata. A recorder must not manufacture both sides after the run and call the result lineage.

## Identity ownership hypotheses

| Identity | Owner | Creation point | Rule |
| --- | --- | --- | --- |
| invocation_id | harness dispatcher | logical call accepted | one logical invocation |
| attempt_id | retry controller or executor wrapper | before each actual execution | every retry gets a new ID |
| raw_outcome_id | executor wrapper | terminal outcome formed | never reused |
| normalized_result_id | normalization or assembly boundary | normalized result constructed | one result gets one ID |
| binding_decision_id | binder | binding choice made | one decision gets one ID |

The raw-outcome identity must be created at the executor boundary. Downstream normalization and binding stages may reference it but must not replace or regenerate it. Downstream components may reference upstream identities but may not overwrite them. The recorder records facts; it is not the authority that creates lifecycle identities after the fact.

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

## Tool Binding feasibility acceptance criteria

These criteria are named `TB-F*` because they apply only to the original Tool
Binding Debugger hypothesis.

- TB-F1: every actual attempt has a unique, non-reused attempt_id;
- TB-F2: the executor observation obtains attempt ownership from the actual attempt-local execution context and does not read a binding-selected invocation identity;
- TB-F3: the binding observation records the invocation actually selected by the production binding or assembly path, rather than inferring it from result position or expected fixture metadata;
- TB-F4: a raw-outcome identity created at the executor boundary survives normalization into the binding decision without downstream regeneration or overwrite;
- TB-F5: an injected binding-policy fault is detected while a structurally similar legal retry control remains clean.

## Lifecycle Observability acceptance criteria

If the Tool Binding criteria fail for a pinned Hermes surface, the project may
only proceed under a downgraded lifecycle-observability scope. These criteria
are named `LO-F*` to avoid confusion with `TB-F*`.

- LO-F1: supported lifecycle observations preserve Hermes-owned correlation keys without recorder regeneration;
- LO-F2: dispatch, handler-completion, post-hook, transformation, and final-delivery observations are present for supported fixture runs;
- LO-F3: dropped, duplicated, malformed, or impossible recorder events produce RECORDER_FAILURE or INCONCLUSIVE, never SUT_VIOLATION;
- LO-F4: when transform_tool_result changes a result, TraceLab distinguishes post-hook-visible content from final-delivered content;
- LO-F5: instrumentation does not materially alter call order, result order, or terminal status within the declared fixture boundary;
- LO-F6: sequential repeated calls, concurrent completion reordering, handler failure, and transformation controls preserve correct tool_call_id correlation.

## Downgrade rules

- TB-F1 or TB-F2 failure: downgrade to lifecycle observability; remove the binding-debugger claim.
- TB-F3 failure: keep outcome provenance only; do not diagnose final binding targets.
- TB-F4 failure: stop the tool binding family.
- TB-F5 failure: stop before graph, slice, or replay work.

## Required next artifact

The next artifact is spike/execution-path.md, based on the real Hermes call path. No implementation module should be designed as if the conceptual normalizer or binder is present until that path is verified.
