#!/usr/bin/env python3
"""
TDD Tests — fact-check-sourcing skill
Tests écrits AVANT le skill. Doivent échouer (RED) puis passer (GREEN).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import validate_skills  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"
FACTCHECK_DIR = SKILLS_DIR / "fact-check-sourcing"
FACTCHECK_MD = FACTCHECK_DIR / "SKILL.md"

FAILURES = []


def check(label: str, condition: bool, detail: str = ""):
    if not condition:
        FAILURES.append(f"FAIL {label}: {detail}")


# === T1 : Le skill existe ===
def test_skill_exists():
    check("skill-exists", FACTCHECK_MD.exists(),
          f"{FACTCHECK_MD} n'existe pas encore")


# === T2 : Le skill passe le validateur ===
def test_skill_passes_validator():
    if not FACTCHECK_MD.exists():
        check("validator", False, "skill n'existe pas")
        return
    errors = validate_skills.validate_skill(FACTCHECK_DIR)
    check("validator", len(errors) == 0,
          f"erreurs: {errors[:3]}")


# === T3 : Description trigger-focused ===
def test_description_trigger():
    if not FACTCHECK_MD.exists():
        check("desc-trigger", False, "skill n'existe pas")
        return
    import re
    content = FACTCHECK_MD.read_text(encoding="utf-8")
    m = re.search(r'description:\s*"([^"]+)"', content)
    if not m:
        check("desc-trigger", False, "pas de description")
        return
    desc = m.group(1)
    has_trigger = re.search(r"(utilisez|use when|quand|dès que)", desc, re.I)
    check("desc-trigger", bool(has_trigger),
          f"description non trigger-focused: {desc[:80]}")


# === T4 : Sections obligatoires ===
def test_required_sections():
    if not FACTCHECK_MD.exists():
        check("sections", False, "skill n'existe pas")
        return
    content = FACTCHECK_MD.read_text(encoding="utf-8")
    # Extraire le body (après le 2e ---)
    end = content.find("\n---", 3)
    body = content[end + 4:] if end != -1 else content

    required = ["## Overview", "## When to Use", "## Common Pitfalls",
                "## Verification Checklist"]
    for section in required:
        check(f"section-{section}", section in body,
              f"section manquante: {section}")


# === T5 : Définit des sources fiables ===
def test_reliable_sources():
    if not FACTCHECK_MD.exists():
        check("sources", False, "skill n'existe pas")
        return
    content = FACTCHECK_MD.read_text(encoding="utf-8").lower()
    # Doit mentionner au moins 3 sources officielles belges
    belgian_sources = ["spf finances", "inasti", "bce", "statbel",
                       "national bank", "banque nationale", "apd",
                       "vlaio", "innoviris", "spw"]
    found = [s for s in belgian_sources if s in content]
    check("sources-be", len(found) >= 3,
          f"sources BE insuffisantes: {found}")


# === T6 : Fournit une méthodologie de fact-checking ===
def test_methodology():
    if not FACTCHECK_MD.exists():
        check("methodology", False, "skill n'existe pas")
        return
    content = FACTCHECK_MD.read_text(encoding="utf-8").lower()
    # Doit contenir des concepts clés de fact-checking
    concepts = ["source", "vérif", "citation", "as_of", "date"]
    found = [c for c in concepts if c in content]
    check("methodology", len(found) >= 3,
          f"concepts méthodologie insuffisants: {found}")


# === T7 : Définit un format de citation ===
def test_citation_format():
    if not FACTCHECK_MD.exists():
        check("citation", False, "skill n'existe pas")
        return
    content = FACTCHECK_MD.read_text(encoding="utf-8").lower()
    # Doit contenir des éléments de format de citation
    citation_elements = ["url", "lien", "référence", "source", "date"]
    found = [c for c in citation_elements if c in content]
    check("citation-format", len(found) >= 3,
          f"éléments citation insuffisants: {found}")


# === T8 : Disclaimer présent ===
def test_disclaimer():
    if not FACTCHECK_MD.exists():
        check("disclaimer", False, "skill n'existe pas")
        return
    import re
    content = FACTCHECK_MD.read_text(encoding="utf-8")
    has_disclaimer = re.search(
        r"Disclaimer.{0,400}(comptable|avocat|expert-comptable|agréé)",
        content, re.I | re.S)
    check("disclaimer", bool(has_disclaimer),
          "disclaimer fiscal/juridique absent")


# === Exécution ===
if __name__ == "__main__":
    test_skill_exists()
    test_skill_passes_validator()
    test_description_trigger()
    test_required_sections()
    test_reliable_sources()
    test_methodology()
    test_citation_format()
    test_disclaimer()

    if FAILURES:
        print("RED — Tests échoués (attendu en TDD):")
        for f in FAILURES:
            print(f"  {f}")
        sys.exit(1)
    print("GREEN — 8/8 tests fact-check-sourcing passent")
    sys.exit(0)
