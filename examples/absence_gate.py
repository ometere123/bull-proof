"""Minimal BullProof composition example; illustrative, not required for deployment."""

from genlayer import *


@gl.contract_interface
class IBullProof:
    class View:
        def is_absence_established(self, claim_id: u256, expected_definition_hash: str) -> bool: ...


class AbsenceGate(gl.Contract):
    bullproof_address: Address
    claim_id: u256
    definition_hash: str
    opened: bool

    def __init__(self, bullproof_address: Address, claim_id: u256, definition_hash: str):
        self.bullproof_address = bullproof_address
        self.claim_id = claim_id
        self.definition_hash = definition_hash
        self.opened = False

    @gl.public.write
    def open_if_absence_established(self) -> None:
        bullproof = gl.get_contract_at(self.bullproof_address, IBullProof)
        if not bullproof.view().is_absence_established(self.claim_id, self.definition_hash):
            raise gl.vm.UserError("BullProof certificate is not valid for the pinned definition")
        self.opened = True

    @gl.public.view
    def is_open(self) -> bool:
        return self.opened
