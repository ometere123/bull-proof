# Threat Model

## Security goal

NullProof should never turn a weak, retrospective, incomplete, or leader-controlled observation process into a strong `ABSENCE_ESTABLISHED` certificate.

## Malicious requester chooses favourable sources

**Not prevented.** Source selection is policy.

Mitigation: the complete sealed source set is committed into `definition_hash`. A consumer must explicitly accept that definition hash or inspect the source set.

NullProof proves absence **over the declared evidence surface**, not the whole internet.

## Retrospective cherry-picking

Attack: create a claim after a window ends, inspect old pages, and present that as continuous monitoring.

Mitigation: `create_claim` requires a future start time, and sealing must happen before the window starts.

## Source-set mutation after bad news

Attack: remove a source after it publishes the qualifying event.

Mitigation: the source set is immutable after `seal_claim`.

## Malicious leader returns NOT_FOUND when an event exists

Mitigation: validators independently fetch and classify the source. A validator that sees `FOUND` rejects a `NOT_FOUND` leader result.

## Malicious leader fabricates FOUND evidence

Mitigation: the excerpt must occur verbatim in the validator's independently fetched page and pass an independent event/window relevance judgment.

## Source outage treated as negative evidence

Mitigation: outages produce `UNAVAILABLE`, which never extends successful negative coverage.

## Ambiguous content treated as negative evidence

Mitigation: `AMBIGUOUS` never extends successful negative coverage.

## Temporary outage hidden between successful checks

The protocol does not pretend to know what happened between snapshots. The claim instead declares `max_gap_seconds` before monitoring begins.

If two successful negative observations are farther apart than that bound, finalization fails with `INSUFFICIENT_COVERAGE`.

## Missed beginning or end of window

Coverage includes edge conditions. A first successful observation later than `start_at + max_gap_seconds`, or a last successful observation earlier than `end_at - max_gap_seconds`, prevents an absence certificate.

## Backfilling a gap later

Impossible. Observation timestamps come from transaction time, and observations after `end_at` are rejected.

## Prompt injection inside monitored pages

The classification prompt treats source content as hostile data and explicitly forbids following embedded instructions. Independent validators repeat the task.

This reduces, but cannot mathematically eliminate, shared model failure. Consumers should choose authoritative, low-adversarial sources when possible.

## Dynamic pages differ between leader and validators

If the material event class differs, validators disagree and normal consensus does not accept the proposed observation. This is safer than silently recording a false negative.

## Observer griefing

Observation is permissionless. A caller can only record `AMBIGUOUS` or `UNAVAILABLE` when consensus agrees with that source state. Such observations do not destroy earlier successful coverage; they simply do not fill time.

## Universal absence

NullProof intentionally does not provide it.

`ABSENCE_ESTABLISHED` means only:

> no qualifying event was found on the sealed required sources under the declared observation-gap policy during the declared window.

The contract exposes this boundary directly rather than hiding it behind a confidence score.
