# Phase 0 Execution Path

Inspection date: 2026-07-16 20:51:50 CST

## Fixed Research Object

```text
TraceLab repository: https://github.com/Himekaovo/Hermes-TraceLab.git
TraceLab base commit: eb1c897334101bd7d123a5509801300baa29d39a
TraceLab branch: restart-tracelab-phase0
Hermes repository: NOT_BOUND
Hermes commit SHA: NOT_BOUND
Hermes tag/release: NOT_BOUND
Selected runtime entrypoint: UNKNOWN
Python version: 3.9.6
Operating system: Darwin 25.5.0 arm64
```

The requested repository contains the TraceLab project, but it does not contain
the real Hermes runtime under test. No external Hermes repository, commit, or
runtime entrypoint was provided with the request.

## Required Runtime Path

Phase 0 must inspect this real path before Phase 1 can start:

```text
User input
-> model output
-> tool-call parse
-> invocation creation
-> attempt creation
-> executor dispatch
-> raw result/error
-> retry handling
-> normalization
-> result binding
-> history/prompt assembly
```

## Current Observation

The path cannot be traced in this repository yet because the system under test
is missing.

This file therefore records a conservative Phase 0 blocker instead of inventing
production lifecycle identities or binding seams.

## Required Next Input

To continue Phase 0, bind a real Hermes runtime:

```text
Hermes repository URL or local path:
Hermes commit SHA:
Runtime entrypoint:
Minimal command to run a tool-calling session:
Any fixture or scenario that performs two adjacent tool calls:
```

Until then, Phase 1 remains blocked.
