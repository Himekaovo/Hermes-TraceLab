# Event Contract

Phase 1 is not active yet, but Phase 0 evaluates whether the following event
contract can be supported by a real Hermes runtime.

## Minimum Event Fields

```yaml
event_id:
run_id:
event_type:
occurred_at:
recorded_at:
schema_version:
producer_component:
source_location:
parent_event_ids:
payload:
```

## Candidate Phase 1 Event Types

```text
RunStarted
InvocationAccepted
AttemptStarted
AttemptCompleted
RawOutcomeObserved
ResultNormalized
BindingObserved
PromptAssemblyObserved
RunCompleted
RecorderFailure
```

## Contract Rules

- `event_id` identifies a recorder event, not a Hermes lifecycle identity.
- Recorder events must cite source locations.
- Recorder failures must be explicit events or explicit report limitations.
- Derived detector conclusions must reference source event IDs.
- Missing critical events must block SUT violation claims.
