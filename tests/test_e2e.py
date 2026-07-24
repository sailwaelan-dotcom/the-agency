#!/usr/bin/env python3
"""
E2E Test — The Agency
Test end-to-end du workflow de contribution :
1. Créer un skill de test temporaire
2. Le valider (validateur)
3. Le scanner (security scan)
4. Vérifier les liens (related_links)
5. Vérifier l'activation (description trigger-focused)
6. Nettoyer

Ce test simule le parcours complet d'un contributeur.
"""
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import validate_skills  # noqa: E402
import security_scan  # noqa: E402
import check_related_links  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"

FAILURES = []


def check(label: str, condition: bool, detail: str = ""):
    if not condition:
        FAILURES.append(f"FAIL {label}: {detail}")


def test_e2e_workflow():
    """Test complet du workflow de contribution."""

    # === 1. Créer un skill de test temporaire ===
    test_skill_name = "test-e2e-temp"
    test_skill_dir = SKILLS_DIR / test_skill_name
    test_skill_md = test_skill_dir / "SKILL.md"

    # Nettoyer si existe déjà
    if test_skill_dir.exists():
        shutil.rmtree(test_skill_dir)

    # Créer le skill de test
    test_skill_dir.mkdir(parents=True, exist_ok=True)
    test_content = """---
name: test-e2e-temp
description: "Utilisez quand vous avez besoin de tester le workflow E2E de The Agency. Ce skill est temporaire et sera supprimé après le test."
version: 0.1.0
license: MIT
author: Test
metadata:
  tags: [test, e2e]
  related_skills: [be-company-setup]
  domain: admin
  language: fr
  as_of: "2026-07"
---

# Test E2E — skill temporaire

## Overview
Ce skill est un test end-to-end du workflow de contribution. Il sera supprimé après le test.

## When to Use
- Test E2E uniquement

## Workflow
1. Créer le skill
2. Valider
3. Scanner
4. Vérifier les liens
5. Vérifier l'activation
6. Nettoyer

## Common Pitfalls
1. Oublier de supprimer le skill de test après le test

## Verification Checklist
- [ ] Skill créé
- [ ] Validation passée
- [ ] Scan passé
- [ ] Liens vérifiés
- [ ] Activation vérifiée
- [ ] Nettoyage effectué

> ⚠️ **Disclaimer** : Ceci est un test. Aucune donnée réelle n'est utilisée.
"""
    test_skill_md.write_text(test_content, encoding="utf-8")
    check("e2e-create", test_skill_md.exists(),
          "skill de test non créé")

    # === 2. Valider le skill ===
    errors = validate_skills.validate_skill(test_skill_dir)
    check("e2e-validate", len(errors) == 0,
          f"erreurs de validation: {errors}")

    # === 3. Scanner le skill ===
    findings = security_scan.scan_file(test_skill_md)
    blocks = [f for f in findings if f[0] == "BLOCK"]
    check("e2e-scan", len(blocks) == 0,
          f"blocks de sécurité: {blocks}")

    # === 4. Vérifier les liens ===
    # Le skill référence be-company-setup qui existe
    existing = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith("_")}
    import yaml
    content = test_skill_md.read_text(encoding="utf-8")
    end = content.find("\n---", 3)
    fm = yaml.safe_load(content[3:end])
    related = fm.get("metadata", {}).get("related_skills", [])
    all_exist = all(r in existing for r in related)
    check("e2e-related-links", all_exist,
          f"liens morts: {[r for r in related if r not in existing]}")

    # === 5. Vérifier l'activation ===
    desc = fm.get("description", "")
    has_trigger = re.search(r"(utilisez|use when|quand|dès que)", desc, re.I)
    check("e2e-activation", bool(has_trigger),
          f"description non trigger-focused: {desc[:80]}")

    # === 6. Nettoyer ===
    shutil.rmtree(test_skill_dir)
    check("e2e-cleanup", not test_skill_dir.exists(),
          "skill de test non supprimé")


def test_e2e_full_gate():
    """Test de la gate complète (validate + scan + related_links)."""

    # Valider tous les skills
    errors = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("_"):
            continue
        skill_errors = validate_skills.validate_skill(skill_dir)
        errors.extend(skill_errors)
    check("e2e-gate-validate", len(errors) == 0,
          f"erreurs de validation: {len(errors)}")

    # Scanner tous les fichiers
    scanned = 0
    blocks = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in security_scan.SKIP_DIRS]
        for fn in filenames:
            if fn in security_scan.SKIP_FILES:
                continue
            ext = Path(fn).suffix.lower()
            if ext not in security_scan.SCAN_EXT:
                continue
            fpath = Path(dirpath) / fn
            scanned += 1
            findings = security_scan.scan_file(fpath)
            blocks.extend([f for f in findings if f[0] == "BLOCK"])
    check("e2e-gate-scan", len(blocks) == 0,
          f"blocks de sécurité: {len(blocks)}")

    # Vérifier tous les liens
    existing = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith("_")}
    dead = []
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        skill_name = skill_md.parent.name
        if skill_name.startswith("_"):
            continue
        content = skill_md.read_text(encoding="utf-8")
        end = content.find("\n---", 3)
        if end == -1:
            continue
        try:
            fm = yaml.safe_load(content[3:end])
        except yaml.YAMLError:
            continue
        if not isinstance(fm, dict):
            continue
        meta = fm.get("metadata") or {}
        related = meta.get("related_skills") or []
        for rel in related:
            if rel not in existing:
                dead.append(f"{skill_name} -> {rel}")
    check("e2e-gate-related-links", len(dead) == 0,
          f"liens morts: {dead}")


def test_e2e_activation_quality():
    """Test de la qualité des descriptions (trigger-focused)."""

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("_"):
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        content = skill_md.read_text(encoding="utf-8")
        m = re.search(r'description:\s*"([^"]+)"', content)
        if not m:
            check(f"e2e-desc-{skill_dir.name}", False, "pas de description")
            continue
        desc = m.group(1)
        has_trigger = re.search(r"(utilisez|use when|quand|dès que)", desc, re.I)
        check(f"e2e-desc-{skill_dir.name}", bool(has_trigger),
              f"description non trigger-focused: {desc[:80]}")


# === Exécution ===
if __name__ == "__main__":
    print("=== E2E Test — Workflow de contribution ===")
    test_e2e_workflow()

    print("\n=== E2E Test — Gate complète ===")
    test_e2e_full_gate()

    print("\n=== E2E Test — Qualité des descriptions ===")
    test_e2e_activation_quality()

    total_tests = 5 + 3 + 18  # workflow + gate + descriptions
    if FAILURES:
        print(f"\nRED — {len(FAILURES)}/{total_tests} tests E2E échoués:")
        for f in FAILURES:
            print(f"  {f}")
        sys.exit(1)
    print(f"\nGREEN — {total_tests}/{total_tests} tests E2E passent")
    sys.exit(0)
