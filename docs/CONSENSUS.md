# Consensus Design

## What consensus decides

For each required source snapshot, GenLayer consensus decides one bounded semantic fact:

- `NOT_FOUND`: the source is readable and no qualifying in-window event is present;
- `FOUND`: the source contains grounded evidence of the qualifying event;
- `AMBIGUOUS`: relevant material cannot be resolved safely;
- `UNAVAILABLE`: the source cannot be read.

The final absence certificate is **not** an LLM verdict. It is deterministic state derived from accumulated consensus observations.

## Leader function

The leader independently fetches the frozen source URL and runs the frozen event-definition task against that page. Web content is explicitly framed as hostile data.

A `FOUND` proposal is only well formed if its excerpt is verbatim and grounded in the leader's fetched source.

## Validator function

The validator receives the leader result but does not treat the leader classification as authoritative.

It independently re-fetches the same URL and independently classifies the snapshot.

Consensus-relevant fields are deliberately small:

```text
leader verdict == validator verdict
```

For `FOUND`, additional requirements apply:

```text
leader evidence is bounded
leader evidence occurs verbatim in validator snapshot
independent evidence judge returns PASS
```

For `NOT_FOUND`, `AMBIGUOUS`, and `UNAVAILABLE`, evidence must be empty.

## Why exact verdict matching

NullProof uses coarse terminal semantic classes rather than comparing model prose. Reason text is diagnostic only.

The classes are settlement-relevant:

- `NOT_FOUND` extends the coverage chain;
- `FOUND` terminates the claim;
- `AMBIGUOUS` extends no coverage;
- `UNAVAILABLE` extends no coverage.

Allowing a tolerance between these classes could change deterministic protocol state, so they must match.

## Why a second evidence judge exists

A validator independently obtaining `FOUND` is not enough to trust arbitrary leader-selected text. The leader could attach an unrelated excerpt while still proposing the correct class.

The second judgment binds the stored excerpt to the subject, event definition, and declared time window.

## Deterministic settlement

After consensus returns, storage changes happen outside the nondeterministic block.

A successful `NOT_FOUND` updates:

```text
successful_count
first_success_at
last_success_at
max_gap_seen
```

A `FOUND` sets `EVENT_FOUND` and stores the terminal observation ID.

`AMBIGUOUS` and `UNAVAILABLE` update diagnostic counters but do not extend coverage.

After the window, `finalize` evaluates every required source using only integer timestamp arithmetic. No web request or LLM participates in finalization.

## Evidence-surface boundary

Source selection is requester-defined policy, not a validator judgment. NullProof makes that policy explicit, immutable before monitoring begins, and committed into `definition_hash`.

Consumers should only accept hashes whose source set, event definition, time window, and maximum-gap policy meet their own requirements.
