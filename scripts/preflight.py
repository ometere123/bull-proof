"""Dependency-free reviewer-facing preflight for NullProof."""

from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "nullproof.py"
README = ROOT / "README.md"
TESTS = ROOT / "tests" / "direct" / "test_nullproof.py"
HARDENING = ROOT / "tests" / "direct" / "test_nullproof_hardening.py"


def require(condition: bool, message: str):
    if not condition:
        raise SystemExit(f"FAIL: {message}")
    print(f"OK: {message}")


def main():
    source = CONTRACT.read_text(encoding="utf-8")
    tests = TESTS.read_text(encoding="utf-8")
    hardening = HARDENING.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")

    ast.parse(source)
    ast.parse(tests)
    ast.parse(hardening)

    require("class NullProof(gl.Contract)" in source, "contract class is NullProof")
    require("class INullProof" in source, "cross-contract interface is INullProof")
    require("run_nondet_unsafe" in source, "custom leader/validator consensus is present")
    require("inspect_source_once" in source, "validators can independently re-observe sources")
    require("definition_hash" in source, "sealed definitions are hash-pinned")
    require("coverage_fields" in source, "temporal coverage is deterministic")
    require("CLAIM_ABSENCE_ESTABLISHED" in source, "absence is an explicit terminal state")
    require("CLAIM_INSUFFICIENT_COVERAGE" in source, "incomplete monitoring fails closed")
    require("test_validator_rejects_forged_false_negative" in tests, "false-negative leader regression exists")
    require("test_internal_gap_prevents_absence_certificate" in tests, "coverage-gap regression exists")
    require("no frontend" in readme.lower(), "README explains standalone primitive scope")
    require(tests.count("def test_") >= 18, "substantial direct-mode suite is present")

    core = "\n".join((source, tests, hardening, readme))
    require("BullProof" not in core, "legacy BullProof branding is absent from core files")
    require("bullproof.py" not in core, "legacy bullproof.py path is absent from core files")

    print("Preflight passed.")


if __name__ == "__main__":
    main()
