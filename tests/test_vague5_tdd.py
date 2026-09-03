#!/usr/bin/env python3
"""
TDD Tests — vague 5 (activate-agency)
Tests écrits AVANT le skill. Doivent échouer (RED) puis passer (GREEN).

Vérifie :
- existence du skill
- frontmatter valide (name == dossier, description trigger-focused
  commençant par « Utilisez quand », metadata complète)
- sections obligatoires (Overview, When to Use, Workflow, Pitfalls, Checklist)
- related_skills qui résolvent
- contenu métier attendu (profil AGENCY_PROFILE.md, interview, shortlist,
  plan 30 jours, handoff, mode mise à jour)
- règle « jamais de données réelles dans le repo » (le profil vit hors du repo)
- phrase de handoff prête à copier
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

FAILURES = []

VAGUE5_SKILLS = {
    "activate-agency": {
        "tags": {"meta", "onboarding", "configuration"},
        "related": {"be-company-setup", "be-admin-deadlines", "fact-check-sourcing"},
        # Contenu métier attendu (onboarding + personnalisation)
        "content": ["AGENCY_PROFILE.md", "## Vous", "## Entreprise", "## Outils",
                    "## Objectifs", "## Journal", "30 jours", "handoff",
                    "mise à jour", "hors du repo", "shortlist"],
        # Les 8 questions de l'interview d'onboarding
        "interview": ["stade", "forme juridique", "tva", "secteur", "langue",
                      "comptable", "ca estimé", "objectifs"],
    },
}

REQUIRED_SECTIONS = ["## Overview", "## When to Use", "## Workflow",
                     "## Common Pitfalls", "## Verification Checklist"]


def check(label: str, condition: bool, detail: str = ""):
    if not condition:
        FAILURES.append(f"FAIL {label}: {detail}")


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
def test_skill_exists(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    check(f"{name}-exists", skill_md.exists(),
          f"{skill_md} n'existe pas encore")


# === T2 : Frontmatter valide ===
def test_frontmatter(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    if not skill_md.exists():
        check(f"{name}-frontmatter", False, "skill n'existe pas")
        return
    content = read_skill(name)
    fm = parse_frontmatter(content)

    check(f"{name}-fm-name", fm.get("name") == name,
          f"name '{fm.get('name')}' != dossier '{name}'")

    desc = str(fm.get("description", ""))
    check(f"{name}-fm-desc-trigger", desc.startswith("Utilisez quand"),
          f"description ne commence pas par 'Utilisez quand': {desc[:60]}")

    # La description doit capturer les formulations de déclenchement réelles
    desc_l = desc.lower()
    for trigger in ("activate", "commencer", "skills"):
        check(f"{name}-fm-desc-trigger-{trigger}", trigger in desc_l,
              f"description sans le déclencheur '{trigger}'")

    meta = fm.get("metadata") or {}
    for field in ("tags", "related_skills", "domain", "language", "as_of"):
        check(f"{name}-fm-meta-{field}", field in meta and meta[field] not in (None, [], ""),
              f"metadata.{field} manquant ou vide")
    check(f"{name}-fm-domain", meta.get("domain") == "meta",
          f"domain '{meta.get('domain')}' != 'meta'")
    check(f"{name}-fm-language", meta.get("language") == "fr",
          f"language '{meta.get('language')}' != 'fr'")
    check(f"{name}-fm-asof", str(meta.get("as_of", "")) == "2026-09",
          f"as_of '{meta.get('as_of')}' != '2026-09'")

    spec = VAGUE5_SKILLS[name]
    check(f"{name}-fm-tags", spec["tags"] <= set(meta.get("tags") or []),
          f"tags attendus {sorted(spec['tags'])} absents de {meta.get('tags')}")
    check(f"{name}-fm-related", spec["related"] <= set(meta.get("related_skills") or []),
          f"related_skills attendus {sorted(spec['related'])} absents de {meta.get('related_skills')}")


# === T3 : Sections obligatoires ===
def test_required_sections(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    if not skill_md.exists():
        check(f"{name}-sections", False, "skill n'existe pas")
        return
    content = read_skill(name)
    end = content.find("\n---", 3)
    body = content[end + 4:] if end != -1 else content

    for section in REQUIRED_SECTIONS:
        check(f"{name}-section-{section}", section in body,
              f"section manquante: {section}")


# === T4 : related_skills qui résolvent ===
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
def test_domain_content(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    if not skill_md.exists():
        check(f"{name}-content", False, "skill n'existe pas")
        return
    content = read_skill(name)
    missing = [kw for kw in VAGUE5_SKILLS[name]["content"] if kw not in content]
    check(f"{name}-content", not missing,
          f"contenu métier manquant: {missing}")


# === T6 : L'interview couvre les 8 questions d'onboarding ===
def test_interview_questions(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    if not skill_md.exists():
        check(f"{name}-interview", False, "skill n'existe pas")
        return
    content = read_skill(name).lower()
    missing = [kw for kw in VAGUE5_SKILLS[name]["interview"] if kw not in content]
    check(f"{name}-interview", not missing,
          f"questions d'interview manquantes: {missing}")


# === T7 : Règle « le profil ne va jamais dans le repo » ===
def test_profile_stays_out_of_repo(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    if not skill_md.exists():
        check(f"{name}-profil-repo", False, "skill n'existe pas")
        return
    content = read_skill(name).lower()
    # La règle doit être explicite : jamais + (commit ou repo)
    has_rule = re.search(r"jamais.{0,80}(commit|repo)|(commit|repo).{0,80}jamais",
                         content, re.DOTALL)
    check(f"{name}-profil-repo", bool(has_rule),
          "règle « profil jamais commité / hors du repo » absente ou trop vague")


# === T8 : Handoff avec phrase prête à copier ===
def test_handoff_copy_paste(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    if not skill_md.exists():
        check(f"{name}-handoff", False, "skill n'existe pas")
        return
    content = read_skill(name).lower()
    has_phrase = re.search(r"(pr[êe]te?s?\s+[àa]\s+copier|dis\s*[:«])", content)
    check(f"{name}-handoff", bool(has_phrase),
          "pas de phrase de handoff prête à copier (format « Dis : « … » »)")


# === T9 : Passe le validateur du repo ===
def test_skill_passes_validator(name: str):
    skill_dir = SKILLS_DIR / name
    if not (skill_dir / "SKILL.md").exists():
        check(f"{name}-validator", False, "skill n'existe pas")
        return
    errors = validate_skills.validate_skill(skill_dir)
    check(f"{name}-validator", len(errors) == 0,
          f"erreurs: {errors[:3]}")


# === T10 : Passe le scanner de sécurité (aucun finding BLOCK) ===
def test_skill_passes_security_scan(name: str):
    skill_md = SKILLS_DIR / name / "SKILL.md"
    if not skill_md.exists():
        check(f"{name}-security", False, "skill n'existe pas")
        return
    findings = security_scan.scan_file(skill_md)
    blocks = [f for f in findings if f[0] == "BLOCK"]
    check(f"{name}-security", not blocks,
          f"findings bloquants: {blocks[:3]}")


# === Exécution ===
if __name__ == "__main__":
    for skill_name in VAGUE5_SKILLS:
        test_skill_exists(skill_name)
        test_frontmatter(skill_name)
        test_required_sections(skill_name)
        test_related_skills_resolve(skill_name)
        test_domain_content(skill_name)
        test_interview_questions(skill_name)
        test_profile_stays_out_of_repo(skill_name)
        test_handoff_copy_paste(skill_name)
        test_skill_passes_validator(skill_name)
        test_skill_passes_security_scan(skill_name)

    if FAILURES:
        print(f"RED — {len(FAILURES)} échec(s) (attendu en TDD) :")
        for f in FAILURES:
            print(f"  {f}")
        sys.exit(1)
    print(f"GREEN — tous les tests vague 5 passent ({', '.join(VAGUE5_SKILLS)})")
    sys.exit(0)
