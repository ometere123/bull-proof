# NullProof deployment and proof runbook

This repository contains only the GenLayer contract, tests, fixtures, and reviewer-facing documentation. It has no frontend, backend, database, CI workflow, money movement, or secrets.

## Reproducible checks

Run these from the repository root:

```powershell
python scripts/preflight.py
python -m compileall contracts tests scripts
genvm-lint check contracts/nullproof.py
```

The complete Direct Mode suite must be run under Linux/WSL because the pinned GenVM artifact is a Linux runtime:

```bash
python3 -m pytest tests/direct -q
```

## Exact-commit StudioNet deployment

Set the built-in StudioNet network and verify the account before deployment:

```bash
genlayer network set studionet
genlayer account
genlayer deploy --contract contracts/nullproof.py
```

Record the deployer, contract address, deployment transaction, source commit, and network. The source commit must be clean and must be the exact commit deployed. A deployment receipt being accepted or finalized is not, by itself, execution success.

## Live proof protocol

Use a fresh deployment of the exact final commit. Configure a prospective claim with the raw GitHub URLs for `fixtures/event_found.txt`, `fixtures/no_event_a.txt`, and `fixtures/no_event_b.txt` after the commit is public.

1. Create the claim, add the complete source set, and seal it before the window starts.
2. For the positive proof, observe the positive fixture after the window starts and record `EVENT_FOUND`, the terminal observation, evidence, definition hash, certificate hash, and successful execution receipts.
3. For the negative proof, observe both negative fixtures at the start and again near the end, keeping each source's leading, internal, and trailing gaps at or below the sealed policy. Finalize only after the window ends and record `ABSENCE_ESTABLISHED`, per-source coverage, definition hash, certificate hash, and successful execution receipts.
4. If coverage is deliberately incomplete, finalize a separate claim and record `INSUFFICIENT_COVERAGE`; never describe that result as absence.

Capture every transaction hash and the resulting public reads. Do not edit a source fixture or definition while a live claim is in progress. If a transaction is accepted but its execution receipt reports failure, record the failure and do not call it a proof.

## Scope boundary

NullProof supplies a consensus-backed public-evidence certificate. It does not custody, transfer, lock, release, slash, or mint value. Consumer contracts must pin the exact `definition_hash` and decide what a valid terminal certificate permits.
