import pytest


@pytest.fixture(autouse=True)
def _enable_pickling_validation(direct_vm):
    """Make Direct Mode catch storage serialization bugs before network testing."""
    direct_vm.check_pickling = True

    # gltest 0.29.x refreshes sender/value after ``warp`` but leaves the
    # cached raw message datetime unchanged.  NullProof intentionally uses
    # the transaction timestamp, so keep the test harness's raw message in
    # sync with its public warp value.  This is test-only compatibility code;
    # production execution still receives the chain-supplied message.
    original_refresh = direct_vm._refresh_gl_message

    def refresh_with_datetime():
        original_refresh()
        import sys

        gl = sys.modules.get("genlayer.gl")
        if gl is not None and isinstance(getattr(gl, "message_raw", None), dict):
            gl.message_raw["datetime"] = direct_vm._datetime

    direct_vm._refresh_gl_message = refresh_with_datetime
    direct_vm._refresh_gl_message()
    yield
