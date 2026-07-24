#!/usr/bin/env python3
"""
TDD Tests — fact-check-sourcing v2 (gate actif)
Tests écrits AVANT le skill. Vérifient que le skill est un GATE ACTIF
qui s'applique après chaque web search, pas une référence passive.
"""
import re
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
          f"{FACTCHECK_MD} n'existe pas")


# === T2 : Le skill passe le validateur ===
def test_skill_passes_validator():
    if not FACTCHECK_MD.exists():
        check("validator", False, "skill n'existe pas")
        return
    errors = validate_skills.validate_skill(FACTCHECK_DIR)
    check("validator", len(errors) == 0,
          f"erreurs: {errors[:3]}")


# === T3 : Description trigger-focused ET gate actif ===
def test_description_is_active_gate():
    if not FACTCHECK_MD.exists():
        check("desc-gate", False, "skill n'existe pas")
        return
    content = FACTCHECK_MD.read_text(encoding="utf-8")
    m = re.search(r'description:\s*"([^"]+)"', content)
    if not m:
        check("desc-gate", False, "pas de description")
        return
    desc = m.group(1).lower()

    # Le gate doit s'activer automatiquement
    has_auto = re.search(r"(automatique|automatically|après chaque|systématiquement|permanent)", desc)
    check("desc-auto-trigger", bool(has_auto),
          f"description ne mentionne pas le déclenchement automatique: {desc[:80]}")

    # Le gate doit mentionner web search
    has_web_search = re.search(r"(web.search|web.extract|recherche)", desc)
    check("desc-web-search", bool(has_web_search),
          f"description ne mentionne pas web search: {desc[:80]}")

    # Le gate doit être décrit comme actif, pas passif
    has_active = re.search(r"(gate|actif|active|vérif|crois|bloqu|score)", desc)
    check("desc-active", bool(has_active),
          f"description ne décrit pas un comportement actif: {desc[:80]}")


# === T4 : Sections obligatoires ===
def test_required_sections():
    if not FACTCHECK_MD.exists():
        check("sections", False, "skill n'existe pas")
        return
    content = FACTCHECK_MD.read_text(encoding="utf-8")
    end = content.find("\n---", 3)
    body = content[end + 4:] if end != -1 else content

    required = ["## Overview", "## When to Use", "## Common Pitfalls",
                "## Verification Checklist"]
    for section in required:
        check(f"section-{section}", section in body,
              f"section manquante: {section}")


# === T5 : Définit un système de scoring (A/B/C/D) ===
def test_scoring_system():
    if not FACTCHECK_MD.exists():
        check("scoring", False, "skill n'existe pas")
        return
    content = FACTCHECK_MD.read_text(encoding="utf-8").lower()

    # Doit définir des niveaux de fiabilité
    has_levels = re.search(r"(niveau|level|score|a/b/c/d|officielle|institutionnelle|journalistique|non.vérifiable)", content)
    check("scoring-levels", bool(has_levels),
          "système de niveaux de fiabilité non défini")

    # Doit définir des actions par niveau (utiliser/bloquer/croiser)
    has_actions = re.search(r"(utilisable|bloquer|croiser|ne pas utiliser|vérifier)", content)
    check("scoring-actions", bool(has_actions),
          "actions par niveau non définies")


# === T6 : Définit des sources officielles belges ===
def test_official_sources():
    if not FACTCHECK_MD.exists():
        check("sources", False, "skill n'existe pas")
        return
    content = FACTCHECK_MD.read_text(encoding="utf-8").lower()

    # Doit lister les sources officielles belges
    official_sources = ["spf finances", "inasti", "statbel", "bce",
                        "vlaio", "awex", "innoviris", "apd", "banque nationale"]
    found = [s for s in official_sources if s in content]
    check("sources-be", len(found) >= 5,
          f"sources BE insuffisantes: {found}")

    # Doit avoir des URLs
    has_urls = re.search(r"(finances\.belgium|rsvz-inasti|statbel|vlaio|awex|hub\.brussels|innoviris)", content)
    check("sources-urls", bool(has_urls),
          "URLs des sources officielles manquantes")


# === T7 : Décrit l'intégration dans le workflow ===
def test_workflow_integration():
    if not FACTCHECK_MD.exists():
        check("workflow", False, "skill n'existe pas")
        return
    content = FACTCHECK_MD.read_text(encoding="utf-8").lower()

    # Doit décrire le pattern après web_search
    has_pattern = re.search(r"(web_search|web.extract|après chaque|pattern|workflow|étape)", content)
    check("workflow-pattern", bool(has_pattern),
          "pattern d'intégration workflow non décrit")

    # Doit décrire les étapes du gate
    has_steps = re.search(r"(étape|step|1\.|2\.|3\.|4\.)", content)
    check("workflow-steps", bool(has_steps),
          "étapes du gate non définies")


# === T8 : Produit un score de confiance ===
def test_confidence_score():
    if not FACTCHECK_MD.exists():
        check("confidence", False, "skill n'existe pas")
        return
    content = FACTCHECK_MD.read_text(encoding="utf-8").lower()

    # Doit produire un score de confiance
    has_score = re.search(r"(score.*confiance|confidence.*score|as_of|date.*consultation)", content)
    check("confidence-score", bool(has_score),
          "score de confiance non produit")

    # Doit formater le score
    has_format = re.search(r"(\[a/b/c/d\]|\[oui/non\]|\[YYYY-MM\])", content)
    check("confidence-format", bool(has_format),
          "format de score non défini")


# === Exécution ===
if __name__ == "__main__":
    test_skill_exists()
    test_skill_passes_validator()
    test_description_is_active_gate()
    test_required_sections()
    test_scoring_system()
    test_official_sources()
    test_workflow_integration()
    test_confidence_score()

    if FAILURES:
        print("RED — Tests échoués:")
        for f in FAILURES:
            print(f"  {f}")
        sys.exit(1)
    print("GREEN — 10/10 tests fact-check-sourcing v2 (gate actif) passent")
    sys.exit(0)
