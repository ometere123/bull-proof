"""Focused hardening regressions for NullProof."""

from datetime import datetime, timezone

CONTRACT = "contracts/nullproof.py"
SUBJECT = "ACME Model Z"
EVENT = "An official safety recall of ACME Model Z is announced or becomes effective."
CLASSIFIER = r"You are adjudicating one prospective NullProof negative-evidence observation"
BASE_ISO = "2026-08-23T20:00:00+00:00"
START_ISO = "2026-08-23T20:10:00+00:00"
END_ISO = "2026-08-23T20:40:00+00:00"


def epoch(value: str) -> int:
    return int(datetime.fromisoformat(value).astimezone(timezone.utc).timestamp())


START = epoch(START_ISO)
END = epoch(END_ISO)
GAP = 600


def new_draft(vm, deploy):
    vm.warp(BASE_ISO)
    contract = deploy(CONTRACT)
    claim_id = contract.create_claim(SUBJECT, EVENT, START, END, GAP)
    return contract, claim_id


def new_sealed(vm, deploy, url="https://example.com/recalls"):
    contract, claim_id = new_draft(vm, deploy)
    source_id = contract.add_source(claim_id, "Official registry", url)
    contract.seal_claim(claim_id)
    return contract, claim_id, source_id


def test_url_gate_rejects_private_local_numeric_and_ambiguous_targets(direct_vm, direct_deploy):
    contract, claim_id = new_draft(direct_vm, direct_deploy)

    bad_urls = (
        "http://example.com/recalls",
        "https://localhost/recalls",
        "https://127.0.0.1/recalls",
        "https://10.0.0.1/recalls",
        "https://169.254.169.254/latest/meta-data",
        "https://192.168.1.4/recalls",
        "https://172.16.0.1/recalls",
        "https://service.internal/recalls",
        "https://user:pass@example.com/recalls",
        "https://example.com:8443/recalls",
        "https://2130706433/recalls",
        "https://0177.0.0.1/recalls",
        "https://%31%32%37.0.0.1/recalls",
        "https://127.0.0.1.nip.io/recalls",
        "https://foo..example.com/recalls",
        "https://-bad.example.com/recalls",
        "https://bad-.example.com/recalls",
    )

    for url in bad_urls:
        with direct_vm.expect_revert("EXPECTED"):
            contract.add_source(claim_id, "bad source", url)


def test_only_requester_can_seal_definition(direct_vm, direct_deploy, direct_alice):
    contract, claim_id = new_draft(direct_vm, direct_deploy)
    contract.add_source(claim_id, "Official registry", "https://example.com/recalls")

    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert("only requester may seal"):
            contract.seal_claim(claim_id)


def test_source_from_another_claim_cannot_be_observed(direct_vm, direct_deploy):
    direct_vm.warp(BASE_ISO)
    contract = direct_deploy(CONTRACT)

    first_claim = contract.create_claim(SUBJECT, EVENT, START, END, GAP)
    first_source = contract.add_source(first_claim, "First registry", "https://example.com/recalls")
    contract.seal_claim(first_claim)

    second_claim = contract.create_claim("ACME Model Y", EVENT, START, END, GAP)
    contract.add_source(second_claim, "Second registry", "https://example.org/recalls")
    contract.seal_claim(second_claim)

    direct_vm.warp(START_ISO)
    with direct_vm.expect_revert("source does not belong"):
        contract.observe(second_claim, first_source)


def test_empty_source_is_unavailable_and_never_extends_negative_coverage(direct_vm, direct_deploy):
    contract, claim_id, source_id = new_sealed(direct_vm, direct_deploy)
    direct_vm.mock_web(r".*example\.com/recalls.*", {"status": 503, "body": ""})
    direct_vm.warp(START_ISO)

    observation_id = contract.observe(claim_id, source_id)
    receipt = contract.get_observation(observation_id)
    coverage = contract.get_coverage(claim_id, source_id)

    assert receipt["verdict_name"] == "UNAVAILABLE"
    assert coverage["unavailable_count"] == 1
    assert coverage["successful_count"] == 0
    assert coverage["complete"] is False
    assert direct_vm.run_validator() is True


def test_unparseable_semantic_result_becomes_ambiguous_not_negative_evidence(direct_vm, direct_deploy):
    contract, claim_id, source_id = new_sealed(direct_vm, direct_deploy)
    direct_vm.mock_web(
        r".*example\.com/recalls.*",
        {"status": 200, "body": "ACME safety notices are available on this page."},
    )
    direct_vm.mock_llm(CLASSIFIER, "definitely maybe")
    direct_vm.warp(START_ISO)

    observation_id = contract.observe(claim_id, source_id)
    receipt = contract.get_observation(observation_id)
    coverage = contract.get_coverage(claim_id, source_id)

    assert receipt["verdict_name"] == "AMBIGUOUS"
    assert coverage["ambiguous_count"] == 1
    assert coverage["successful_count"] == 0
    assert coverage["complete"] is False


def test_validator_rejects_non_integer_leader_verdict(direct_vm, direct_deploy):
    contract, claim_id, source_id = new_sealed(direct_vm, direct_deploy)
    direct_vm.mock_web(
        r".*example\.com/recalls.*",
        {"status": 200, "body": "ACME Safety Notices: no qualifying Model Z recall is listed."},
    )
    direct_vm.mock_llm(
        CLASSIFIER,
        {"verdict": "NOT_FOUND", "reason": "no qualifying event", "evidence": ""},
    )
    direct_vm.warp(START_ISO)
    contract.observe(claim_id, source_id)

    direct_vm.clear_mocks()
    direct_vm.mock_web(
        r".*example\.com/recalls.*",
        {"status": 200, "body": "ACME Safety Notices: no qualifying Model Z recall is listed."},
    )
    direct_vm.mock_llm(
        CLASSIFIER,
        {"verdict": "NOT_FOUND", "reason": "no qualifying event", "evidence": ""},
    )
    assert direct_vm.run_validator(
        leader_result={"verdict": "1", "reason": "wrong type", "evidence": ""}
    ) is False
