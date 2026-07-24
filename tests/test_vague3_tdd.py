#!/usr/bin/env python3
"""
TDD Tests — vague 3 skills (be-sales-outreach, be-financial-modeling, be-contracts-legal)
Tests écrits AVANT les skills. Doivent échouer (RED) puis passer (GREEN).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import validate_skills  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"

FAILURES = []

# Skills de la vague 3
VAGUE3_SKILLS = [
    "be-sales-outreach",
    "be-financial-modeling",
    "be-contracts-legal",
]


def check(label: str, condition: bool, detail: str = ""):
    if not condition:
        FAILURES.append(f"FAIL {label}: {detail}")


def test_skill_exists(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    check(f"{name}-exists", skill_md.exists(),
          f"{skill_md} n'existe pas encore")


def test_skill_passes_validator(name: str):
    skill_dir = SKILLS_DIR / name
    if not (skill_dir / "SKILL.md").exists():
        check(f"{name}-validator", False, "skill n'existe pas")
        return
    errors = validate_skills.validate_skill(skill_dir)
    check(f"{name}-validator", len(errors) == 0,
          f"erreurs: {errors[:3]}")


def test_description_trigger(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    if not skill_md.exists():
        check(f"{name}-desc-trigger", False, "skill n'existe pas")
        return
    import re
    content = skill_md.read_text(encoding="utf-8")
    m = re.search(r'description:\s*"([^"]+)"', content)
    if not m:
        check(f"{name}-desc-trigger", False, "pas de description")
        return
    desc = m.group(1)
    has_trigger = re.search(r"(utilisez|use when|quand|dès que)", desc, re.I)
    check(f"{name}-desc-trigger", bool(has_trigger),
          f"description non trigger-focused: {desc[:80]}")


def test_required_sections(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    if not skill_md.exists():
        check(f"{name}-sections", False, "skill n'existe pas")
        return
    content = skill_md.read_text(encoding="utf-8")
    end = content.find("\n---", 3)
    body = content[end + 4:] if end != -1 else content

    required = ["## Overview", "## When to Use", "## Common Pitfalls",
                "## Verification Checklist"]
    for section in required:
        check(f"{name}-section-{section}", section in body,
              f"section manquante: {section}")


def test_belgian_content(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    if not skill_md.exists():
        check(f"{name}-be-content", False, "skill n'existe pas")
        return
    content = skill_md.read_text(encoding="utf-8").lower()
    # Doit contenir des références belges
    be_refs = ["belgique", "belge", "bce", "srl", "tva", "inasti",
               "spf", "bruxelles", "wallonie", "flandre"]
    found = [r for r in be_refs if r in content]
    check(f"{name}-be-content", len(found) >= 3,
          f"contenu BE insuffisant: {found}")


def test_disclaimer(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    if not skill_md.exists():
        check(f"{name}-disclaimer", False, "skill n'existe pas")
        return
    import re
    content = skill_md.read_text(encoding="utf-8")
    has_disclaimer = re.search(
        r"Disclaimer.{0,400}(comptable|avocat|expert-comptable|agréé)",
        content, re.I | re.S)
    check(f"{name}-disclaimer", bool(has_disclaimer),
          "disclaimer fiscal/juridique absent")


# === Exécution ===
if __name__ == "__main__":
    for skill_name in VAGUE3_SKILLS:
        test_skill_exists(skill_name)
        test_skill_passes_validator(skill_name)
        test_description_trigger(skill_name)
        test_required_sections(skill_name)
        test_belgian_content(skill_name)
        test_disclaimer(skill_name)

    total_tests = len(VAGUE3_SKILLS) * 6
    if FAILURES:
        print(f"RED — {len(FAILURES)}/{total_tests} tests échoués (attendu en TDD):")
        for f in FAILURES:
            print(f"  {f}")
        sys.exit(1)
    print(f"GREEN — {total_tests}/{total_tests} tests vague 3 passent")
    sys.exit(0)
