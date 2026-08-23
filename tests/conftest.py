import pytest


@pytest.fixture(autouse=True)
def _configure_direct_mode(direct_vm):
    """Catch storage-serialization mistakes and isolate contract definitions per test."""
    direct_vm.check_pickling = True
    yield
    try:
        import genlayer.gl.genvm_contracts as contracts
    except ImportError:
        return
    contracts.__known_contract__ = None
