import pytest


@pytest.fixture(autouse=True)
def _enable_pickling_validation(direct_vm):
    """Make Direct Mode catch storage serialization bugs before network testing."""
    direct_vm.check_pickling = True
    yield
