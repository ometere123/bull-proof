# NullProof — Verified StudioNet deployment

This is the canonical evidence record for the live NullProof run. Values below are complete transaction hashes and complete state hashes, not abbreviated notes.

## Canonical source

- Repository: https://github.com/ometere123/nullproof
- Final `main` commit: `7547bc76bfc39bec8f9c545827f46453a4d8146c`
- Contract: `contracts/nullproof.py`
- Git blob ID: `42c193d6e1d9067dbd1a4fbd42a364e37944ccdc`
- Final source bytes after LF normalization: 36,883
- Final source SHA-256: `e76a9ff911426cc5999fb3a342b32b7262cc1de8fe02859e639b4e0fa7a90413`
- Class: `NullProof`
- Interface: `INullProof`
- Public methods: 13 — 7 views and 6 writes

The canonical deployment was created from the contract source at commit `93ba827`. Commit `7547bc76bfc39bec8f9c545827f46453a4d8146c` changed only `fixtures/event_found.txt`; `git diff 93ba827..7547bc7 -- contracts/nullproof.py` is empty. StudioNet `gen_getContractCode` returned 36,883 bytes for the deployed address, and its SHA-256 is exactly `e76a9ff911426cc5999fb3a342b32b7262cc1de8fe02859e639b4e0fa7a90413`. Therefore the deployed contract bytes are byte-for-byte identical to the final repository contract file after line-ending normalization. The later fixture-only commit is recorded separately rather than misrepresented as a contract redeployment.

## Verification

- Direct Mode: 41 passed, 0 failed, 0 errors under Linux/WSL
- StudioNet integration: 3/3 passed against the final contract source
- Preflight: PASS
- Compileall: PASS
- GenVM lint: PASS
- Lint informational warning: the pinned runner is older than a newer available runner; the deployed source remains pinned to the tested runner required by this repository.

## StudioNet deployment

- Network: StudioNet (`https://studio.genlayer.com/api`)
- Deployer: `0x74c1BA0642994d0Df5d8B78c64Db3E7214EEfcde`
- Contract: `0x26b9FAdd9cCAB67D3b813CBBcf77400f92d0f31d`
- Deployment transaction: `0xc10fbee5b9c1f225ffd322d8e67d633854cfeb1173307fe597898557e3f1fc89`
- Deployment UTC: `2026-08-24T00:06:30.766035Z`
- Deployment status: `FINALIZED` when rechecked through StudioNet transaction status
- Deployed source identity: SHA-256 `e76a9ff911426cc5999fb3a342b32b7262cc1de8fe02859e639b4e0fa7a90413`

## Public fixture URLs

These are the exact canonical URLs stored in the live claims:

- Positive: `https://raw.githubusercontent.com/ometere123/nullproof/main/fixtures/event_found.txt`
- Negative A: `https://raw.githubusercontent.com/ometere123/nullproof/main/fixtures/no_event_a.txt`
- Negative B: `https://raw.githubusercontent.com/ometere123/nullproof/main/fixtures/no_event_b.txt`

The positive fixture is historical demonstration evidence effective throughout 24 August 2026 UTC. It is preserved in repository history and was not edited during any active claim.

For a future reproduction, do not edit this historical fixture or reuse its past effective date. Create a separate fixture whose effective interval is in the future, publish it before sealing a new prospective claim, and record the new source URL and lifecycle transactions. Existing claims remain auditable against the exact immutable source surface they sealed.

## EVENT_FOUND live proof

- Claim: `1`
- Subject: `ACME Model Z`
- Event definition: `The official public bulletin at the source is the qualifying safety-recall announcement for ACME Model Z during the target window.`
- Window: `start_at=1787530520`, `end_at=1787530640`
- Maximum gap: `120` seconds
- Source ID: `1`
- Source URL: `https://raw.githubusercontent.com/ometere123/nullproof/main/fixtures/event_found.txt`
- Definition hash: `b3ab17475b00942eae3986ca2bb21d664709510b152947300806de0301118de4`
- Terminal observation ID: `1`
- Observation timestamp: `1787530532`
- Verdict: `FOUND`
- Evidence: `At retrieval time, this fictional bulletin is the official qualifying safety-recall announcement for ACME Model Z. This bulletin is effective continuously throughout 24 August 2026 UTC, including any prospective target window on that date.`
- Certificate hash: `1c71d82ce15d9db31e72ecde47c53425143c922b62673567f7e88ee1bf2ec7cc`

Transactions, all executed successfully:

- Create claim: `0xa8e9c6ee8e2503d200f72abbce3c1feaa1e5728a9987cfed6da2cdba60d2efb3`
- Add source: `0xa96ff76d4162a80b5c807e03d578e461800b76b7e65b77e16d8ba739667f2dd4`
- Seal: `0xe9a832a3b38d624e2fd923eb81ed0d20128be98ecc86a8463de94ec79cdce246`
- Observe: `0x484fa4133456416fa2f9aae1fb2778404cb655fbcc8dfb5c282ec3142471de75`

Verified readback:

- `status_name == EVENT_FOUND`
- `is_event_found(1, correct_definition_hash) == true`
- `is_event_found(1, wrong_definition_hash) == false`
- `is_absence_established(1, correct_definition_hash) == false`

## ABSENCE_ESTABLISHED live proof

- Claim: `4`
- Subject: `ACME Model Z`
- Event definition: `No official safety-recall announcement for ACME Model Z is found on either required registry during the target window.`
- Window: `start_at=1787532036`, `end_at=1787532336`
- Maximum gap: `240` seconds
- Definition hash: `a859a08d460392919db7de5cf5f9a2d4373aa3f179f5e04e0bb6fa644a640618`
- Certificate hash: `7a22bf8df0950d1887ebe7d29388db0683ba230ba70f052bd9d3b02169636bc4`

### Source 1

- Source ID: `6`
- URL: `https://raw.githubusercontent.com/ometere123/nullproof/main/fixtures/no_event_a.txt`
- Successful count: `2`
- First successful timestamp: `1787532056`
- Last successful timestamp: `1787532183`
- Leading gap: `20`
- Trailing gap: `153`
- Maximum internal gap: `127`
- Maximum observed gap: `127`
- Unavailable count: `0`
- Ambiguous count: `0`
- Complete: `true`
- Observation IDs: `8`, `10`
- Observation transactions: `0x39730989e5e1e9542a23c7d89a60e94bea3ca538a005aa33022a08eb88b83d16`, `0x494f4b20ea9b0e688acfbf49df0173edb7c89d5b54a916d0579797f772b7d21f`

### Source 2

- Source ID: `7`
- URL: `https://raw.githubusercontent.com/ometere123/nullproof/main/fixtures/no_event_b.txt`
- Successful count: `2`
- First successful timestamp: `1787532071`
- Last successful timestamp: `1787532210`
- Leading gap: `35`
- Trailing gap: `126`
- Maximum internal gap: `139`
- Maximum observed gap: `139`
- Unavailable count: `0`
- Ambiguous count: `0`
- Complete: `true`
- Observation IDs: `9`, `11`
- Observation transactions: `0x7eaa69f6e154b6f677a15809f31510cf4937988eab1c59db2d600d892a4d5f26`, `0xcb01968ee3770a664fe19eedc0de56c9c3ddc4f17aed6288729df980edcc8d83`

Finalization transaction: `0xffb5ec115c0840b69fb1dcd066fecc48090e9cf38060d05d537837fdc7c17473`

Verified readback:

- `status_name == ABSENCE_ESTABLISHED`
- every required source `complete == true`
- every leading, trailing, and internal gap is `<= 240`
- `is_absence_established(4, correct_definition_hash) == true`
- `is_absence_established(4, wrong_definition_hash) == false`

## INSUFFICIENT_COVERAGE live proof

- Claim: `3`
- Source IDs: `4`, `5`
- Definition hash: `ad3ceae734c2268ce3be374c0edea589c3757d508c6ac191d7a75696d30657a1`
- Certificate hash: `45040a05a6306c7b0ee4687b9054ffdc3d110b1a7bdd14c9e46595bddb1bf5d1`
- Finalization transaction: `0x98366849e44bc56bda61d77e415779485a096b8220e21f3831401972594ef32e`
- Failure: both required sources had `successful_count=2`, but source 4 had trailing gap `478 > 300` and source 5 had trailing gap `451 > 300`.
- Verified readback: `status_name == INSUFFICIENT_COVERAGE`; `is_absence_established(3, correct_definition_hash) == false`.

## Reproduction and audit commands

Official current tooling documents the following commands:

```bash
python scripts/preflight.py
python -m compileall contracts tests examples scripts
python3 -m pytest tests/direct -v
genvm-lint check contracts/nullproof.py
gltest tests/integration/ -v -s --network studionet
```

For public state reads, use the GenLayer Studio contract interface for `get_claim`, `get_source`, `get_observation`, `get_coverage`, `is_event_found`, and `is_absence_established` at the canonical address above. The deployed contract source is available through `gen_getContractCode`; hash the returned bytes after normalizing repository line endings as documented above.

`examples/absence_gate.py` is the composability reference. The current Direct Mode harness does not execute cross-contract calls, so the repository reports static compile/lint verification for that consumer rather than inventing a runtime gate result.

## Scope and limitation

NullProof does not prove universal non-existence. It proves only that no qualifying event was found across this exact sealed evidence surface during this exact interval under this exact maximum-observation-gap policy. It contains no frontend, backend, database, hosted service, CI workflow, money movement, or secrets.
