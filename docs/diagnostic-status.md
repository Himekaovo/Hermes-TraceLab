# Diagnostic Status

Reports may use only conservative diagnostic states.

## Allowed States

```text
CONTROL_PASS
SUT_VIOLATION
RECORDER_FAILURE
INCOMPLETE_TRACE
INCONCLUSIVE
UNSUPPORTED
```

## Meaning

`CONTROL_PASS` means the control scenario produced sufficient evidence and no
supported invariant was violated.

`SUT_VIOLATION` means recorder fidelity passed, trace completeness was
sufficient, and a supported invariant was violated by the system under test.

`RECORDER_FAILURE` means the trace cannot be trusted because the recorder lost,
duplicated, reordered, or mutated critical evidence.

`INCOMPLETE_TRACE` means required evidence is missing and recorder fault is not
fully established.

`INCONCLUSIVE` means evidence is insufficient for a stronger state.

`UNSUPPORTED` means the current runtime or release boundary does not support
the requested diagnostic claim.
