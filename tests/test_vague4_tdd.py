#!/usr/bin/env python3
"""
TDD Tests — vague 4 skills (skill-forge, agency-doc-keeper)
Tests écrits AVANT les skills. Doivent échouer (RED) puis passer (GREEN).

Vérifie :
- existence des deux skills
- frontmatter valide (name == dossier, description trigger-focused
  commençant par « Utilisez quand », metadata complète)
- sections obligatoires (Overview, When to Use, Workflow, Pitfalls, Checklist)
- related_skills qui résolvent
- contenu métier attendu (gates, scripts, TDD)
- passage de validate_skills.py et security_scan.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import validate_skills  # noqa: E402
import security_scan  # noqa: E402
from tdd_common import check, parametrize_skills  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"

FAILURES = []

# Skills de la vague 4 : (nom, tags attendus, related attendus)
VAGUE4_SKILLS = {
    "skill-forge": {
        "tags": {"meta", "contribution", "tooling"},
        "related": {"agency-doc-keeper", "fact-check-sourcing"},
        # Contenu métier attendu (meta-skill de création de skills)
        "content": ["_template", "validate_skills.py", "security_scan.py",
                    "check_related_links.py", "frontmatter", "TDD"],
    },
    "agency-doc-keeper": {
        "tags": {"meta", "documentation", "maintenance"},
        "related": {"skill-forge", "fact-check-sourcing"},
        # Contenu métier attendu (maintenance documentaire du repo)
        "content": ["build_index.py", "check_doc_sync.py", "freshness_report.py",
                    "INDEX.md", "catalog.json", "CHANGELOG"],
    },
}


def read_skill(name: str) -> str:
    return (SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8")


def parse_frontmatter(content: str) -> dict:
    import yaml
    end = content.find("\n---", 3)
    if end == -1:
        return {}
    fm = yaml.safe_load(content[3:end])
    return fm if isinstance(fm, dict) else {}


# === T1 : Le skill existe ===
@parametrize_skills("name", list(VAGUE4_SKILLS))
def test_skill_exists(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    check(f"{name}-exists", skill_md.exists(),
          f"{skill_md} n'existe pas encore")


# === T2 : Frontmatter valide ===
@parametrize_skills("name", list(VAGUE4_SKILLS))
def test_frontmatter(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    if not skill_md.exists():
        check(f"{name}-frontmatter", False, "skill n'existe pas")
        return
    content = read_skill(name)
    fm = parse_frontmatter(content)

    # name == dossier
    check(f"{name}-fm-name", fm.get("name") == name,
          f"name '{fm.get('name')}' != dossier '{name}'")

    # description trigger-focused commençant par « Utilisez quand »
    desc = str(fm.get("description", ""))
    check(f"{name}-fm-desc-trigger", desc.startswith("Utilisez quand"),
          f"description ne commence pas par 'Utilisez quand': {desc[:60]}")

    # metadata complète
    meta = fm.get("metadata") or {}
    for field in ("tags", "related_skills", "domain", "language", "as_of"):
        check(f"{name}-fm-meta-{field}", field in meta and meta[field] not in (None, [], ""),
              f"metadata.{field} manquant ou vide")
    check(f"{name}-fm-domain", meta.get("domain") == "meta",
          f"domain '{meta.get('domain')}' != 'meta'")
    check(f"{name}-fm-language", meta.get("language") == "fr",
          f"language '{meta.get('language')}' != 'fr'")
    check(f"{name}-fm-asof", str(meta.get("as_of", "")) == "2026-08",
          f"as_of '{meta.get('as_of')}' != '2026-08'")

    # tags et related_skills conformes à la spec de la vague
    spec = VAGUE4_SKILLS[name]
    check(f"{name}-fm-tags", spec["tags"] <= set(meta.get("tags") or []),
          f"tags attendus {sorted(spec['tags'])} absents de {meta.get('tags')}")
    check(f"{name}-fm-related", spec["related"] <= set(meta.get("related_skills") or []),
          f"related_skills attendus {sorted(spec['related'])} absents de {meta.get('related_skills')}")


# === T3 : Sections obligatoires ===
@parametrize_skills("name", list(VAGUE4_SKILLS))
def test_required_sections(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    if not skill_md.exists():
        check(f"{name}-sections", False, "skill n'existe pas")
        return
    content = read_skill(name)
    end = content.find("\n---", 3)
    body = content[end + 4:] if end != -1 else content

    required = ["## Overview", "## When to Use", "## Workflow",
                "## Common Pitfalls", "## Verification Checklist"]
    for section in required:
        check(f"{name}-section-{section}", section in body,
              f"section manquante: {section}")


# === T4 : related_skills qui résolvent ===
@parametrize_skills("name", list(VAGUE4_SKILLS))
def test_related_skills_resolve(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    if not skill_md.exists():
        check(f"{name}-related-resolve", False, "skill n'existe pas")
        return
    fm = parse_frontmatter(read_skill(name))
    related = (fm.get("metadata") or {}).get("related_skills") or []
    for rel in related:
        check(f"{name}-related-{rel}",
              (SKILLS_DIR / rel / "SKILL.md").exists(),
              f"related_skill '{rel}' ne résout pas")


# === T5 : Contenu métier attendu ===
@parametrize_skills("name", list(VAGUE4_SKILLS))
def test_domain_content(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    if not skill_md.exists():
        check(f"{name}-content", False, "skill n'existe pas")
        return
    content = read_skill(name)
    missing = [kw for kw in VAGUE4_SKILLS[name]["content"] if kw not in content]
    check(f"{name}-content", not missing,
          f"contenu métier manquant: {missing}")


# === T6 : Passe le validateur du repo ===
@parametrize_skills("name", list(VAGUE4_SKILLS))
def test_skill_passes_validator(name: str):
    skill_dir = SKILLS_DIR / name
    if not (skill_dir / "SKILL.md").exists():
        check(f"{name}-validator", False, "skill n'existe pas")
        return
    errors = validate_skills.validate_skill(skill_dir)
    check(f"{name}-validator", len(errors) == 0,
          f"erreurs: {errors[:3]}")


# === T7 : Passe le scanner de sécurité (aucun finding BLOCK) ===
@parametrize_skills("name", list(VAGUE4_SKILLS))
def test_skill_passes_security_scan(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    if not skill_md.exists():
        check(f"{name}-security", False, "skill n'existe pas")
        return
    findings = security_scan.scan_file(skill_md)
    blocks = [f for f in findings if f[0] == "BLOCK"]
    check(f"{name}-security", not blocks,
          f"findings bloquants: {blocks[:3]}")


# === Exécution directe (mode CI « gates » : python tests/test_vague4_tdd.py) ===
TESTS = (test_skill_exists, test_frontmatter, test_required_sections,
         test_related_skills_resolve, test_domain_content,
         test_skill_passes_validator, test_skill_passes_security_scan)

if __name__ == "__main__":
    for skill_name in VAGUE4_SKILLS:
        for test_fn in TESTS:
            try:
                test_fn(skill_name)
            except AssertionError as e:
                FAILURES.append(f"FAIL {e}")

    total_checks = len(VAGUE4_SKILLS) * len(TESTS)
    if FAILURES:
        print(f"RED — {len(FAILURES)} échec(s) sur {len(VAGUE4_SKILLS)} skills "
              f"x {len(TESTS)} familles de tests (attendu en TDD):")
        for f in FAILURES:
            print(f"  {f}")
        sys.exit(1)
    print(f"GREEN — tous les tests vague 4 passent "
          f"({', '.join(VAGUE4_SKILLS)})")
    sys.exit(0)
