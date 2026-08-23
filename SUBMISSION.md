# BullProof — Standalone Intelligent Contract Submission

## One-line purpose

BullProof is a reusable GenLayer primitive for **prospective negative evidence**: it can establish that no qualifying event was found across a sealed set of public sources during a time window, but only when consensus-backed observations are dense enough to satisfy a precommitted maximum-gap policy.

## Why this is not a thin LLM wrapper

The LLM handles only the semantic observation at each source snapshot.

The protocol-level result comes from persistent state and deterministic mechanics:

- prospective registration;
- immutable source surface;
- immutable event/window/gap policy;
- independent validator re-observation;
- permissionless observation writes;
- per-source coverage chains;
- edge-gap and internal-gap accounting;
- terminal positive evidence;
- deterministic post-window finalization;
- definition-hash pinning for downstream contracts.

One LLM answer can never directly create `ABSENCE_ESTABLISHED`.

## Consensus logic

For each observation:

1. the leader fetches the required public source;
2. the leader classifies it as `FOUND`, `NOT_FOUND`, or `AMBIGUOUS`;
3. runtime/source failure maps to `UNAVAILABLE`;
4. a validator independently fetches and independently classifies;
5. decision classes must match exactly;
6. a `FOUND` excerpt must exist verbatim in the validator's own snapshot and pass an independent event/window relevance judgment.

The validator therefore verifies the semantic decision, not just the schema.

## State design

### Claim

Stores requester, subject, event definition, future window, maximum allowed observation gap, source IDs, status, definition hash, terminal observation, certificate hash, and lifecycle timestamps.

### SourceRecord

Each required URL is permanently bound to one claim after sealing.

### SourceCoverage

Stores successful-negative count, first/last successful-negative timestamps, maximum successful-observation gap, and ambiguity/unavailability diagnostics.

### Observation

Immutable receipt containing source, caller, transaction timestamp, consensus verdict, bounded rationale, and grounded positive evidence when applicable.

## Epistemic correctness

The contract never says "the event did not happen."

It says:

> no qualifying event was found across this exact sealed evidence surface while all required sources satisfied this exact temporal sampling policy.

That boundary is a feature. It makes the primitive safe to compose.

## Reuse

Potential consumers include insurance, governance, compliance, warranty, SLA, agent revocation, prediction/resolution, and conditional-execution contracts.

The primary composition method is:

```python
is_absence_established(claim_id, expected_definition_hash)
```

## Adversarial test focus

The Direct Mode suite exercises state transitions, authorization, source freezing, prospective-only creation, temporal coverage, ambiguity gaps, multi-source requirements, and malicious leader proposals.

Important regressions include:

- leader proposes `NOT_FOUND`, validator independently sees `FOUND` -> reject;
- leader proposes forged `FOUND` evidence absent from validator source -> reject;
- ambiguous observation between two negative observations -> does not fill the gap;
- late first observation -> cannot be backfilled;
- one uncovered required source -> whole absence certificate fails.

## No frontend / no backend

This submission is intentionally only the reusable contract primitive plus tests, documentation, and a minimal composition example. No hosted backend or frontend is required.
