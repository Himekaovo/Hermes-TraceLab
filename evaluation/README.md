# Evaluation

Evaluation distinguishes real Hermes regressions, SUT mutations, boundary faults, trace-only tests, and negative controls. Small case counts are reported per case; they are not presented as broad statistical claims.

The evaluation must include:

- recorder fidelity against an independent fixture side channel;
- a legal retry or repeated-call negative control;
- at least one incomplete or recorder-failure case that yields INCONCLUSIVE;
- captured-input component replay results;
- runtime, storage, and privacy measurements once instrumentation exists.
