# BullProof

**Prospective negative-evidence certificates for GenLayer.**

BullProof is a standalone reusable Intelligent Contract that answers a deceptively hard question:

> Can another contract safely rely on the claim that a qualifying event was **not found** across a declared public evidence surface during a declared time window?

It does **not** treat one failed search as proof of absence. It creates a sealed, prospective monitoring protocol in which independent GenLayer validators repeatedly re-observe required sources, and deterministic contract logic decides whether temporal coverage was complete enough to establish a bounded negative claim.

There is intentionally **no frontend**. BullProof is infrastructure for other contracts.

## Why this primitive exists

Positive evidence is easy to model: one source can prove that an event happened. Negative evidence is fundamentally different. "I looked once and did not see it" does not establish that nothing appeared over an interval.

BullProof makes the epistemic boundary explicit:

> `ABSENCE_ESTABLISHED` means **no qualifying event was found across the sealed source set while every required source satisfied the declared maximum observation-gap policy**.

It never claims to prove that an event did not exist anywhere on the internet.

## State machine

```text
DRAFT
  │ add required public sources
  │ seal before start_at
  ▼
MONITORING
  │
  ├── consensus FOUND ───────────────────────► EVENT_FOUND
  │
  └── window ends
         │
         ├── every source satisfies coverage ─► ABSENCE_ESTABLISHED
         │
         └── any source has a blind gap ──────► INSUFFICIENT_COVERAGE

DRAFT ── requester aborts before sealing ─────► ABORTED
```

Terminal states cannot be rewritten.

## The core idea: temporal coverage

For every required source BullProof stores:

- first successful `NOT_FOUND` observation;
- last successful `NOT_FOUND` observation;
- maximum gap between successful negative observations;
- unavailable observations;
- ambiguous observations;
- found observations.

A source satisfies coverage only when:

```text
first_success - window_start <= max_gap
window_end - last_success <= max_gap
max(success[i] - success[i-1]) <= max_gap
```

Only consensus-backed `NOT_FOUND` observations extend the successful coverage chain.

`AMBIGUOUS` and `UNAVAILABLE` never fill a gap.

That means an outage at 12:10 followed by a successful check at 12:20 cannot be retroactively rewritten as continuous evidence. If the successful-observation gap exceeds the policy, the final certificate is `INSUFFICIENT_COVERAGE`.

## Why claims are prospective

BullProof deliberately rejects backdated claims.

`create_claim(...)` requires `start_at` to be at least 60 seconds in the future. The requester must add sources and call `seal_claim(...)` before monitoring begins.

Once sealed:

- sources cannot be added or removed;
- the subject cannot change;
- the event definition cannot change;
- the time window cannot change;
- the maximum gap policy cannot change.

This prevents a requester from searching history, selecting only sources that happen to look clean, and presenting the result as if continuous monitoring had occurred.

## Consensus architecture

BullProof uses `gl.vm.run_nondet_unsafe` with a custom validator.

### Leader

For an observation the leader:

1. fetches the required public source with `gl.nondet.web.render`;
2. treats the rendered page as hostile data;
3. asks an LLM to classify the source snapshot as:
   - `FOUND`
   - `NOT_FOUND`
   - `AMBIGUOUS`
   - `UNAVAILABLE` is produced by runtime/source failure;
4. requires a verbatim grounded excerpt for `FOUND`;
5. returns only bounded decision fields and diagnostic text.

### Validators

A validator does **not** check JSON shape and trust the leader.

Each validator independently:

1. fetches the source again;
2. independently performs the same event classification;
3. requires the same decision class;
4. for `FOUND`, verifies that the leader's evidence is present in the validator's own snapshot;
5. independently judges that the excerpt actually supports the qualifying event in the declared window.

A forged leader `NOT_FOUND` is rejected when the validator independently observes `FOUND`.

This follows GenLayer's recommended pattern for classification and settlement logic: validators independently derive the decision rather than merely validating format.

## Contract surface

### Create a claim

```python
claim_id = bullproof.create_claim(
    "ACME Model Z",
    "An official safety recall of ACME Model Z is announced or becomes effective.",
    start_at,
    end_at,
    max_gap_seconds,
)
```

### Add required sources

```python
source_id = bullproof.add_source(
    claim_id,
    "Official recall registry",
    "https://example.com/recalls",
)
```

All configured sources are required. A duplicated URL is rejected.

### Seal the evidence surface

```python
bullproof.seal_claim(claim_id)
```

This writes a canonical `definition_hash` over:

```text
subject
qualifying event definition
start_at
end_at
max_gap_seconds
ordered source labels + URLs
```

### Record an observation

```python
observation_id = bullproof.observe(claim_id, source_id)
```

Anyone may call `observe`. The requester does not control who is allowed to check the source.

### Finalize

```python
bullproof.finalize(claim_id)
```

After `end_at`, finalization is deterministic. No LLM is asked whether coverage is "good enough".

### Consume from another contract

```python
ok = bullproof.is_absence_established(claim_id, expected_definition_hash)
```

The expected definition hash prevents a consumer from accidentally accepting an absence certificate for a weaker source set, different event definition, wider gap policy, or different time window.

## Example use cases

BullProof is intentionally domain-neutral. The same primitive can support:

- **insurance:** no official recall or exclusion notice appeared during a coverage window;
- **governance:** no veto notice was published before a deadline;
- **SLA settlement:** no termination notice appeared during a service interval;
- **compliance:** no sanctions/listing event appeared across declared registries;
- **warranties:** no disqualifying manufacturer notice was found during a warranty period;
- **agent workflows:** no cancellation/revocation notice was published before autonomous execution;
- **prediction/resolution markets:** establish bounded negative conditions without trusting one oracle server.

## Security properties

### No historical backfill

A valid proof can only start after registration. Missed past coverage cannot be reconstructed later.

### Immutable evidence surface

The source set is frozen before the observation window.

### Independent validator re-observation

Validators fetch and classify for themselves.

### Negative observations carry no leader-selected evidence

`NOT_FOUND`, `AMBIGUOUS`, and `UNAVAILABLE` receipts store no evidence excerpt. Their force comes from independent consensus, not from text selected by the leader.

### Positive terminal evidence is source-grounded

A `FOUND` receipt must carry a verbatim excerpt present in the validator's own snapshot and must pass a second relevance/qualification check.

### Fail closed on uncertainty

Ambiguity and source failure never extend temporal coverage.

### No money movement

BullProof does not custody, transfer, lock, release, slash, or mint value. Consumer contracts decide what a valid BullProof certificate means for their own state.

## Repository structure

```text
contracts/bullproof.py          core Intelligent Contract
tests/direct/test_bullproof.py  direct-mode protocol + adversarial tests
docs/CONSENSUS.md               leader/validator design
docs/THREAT_MODEL.md            attacks, assumptions, epistemic limits
docs/INTEGRATION.md             downstream composition patterns
examples/absence_gate.py        minimal cross-contract consumer
scripts/preflight.py            repository/static preflight checks
SUBMISSION.md                   reviewer-focused submission summary
```

## Test suite

The direct suite contains 17 tests covering:

- prospective-only claim creation;
- immutable source surfaces;
- duplicate source rejection;
- passive event definitions;
- observation-window boundaries;
- negative coverage accumulation;
- positive terminal evidence;
- malicious false-negative leader rejection;
- forged evidence rejection;
- complete temporal coverage;
- internal coverage gaps;
- ambiguous observations not filling gaps;
- missing leading coverage;
- all required sources participating;
- early finalization rejection;
- post-window observation rejection;
- requester authorization for draft mutation.

Run:

```bash
python -m pip install -r requirements-test.txt
pytest tests/direct -q
```

Optional linter:

```bash
python -m pip install -r requirements.txt
genvm-lint check contracts/bullproof.py
```

GenLayer's current `genlayer-test` release is `0.29.2`; `genvm-linter` is `0.11.0`.

## Deployment

BullProof has no constructor arguments.

```bash
npm install -g genlayer
genlayer network studionet
genlayer deploy --contract contracts/bullproof.py
```

The contract does not require a backend, database, keeper server, or frontend. Observations are ordinary contract writes and may be submitted by any caller.

## Epistemic statement

BullProof proves a **bounded monitoring statement**, not universal non-existence.

A certificate is only as broad as:

1. the event definition;
2. the required source set;
3. the observation window;
4. the maximum permitted gap between successful negative observations.

Those four things are deliberately committed into the immutable definition hash so downstream contracts can choose exactly what evidence policy they are willing to trust.

## License

MIT
