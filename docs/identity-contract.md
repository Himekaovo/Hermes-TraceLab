# Identity Contract

Phase 0 determines whether Hermes exposes stable lifecycle identities.

## Required Lifecycle Identities

```text
run_id
invocation_id
attempt_id
raw_outcome_id
normalized_result_id
binding_decision_id
```

## Ownership Rules

- Lifecycle IDs must be created by the component that owns the lifecycle.
- The recorder may observe lifecycle IDs but must not invent them.
- Content hashes are not valid substitutes for missing lifecycle IDs.
- Retry attempts must have distinct attempt identity.
- Normalization must not overwrite raw outcome identity.

## Unsupported Identity Sources

The following are not sufficient for strong provenance:

- list index;
- log line number;
- wall-clock order alone;
- object memory address;
- fixture-only truth;
- detector-side reconstruction.
