#!/usr/bin/env python3
"""Auto-test de skill_meta.split_list — format « liste en chaîne » des metadata (spec agentskills.io)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from skill_meta import split_list  # noqa: E402

CASES = [
    ("chaine-virgules", "finance, tax, be", ["finance", "tax", "be"]),
    ("espaces-superflus", "  a ,b,  c  ", ["a", "b", "c"]),
    ("element-unique", "be-company-setup", ["be-company-setup"]),
    ("chaine-vide", "", []),
    ("none", None, []),
    ("virgules-vides", "a,, ,b,", ["a", "b"]),
    ("liste-ancien-format", ["finance", "be"], ["finance", "be"]),
]


def test_split_list():
    for label, value, expected in CASES:
        assert split_list(value) == expected, f"{label}: {split_list(value)!r} != {expected!r}"


if __name__ == "__main__":
    test_split_list()
    print(f"OK: {len(CASES)}/{len(CASES)} cas split_list passent")
