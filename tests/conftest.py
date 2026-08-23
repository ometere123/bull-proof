import pytest


@pytest.fixture(autouse=True)
def _reset_contract_registry():
    """Keep independently deployed direct tests isolated without constraining Studio tests."""
    yield
    try:
        import genlayer.gl.genvm_contracts as contracts
    except ImportError:
        return
    contracts.__known_contract__ = None
