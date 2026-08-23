# Integration Guide

BullProof is designed to be consumed by other Intelligent Contracts.

## Pin the definition

Do not rely only on `claim_id`.

Read the sealed claim and record the `definition_hash` your contract accepts:

```python
claim = bullproof.get_claim(claim_id)
expected = claim["definition_hash"]
```

Later:

```python
if bullproof.is_absence_established(claim_id, expected):
    ...
```

This prevents policy substitution.

## Example: governance no-veto gate

A DAO may require that no veto appears on two official publication surfaces during a 72-hour challenge period.

The governance contract can pin:

```text
subject: proposal 42
event: an official veto of proposal 42 is published or becomes effective
sources:
  - governance notices
  - council notices
window: challenge start -> challenge end
max gap: 15 minutes
```

Execution after the challenge period requires BullProof's `ABSENCE_ESTABLISHED` result for exactly that hash.

## Example: insurance exclusion gate

A settlement contract can require that no official product recall was found across the manufacturer and regulator registries during the relevant coverage window.

BullProof does not move insurance funds itself. It supplies the reusable public-evidence certificate.

## Example: autonomous-agent revocation

An agent can be authorised to execute only if no revocation notice appears on a declared policy endpoint before a deadline.

The consumer should still validate the source set during claim creation; BullProof guarantees that the sealed definition cannot later be weakened.

## Consumer checklist

Before trusting a BullProof certificate, a downstream contract or protocol should verify:

1. the subject is the intended entity;
2. the qualifying event definition is sufficiently precise;
3. every required URL is authoritative enough for the use case;
4. the observation window matches the business rule;
5. `max_gap_seconds` is strict enough;
6. the consumer pins the exact `definition_hash`;
7. terminal state is `ABSENCE_ESTABLISHED`, not merely `MONITORING` or `INSUFFICIENT_COVERAGE`.

## Read interface

```python
@gl.contract_interface
class IBullProof:
    class View:
        def get_claim(self, claim_id: u256) -> dict: ...
        def get_source(self, source_id: u256) -> dict: ...
        def get_observation(self, observation_id: u256) -> dict: ...
        def get_coverage(self, claim_id: u256, source_id: u256) -> dict: ...
        def is_absence_established(self, claim_id: u256, expected_definition_hash: str) -> bool: ...
        def is_event_found(self, claim_id: u256, expected_definition_hash: str) -> bool: ...
```

The write surface stays deliberately small. Consumers generally need only observation/finalization, while claim authors configure the evidence policy before the monitoring window begins.
