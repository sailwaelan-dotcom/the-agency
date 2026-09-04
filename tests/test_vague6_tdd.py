#!/usr/bin/env python3
"""
TDD Tests — vague 6 (be-devis-quotes + persona deviseur-be)
Tests écrits AVANT le skill. Doivent échouer (RED) puis passer (GREEN).

Vérifie :
- existence du skill et du persona
- frontmatter valide (name == dossier, description trigger-focused
  commençant par « Utilisez quand », metadata complète)
- sections obligatoires (Overview, When to Use, Workflow, Pitfalls, Checklist)
- related_skills qui résolvent
- contenu métier attendu (tarification, mentions, numérotation, validité,
  acompte, relance, passage devis → facture Peppol)
- persona : rôle, skills à charger, posture, limites
- passage de validate_skills.py et security_scan.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import validate_skills  # noqa: E402
import security_scan  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"
AGENTS_DIR = REPO_ROOT / ".agents" / "agents"

FAILURES = []

SKILL_NAME = "be-devis-quotes"
PERSONA_NAME = "deviseur-be"

EXPECTED_TAGS = {"sales", "devis", "be"}
EXPECTED_RELATED = {"be-sales-outreach", "be-invoicing-peppol", "be-contracts-legal"}

# Contenu métier attendu du skill
EXPECTED_CONTENT = ["devis", "tarification", "validité", "acompte", "BCE",
                    "TVA", "Peppol", "relance", "numérotation", "be-sales-outreach",
                    "be-invoicing-peppol", "be-contracts-legal"]

# Vocabulaire de chiffrage attendu (workflow de tarification)
EXPECTED_PRICING = ["tjm", "forfait", "phase", "acompte"]

REQUIRED_SECTIONS = ["## Overview", "## When to Use", "## Workflow",
                     "## Common Pitfalls", "## Verification Checklist"]


def check(label: str, condition: bool, detail: str = ""):
    if not condition:
        FAILURES.append(f"FAIL {label}: {detail}")


def skill_path() -> Path:
    return SKILLS_DIR / SKILL_NAME / "SKILL.md"


def persona_path() -> Path:
    return AGENTS_DIR / f"{PERSONA_NAME}.md"


def parse_frontmatter(content: str) -> dict:
    import yaml
    end = content.find("\n---", 3)
    if end == -1:
        return {}
    fm = yaml.safe_load(content[3:end])
    return fm if isinstance(fm, dict) else {}


# === T1 : Le skill existe ===
def test_skill_exists():
    check("skill-exists", skill_path().exists(), f"{skill_path()} n'existe pas encore")


# === T2 : Frontmatter valide ===
def test_frontmatter():
    if not skill_path().exists():
        check("frontmatter", False, "skill n'existe pas")
        return
    fm = parse_frontmatter(skill_path().read_text(encoding="utf-8"))

    check("fm-name", fm.get("name") == SKILL_NAME,
          f"name '{fm.get('name')}' != '{SKILL_NAME}'")

    desc = str(fm.get("description", ""))
    check("fm-desc-trigger", desc.startswith("Utilisez quand"),
          f"description ne commence pas par 'Utilisez quand': {desc[:60]}")
    desc_l = desc.lower()
    for trigger in ("devis", "tarif", "facture"):
        check(f"fm-desc-trigger-{trigger}", trigger in desc_l,
              f"description sans le déclencheur '{trigger}'")

    meta = fm.get("metadata") or {}
    for field in ("tags", "related_skills", "domain", "language", "as_of"):
        check(f"fm-meta-{field}", field in meta and meta[field] not in (None, [], ""),
              f"metadata.{field} manquant ou vide")
    check("fm-domain", meta.get("domain") == "sales",
          f"domain '{meta.get('domain')}' != 'sales'")
    check("fm-language", meta.get("language") == "fr",
          f"language '{meta.get('language')}' != 'fr'")
    check("fm-asof", str(meta.get("as_of", "")) == "2026-09",
          f"as_of '{meta.get('as_of')}' != '2026-09'")
    check("fm-tags", EXPECTED_TAGS <= set(meta.get("tags") or []),
          f"tags attendus {sorted(EXPECTED_TAGS)} absents de {meta.get('tags')}")
    check("fm-related", EXPECTED_RELATED <= set(meta.get("related_skills") or []),
          f"related_skills attendus {sorted(EXPECTED_RELATED)} absents de {meta.get('related_skills')}")


# === T3 : Sections obligatoires ===
def test_required_sections():
    if not skill_path().exists():
        check("sections", False, "skill n'existe pas")
        return
    content = skill_path().read_text(encoding="utf-8")
    end = content.find("\n---", 3)
    body = content[end + 4:] if end != -1 else content
    for section in REQUIRED_SECTIONS:
        check(f"section-{section}", section in body, f"section manquante: {section}")


# === T4 : related_skills qui résolvent ===
def test_related_skills_resolve():
    if not skill_path().exists():
        check("related-resolve", False, "skill n'existe pas")
        return
    fm = parse_frontmatter(skill_path().read_text(encoding="utf-8"))
    for rel in (fm.get("metadata") or {}).get("related_skills") or []:
        check(f"related-{rel}", (SKILLS_DIR / rel / "SKILL.md").exists(),
              f"related_skill '{rel}' ne résout pas")


# === T5 : Contenu métier attendu ===
def test_domain_content():
    if not skill_path().exists():
        check("content", False, "skill n'existe pas")
        return
    content = skill_path().read_text(encoding="utf-8")
    missing = [kw for kw in EXPECTED_CONTENT if kw not in content]
    check("content", not missing, f"contenu métier manquant: {missing}")
    content_l = content.lower()
    missing_pricing = [kw for kw in EXPECTED_PRICING if kw not in content_l]
    check("content-pricing", not missing_pricing,
          f"vocabulaire de tarification manquant: {missing_pricing}")


# === T6 : Le devis → facture est couvert (boucle avec Peppol) ===
def test_devis_to_invoice_loop():
    if not skill_path().exists():
        check("devis-facture", False, "skill n'existe pas")
        return
    content = skill_path().read_text(encoding="utf-8").lower()
    has_loop = re.search(r"devis.{0,200}factur", content, re.DOTALL)
    check("devis-facture", bool(has_loop),
          "passage devis accepté → facture Peppol non décrit")


# === T7 : Le persona deviseur-be existe et suit le format maison ===
def test_persona():
    p = persona_path()
    check("persona-exists", p.exists(), f"{p} n'existe pas encore")
    if not p.exists():
        return
    content = p.read_text(encoding="utf-8")
    for part in ("**Rôle**", "**Skills à charger**", "**Posture**", "**Ce qu'il ne fait pas**"):
        check(f"persona-{part}", part in content, f"section persona manquante: {part}")
    for skill in (SKILL_NAME, "be-invoicing-peppol", "be-sales-outreach"):
        check(f"persona-charge-{skill}", f"`{skill}`" in content,
              f"le persona ne charge pas `{skill}`")


# === T8 : Passe le validateur du repo ===
def test_skill_passes_validator():
    skill_dir = SKILLS_DIR / SKILL_NAME
    if not (skill_dir / "SKILL.md").exists():
        check("validator", False, "skill n'existe pas")
        return
    errors = validate_skills.validate_skill(skill_dir)
    check("validator", len(errors) == 0, f"erreurs: {errors[:3]}")


# === T9 : Passe le scanner de sécurité (aucun finding BLOCK) ===
def test_passes_security_scan():
    targets = [skill_path(), persona_path()]
    for target in targets:
        if not target.exists():
            check(f"security-{target.name}", False, "fichier n'existe pas")
            continue
        findings = security_scan.scan_file(target)
        blocks = [f for f in findings if f[0] == "BLOCK"]
        check(f"security-{target.name}", not blocks,
              f"findings bloquants: {blocks[:3]}")


# === Exécution ===
if __name__ == "__main__":
    test_skill_exists()
    test_frontmatter()
    test_required_sections()
    test_related_skills_resolve()
    test_domain_content()
    test_devis_to_invoice_loop()
    test_persona()
    test_skill_passes_validator()
    test_passes_security_scan()

    if FAILURES:
        print(f"RED — {len(FAILURES)} échec(s) (attendu en TDD) :")
        for f in FAILURES:
            print(f"  {f}")
        sys.exit(1)
    print(f"GREEN — tous les tests vague 6 passent ({SKILL_NAME} + {PERSONA_NAME})")
    sys.exit(0)
