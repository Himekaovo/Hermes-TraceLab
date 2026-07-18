# Feasibility Spike: Hermes Execution Path

## Investigation metadata

- Upstream repository: NousResearch/hermes-agent
- Inspected ref: main at commit 444b5e96fa2829c29cfd7ecdc84d89f83a1441da
- Release/tag: not pinned; this spike targets the commit above
- Inspection date: 2026-07-14
- Expected Python: >=3.11,<3.14, from the upstream pyproject.toml
- TraceLab branch: feat/bootstrap-skeleton
- Hermes source modifications: none
- TraceLab runtime instrumentation added: none
- SUT mutation fixture added: none

## Question

Can the pinned Hermes source expose independent producer lineage and a later binding decision for a tool result?

The answer must be based on the actual execution path. A conceptual normalizer or binder is not sufficient evidence.

## Verified execution path

Hermes documents the turn as:

1. build the prompt;
2. call the model;
3. parse the response;
4. execute returned tool calls;
5. append tool results;
6. continue the loop.

Relevant upstream documentation:

- Agent loop: https://github.com/NousResearch/hermes-agent/blob/444b5e96fa2829c29cfd7ecdc84d89f83a1441da/website/docs/developer-guide/agent-loop.md
- Tool runtime: https://github.com/NousResearch/hermes-agent/blob/444b5e96fa2829c29cfd7ecdc84d89f83a1441da/website/docs/developer-guide/tool-runtime.md

The observed call chain is:

model tool call
-> conversation_loop.run_conversation
-> run_agent._execute_tool_calls
-> run_agent._invoke_tool
-> agent_runtime_helpers.invoke_tool
-> model_tools.handle_function_call
-> registry.dispatch
-> handler
-> result normalization
-> post_tool_call observation
-> make_tool_result_message
-> append to conversation messages

The exact source responsibilities are:

- conversation_loop.py: selects tool execution after an assistant message contains tool calls.
- tool_executor.py: executes sequential or concurrent calls and appends results.
- agent_runtime_helpers.py: applies request and execution middleware.
- model_tools.py: forwards tool_call_id through middleware, approval, dispatch, post-hook, and result transformation.
- tools/registry.py: invokes the handler, normalizes its return, and catches handler exceptions.

## Pinned source evidence

All source links below target commit
`444b5e96fa2829c29cfd7ecdc84d89f83a1441da`.

### Concurrent delivery association

Claim: concurrent tool results are restored to the original model tool-call
order by list index, not by a later binder selecting among candidate
invocations.

- Evidence:
  [`agent/tool_executor.py#L325-L329`](https://github.com/NousResearch/hermes-agent/blob/444b5e96fa2829c29cfd7ecdc84d89f83a1441da/agent/tool_executor.py#L325-L329)
  states that concurrent results are collected in original tool-call order.
- Evidence:
  [`agent/tool_executor.py#L567-L608`](https://github.com/NousResearch/hermes-agent/blob/444b5e96fa2829c29cfd7ecdc84d89f83a1441da/agent/tool_executor.py#L567-L608)
  passes the original `tool_call.id` into `_invoke_tool`.
- Evidence:
  [`agent/tool_executor.py#L680-L715`](https://github.com/NousResearch/hermes-agent/blob/444b5e96fa2829c29cfd7ecdc84d89f83a1441da/agent/tool_executor.py#L680-L715)
  maps each submitted future back to the original parsed-call index.
- Evidence:
  [`agent/tool_executor.py#L972-L978`](https://github.com/NousResearch/hermes-agent/blob/444b5e96fa2829c29cfd7ecdc84d89f83a1441da/agent/tool_executor.py#L972-L978)
  constructs and appends the tool result message with `tc.id`.

Implication: delivery association survives completion-order changes.

Does not prove: a later production binder chooses among multiple candidate
invocation identities.

### Sequential propagation

Claim: the sequential path propagates the model-owned `tool_call.id` from the
parsed call into execution and final tool-result message construction.

- Evidence:
  [`agent/tool_executor.py#L1022-L1060`](https://github.com/NousResearch/hermes-agent/blob/444b5e96fa2829c29cfd7ecdc84d89f83a1441da/agent/tool_executor.py#L1022-L1060)
  iterates the assistant message's tool calls and uses `tool_call.id` when
  building immediate malformed-argument results.
- Evidence:
  [`agent/tool_executor.py#L1475-L1487`](https://github.com/NousResearch/hermes-agent/blob/444b5e96fa2829c29cfd7ecdc84d89f83a1441da/agent/tool_executor.py#L1475-L1487)
  passes `tool_call.id` into `handle_function_call`.
- Evidence:
  [`agent/tool_executor.py#L1653-L1657`](https://github.com/NousResearch/hermes-agent/blob/444b5e96fa2829c29cfd7ecdc84d89f83a1441da/agent/tool_executor.py#L1653-L1657)
  creates the final tool message with `tool_call.id` and appends it.

Implication: the inspected synchronous path has strong lifecycle correlation
via the provider/model-owned call ID.

Does not prove: executor-owned attempts, raw outcomes, or independent binding
decisions.

### Handler dispatch and normalization

Claim: handler execution and result normalization occur inside registry dispatch
and return a normalized value upward; dispatch does not create a separate
raw-outcome identity.

- Evidence:
  [`tools/registry.py#L584-L612`](https://github.com/NousResearch/hermes-agent/blob/444b5e96fa2829c29cfd7ecdc84d89f83a1441da/tools/registry.py#L584-L612)
  normalizes handler results into supported string or multimodal shapes.
- Evidence:
  [`tools/registry.py#L614-L644`](https://github.com/NousResearch/hermes-agent/blob/444b5e96fa2829c29cfd7ecdc84d89f83a1441da/tools/registry.py#L614-L644)
  invokes the handler, normalizes the result, and catches handler exceptions.

Implication: registry dispatch is a useful lifecycle boundary for handler
completion and normalized result observation.

Does not prove: a distinct `RawOutcome` object or `NormalizedToolResult`
identity that can be independently linked to a later binding decision.

### Post hook versus final delivery

Claim: `post_tool_call` observes the dispatch result before
`transform_tool_result`; the final delivered result may differ from what the
post hook saw.

- Evidence:
  [`model_tools.py#L1239-L1291`](https://github.com/NousResearch/hermes-agent/blob/444b5e96fa2829c29cfd7ecdc84d89f83a1441da/model_tools.py#L1239-L1291)
  dispatches the tool through middleware and carries Hermes-owned correlation
  keys.
- Evidence:
  [`model_tools.py#L1300-L1311`](https://github.com/NousResearch/hermes-agent/blob/444b5e96fa2829c29cfd7ecdc84d89f83a1441da/model_tools.py#L1300-L1311)
  emits `post_tool_call`.
- Evidence:
  [`model_tools.py#L1313-L1347`](https://github.com/NousResearch/hermes-agent/blob/444b5e96fa2829c29cfd7ecdc84d89f83a1441da/model_tools.py#L1313-L1347)
  runs `transform_tool_result` after `post_tool_call` and before returning the
  result for conversation delivery.

Implication: Phase 1A can measure post-hook-visible versus final-delivered
result digests.

Does not prove: post-hook observation equals final delivery.

## Identity observations

Hermes already carries several IDs:

- session_id: session scope;
- task_id: turn/task scope;
- turn_id: generated once for a turn;
- api_request_id: model request scope;
- tool_call_id: supplied by the model/provider and propagated to the tool result message.

These IDs are useful lifecycle correlation keys. They are not equivalent to the identities required by the original binding-debugger hypothesis.

The pinned source does not create:

- an executor-owned attempt_id for every actual tool execution attempt;
- an executor-created raw_outcome_id at terminal outcome formation;
- a normalized_result_id that crosses a separately observable normalization boundary;
- a binding_decision_id representing a candidate-selection decision.

In particular, tool_call_id is provider/model-owned. task_id and turn_id are not per-attempt identities.

## Sequential execution

The sequential path passes the original tool_call.id into handle_function_call and later into make_tool_result_message. The result is therefore associated with the originating model tool call through propagation.

The source does not show a later binder selecting among competing invocation candidates. A handler returns, the result is normalized, hooks observe it, and the tool message is appended.

## Concurrent execution

The concurrent path retains the original parsed-call list and submits workers with the original list index. Completed results are placed back into that index and appended in original tool-call order. The original tool_call.id is used to construct each tool result message.

This is a real delivery-association mechanism. It is not evidence of a separate binder that receives multiple candidate outcomes and makes a later binding decision.

## Retry semantics

The inspected retry counters and branches primarily concern model API failures, invalid tool names or arguments, compression/fallback, and model-response handling. The pinned path does not expose a retry controller that re-executes one tool invocation as multiple executor attempts and later chooses a result between them.

Therefore the phrase “retry/repeated tool calls” cannot be used as proof of executor attempt identity in this source version.

## Hook and observation boundaries

The strongest available lifecycle seams are:

- turn context creation;
- model request start/response;
- tool request middleware and pre_tool_call;
- registry dispatch and handler completion;
- post_tool_call;
- transform_tool_result;
- tool result message append.

The post-hook observes the result after dispatch and before final message delivery. The transform hook can change the result after post observation. This distinction matters: a post-hook observation is not automatically the final delivered value.

## Session boundary

Hermes has session IDs, session persistence, conversation history, and prompt assembly. The current path does not provide the MVP's independent pair of:

- entrypoint-supplied expected_session_id;
- resource-owned session identity observed at history loading.

The session family is therefore deferred. It cannot be claimed from the current source inspection.

## Current evidence judgment

The source supports a lifecycle observability project:

model tool_call
-> hook/dispatch
-> handler completion
-> normalized/delivered tool result
-> message append

The source does not support the stronger claim that TraceLab can presently diagnose outcome-to-invocation binding mismatch using independent producer and binder evidence.

Under the Tool Binding spike rules:

- TB-F1 Attempt Identity: NOT SATISFIED
- TB-F2 Origin Capture: NOT SATISFIED
- TB-F3 Binding Capture: NOT SATISFIED as a production candidate-selection seam
- TB-F4 Lineage Continuity: NOT SATISFIED
- TB-F5 Fault Discriminability: NOT RUN because the required evidence contract fails

## Decision

Downgrade the Tool family to lifecycle observability for this pinned Hermes path.

Before any permanent recorder, graph, backward slice, replay, or Session family implementation, the project owner must either:

1. approve the lifecycle-observability scope; or
2. identify another Hermes surface, such as an asynchronous gateway, subagent route, or result-routing layer, that contains a real candidate-selection seam and request a new evidence audit.

The owner decision is recorded in `spike/go-no-go.md`: Phase 1A may proceed
only as lifecycle observability. This document does not claim that Hermes has no
future or external surface with stronger binding semantics.
