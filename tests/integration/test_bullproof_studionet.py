"""High-signal StudioNet lifecycle checks for BullProof.

These tests deliberately stop before the future monitoring window. Direct Mode
covers time warping, semantic observations, malicious validators, and terminal
certificates; StudioNet verifies that the real runtime deploys the contract and
persists the sealed prospective evidence definition correctly.
"""

from datetime import datetime, timezone

from gltest import get_contract_factory, get_default_account
from gltest.assertions import tx_execution_succeeded


CONTRACT = "bullproof.py"
TX_KW = {"consensus_max_rotations": 3, "wait_interval": 10000, "wait_retries": 20}


def future_window():
    now = int(datetime.now(timezone.utc).timestamp())
    start_at = now + 300
    end_at = start_at + 1800
    max_gap = 600
    return start_at, end_at, max_gap


def deploy_contract():
    factory = get_contract_factory(contract_file_path=CONTRACT)
    contract = factory.deploy(
        account=get_default_account(),
        consensus_max_rotations=3,
        wait_interval=10000,
        wait_retries=20,
    )
    assert contract.address
    return contract


def assert_success(receipt):
    assert tx_execution_succeeded(receipt), receipt


def test_deployment_and_status_dictionary():
    contract = deploy_contract()
    dictionary = contract.get_status_dictionary().call()
    assert dictionary["claim"]["DRAFT"] == 0
    assert dictionary["claim"]["MONITORING"] == 1
    assert dictionary["claim"]["ABSENCE_ESTABLISHED"] == 3
    assert dictionary["observation"]["NOT_FOUND"] == 1
    assert dictionary["observation"]["FOUND"] == 2


def test_future_claim_can_be_configured_and_sealed():
    contract = deploy_contract()
    start_at, end_at, max_gap = future_window()

    created = contract.create_claim([
        "ACME Model Z",
        "An official safety recall of ACME Model Z is announced or becomes effective.",
        start_at,
        end_at,
        max_gap,
    ]).transact(**TX_KW)
    assert_success(created)

    claim_id = 1
    draft = contract.get_claim([claim_id]).call()
    assert draft["status_name"] == "DRAFT"
    assert draft["definition_hash"] == ""

    added = contract.add_source([
        claim_id,
        "Official public registry",
        "https://example.com/recalls",
    ]).transact(**TX_KW)
    assert_success(added)

    sealed = contract.seal_claim([claim_id]).transact(**TX_KW)
    assert_success(sealed)

    claim = contract.get_claim([claim_id]).call()
    source = contract.get_source([1]).call()
    assert claim["status_name"] == "MONITORING"
    assert len(claim["definition_hash"]) == 64
    assert claim["source_ids"] == [1]
    assert source["claim_id"] == claim_id
    assert source["url"] == "https://example.com/recalls"
    assert contract.is_absence_established([claim_id, claim["definition_hash"]]).call() is False


def test_draft_can_be_aborted_before_sealing():
    contract = deploy_contract()
    start_at, end_at, max_gap = future_window()

    created = contract.create_claim([
        "ACME Model Z",
        "An official safety recall of ACME Model Z is announced or becomes effective.",
        start_at,
        end_at,
        max_gap,
    ]).transact(**TX_KW)
    assert_success(created)

    aborted = contract.abort_draft([1]).transact(**TX_KW)
    assert_success(aborted)
    assert contract.get_claim([1]).call()["status_name"] == "ABORTED"
