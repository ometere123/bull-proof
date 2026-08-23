"""Minimal NullProof composition example; illustrative, not required for deployment."""

from genlayer import *


@gl.contract_interface
class INullProof:
    class View:
        def is_absence_established(self, claim_id: u256, expected_definition_hash: str) -> bool: ...

    class Write:
        pass


class AbsenceGate(gl.Contract):
    nullproof_address: Address
    claim_id: u256
    definition_hash: str
    opened: bool

    def __init__(self, nullproof_address: Address, claim_id: u256, definition_hash: str):
        self.nullproof_address = nullproof_address
        self.claim_id = claim_id
        self.definition_hash = definition_hash
        self.opened = False

    @gl.public.write
    def open_if_absence_established(self) -> None:
        nullproof = INullProof(self.nullproof_address)
        if not nullproof.view().is_absence_established(self.claim_id, self.definition_hash):
            raise gl.vm.UserError("NullProof certificate is not valid for the pinned definition")
        self.opened = True

    @gl.public.view
    def is_open(self) -> bool:
        return self.opened
