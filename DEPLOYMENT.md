# NullProof — Verified StudioNet deployment

This is the canonical evidence record for the live NullProof run. Values below are complete transaction hashes and complete state hashes, not abbreviated notes.

## Submission identity

- Repository: https://github.com/ometere123/nullproof
- Evidence-record base commit: `bd211759d2b57a20d367f8a0ba3fd39f911bb272`
- Current submission HEAD should be verified from GitHub `main` at review time.
- Contract: `contracts/nullproof.py`
- Contract Git blob: `42c193d6e1d9067dbd1a4fbd42a364e37944ccdc`
- Contract SHA-256 after LF normalization: `e76a9ff911426cc5999fb3a342b32b7262cc1de8fe02859e639b4e0fa7a90413`
- Deployed contract-source commit: `93ba827b7072f4dc676d8c5f13c7ffc0e44f2014`
- Later submission commits: `7547bc7` changed the historical positive fixture; `bd211759` changed tests and documentation only.
- Class: `NullProof`
- Interface: `INullProof`
- Public methods: 13 — 7 views and 6 writes

The canonical deployment was created from commit `93ba827b7072f4dc676d8c5f13c7ffc0e44f2014`. `git diff 93ba827b7072f4dc676d8c5f13c7ffc0e44f2014..bd211759d2b57a20d367f8a0ba3fd39f911bb272 -- contracts/nullproof.py` is empty, and the current contract blob remains `42c193d6e1d9067dbd1a4fbd42a364e37944ccdc`. StudioNet `gen_getContractCode` returned 36,883 bytes whose SHA-256 is exactly `e76a9ff911426cc5999fb3a342b32b7262cc1de8fe02859e639b4e0fa7a90413`. Therefore the evidence-record base commit contains the exact deployed contract source; later fixture/test/documentation commits were not deployments. Reviewers should verify the current submission HEAD from GitHub `main` at review time.

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

## CANONICAL ABSENCE_ESTABLISHED live proof

- Claim: `9`
- Subject: `ACME Model Z`
- Event definition: `An official safety-recall announcement for ACME Model Z is announced or becomes effective during the target window.`
- Window: `start_at=1787569055`, `end_at=1787569355`
- Maximum gap: `240` seconds
- Definition hash: `387ae9bd0f2231a2953ebb1d59ee01bd5f0188fd3a2a404a2199760cee6243a6`
- Certificate hash: `046843db6cb05af1cc8bd784895151613aff158b2ce54897bda0add8c0544c57`

### Source 1

- Source ID: `16`
- URL: `https://raw.githubusercontent.com/ometere123/nullproof/main/fixtures/no_event_a.txt`
- Successful count: `2`
- First successful timestamp: `1787569077`
- Last successful timestamp: `1787569148`
- Leading gap: `22`
- Trailing gap: `207`
- Maximum internal gap: `71`
- Maximum observed gap: `71`
- Unavailable count: `0`
- Ambiguous count: `0`
- Complete: `true`
- Observation IDs: `20`, `22`
- Observation transactions: `0x9920b1306aef8246fd3574b36610e3b72714daf49f5bb82ae8a5ad04b8ff97fa`, `0xbe1b3623ab689ca8af5c74be192b132328a7d4cdc71036b379c1ac817aceb3ee`

### Source 2

- Source ID: `17`
- URL: `https://raw.githubusercontent.com/ometere123/nullproof/main/fixtures/no_event_b.txt`
- Successful count: `2`
- First successful timestamp: `1787569112`
- Last successful timestamp: `1787569179`
- Leading gap: `57`
- Trailing gap: `176`
- Maximum internal gap: `67`
- Maximum observed gap: `67`
- Unavailable count: `0`
- Ambiguous count: `0`
- Complete: `true`
- Observation IDs: `21`, `23`
- Observation transactions: `0x9ac03ee2eb9107cab2e2ef1437b6e3117ecfd0bce2e2fdbbf6f9a9ede59d98d1`, `0xaf35dc5daafef95db08e91e9b824c1afea27d19fd24e2799379f00841754842b`

Transactions: create `0x69396da479fd39c5afad9f61179625fd029b3d3c81568e03ad9eb5cd323643e5`; add source A `0x7417d99295722240e685fb40a3f60f4041973e5a7a7fee60be7efc99de450c65`; add source B was finalized successfully but its CLI hash was not retained in the captured output; seal `0xb9c6dabf3d5d70e95353dcf3ada8f1ac7a725c2dc6ad9bc8601625f8c53a2ca3`; finalize `0xc91bfd15215ff0e10d3395a0cd06b5e3e99ed897ca745bd9df91cb7d2da72f2a`.

Verified readback:

- `status_name == ABSENCE_ESTABLISHED`
- every required source `complete == true`
- every leading, trailing, and internal gap is `<= 240`
- `is_absence_established(9, correct_definition_hash) == true`
- `is_absence_established(9, wrong_definition_hash) == false`

The qualifying event is positively defined; each persisted observation is `NOT_FOUND`. Only complete deterministic temporal coverage produces the terminal absence state.

## HISTORICAL ABSENCE PROOF

Earlier claim `4` reached `ABSENCE_ESTABLISHED` successfully and remains retained for transparency. Its event definition was negatively phrased (`No official ... is found ...`), so claim `9` supersedes it as the canonical flagship absence demonstration. Claim `4` was mechanically valid; claim `9` is semantically cleaner.

- Definition hash: `a859a08d460392919db7de5cf5f9a2d4373aa3f179f5e04e0bb6fa644a640618`
- Certificate hash: `7a22bf8df0950d1887ebe7d29388db0683ba230ba70f052bd9d3b02169636bc4`
- Finalization transaction: `0xffb5ec115c0840b69fb1dcd066fecc48090e9cf38060d05d537837fdc7c17473`
- Sources: IDs `6` and `7`, both complete; maximum internal gaps `127` and `139`; correct hash readback `true`; wrong hash readback `false`.

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
