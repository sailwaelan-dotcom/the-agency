#!/usr/bin/env python3
"""
Vérificateur de liens related_skills — The Agency.
Vérifie que chaque skill listé dans metadata.related_skills d'un SKILL.md
correspond à un dossier existant dans .agents/skills/.
Usage: python scripts/check_related_links.py
Exit 0 si tous les liens résolvent, 1 avec la liste des liens morts sinon.
"""
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"ERREUR: {SKILLS_DIR} introuvable", file=sys.stderr)
        return 1

    existing = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith("_")}
    dead: list[str] = []
    checked = 0

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
            checked += 1
            if rel not in existing:
                dead.append(f"{skill_name} -> {rel}")

    print(f"Vérifié: {checked} lien(s) related_skills dans {len(existing)} skills")
    if dead:
        print(f"\nLIENS MORTS ({len(dead)}):")
        for d in dead:
            print(f"  ✗ {d}")
        return 1
    print("OK: tous les liens related_skills résolvent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
