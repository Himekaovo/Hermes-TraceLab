# Feasibility spike

The spike is time-boxed to one to three days. It answers one question:

> Can independent Hermes boundaries provide producer lineage and binding lineage, connected by immutable identities?

The spike may inspect Hermes, add the smallest temporary instrumentation needed to observe boundaries, and build a narrow SUT-level mutation fixture. It must not build a provenance graph, backward slice, HTML report, session tracing, repair assistant, or full replay framework.

Expected artifacts:

- execution-path.md: real Hermes call path and boundary ownership;
- instrumentation-notes.md: smallest observation changes and unresolved seams;
- acceptance-results.md: F1-F5 evidence and the go/no-go decision.
