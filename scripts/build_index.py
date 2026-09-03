#!/usr/bin/env python3
"""
Générateur d'index des skills — The Agency.
Scanne .agents/skills/<nom>/SKILL.md (hors _template), parse les frontmatters et génère :
- INDEX.md à la racine : catalogue en français groupé par domaine (lisible humain).
- catalog.json à la racine : catalogue machine-readable.

Usage: python scripts/build_index.py [--root DIR] [--today YYYY-MM-DD] [--check]
--check : n'écrit rien, exit 1 si INDEX.md ou catalog.json seraient différents (stale).
Exit 0 sinon.
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

MAX_TRIGGER = 120  # longueur max de la colonne « Déclencheur »
DATE_RE = re.compile(r"Généré le (\d{4}-\d{2}-\d{2})")


def parse_skill(skill_md: Path) -> dict | None:
    """Extrait les métadonnées d'un SKILL.md. Retourne None si illisible."""
    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception:
        return None
    if not content.startswith("---"):
        return None
    end = content.find("\n---", 3)
    if end == -1:
        return None
    try:
        fm = yaml.safe_load(content[3:end])
    except yaml.YAMLError:
        return None
    if not isinstance(fm, dict):
        return None
    meta = fm.get("metadata") or {}
    return {
        "name": fm.get("name", skill_md.parent.name),
        "description": fm.get("description", ""),
        "version": fm.get("version", ""),
        "domain": meta.get("domain", "autre"),
        "tags": meta.get("tags") or [],
        "related_skills": meta.get("related_skills") or [],
        "as_of": str(meta.get("as_of", "")),
    }


def scan_skills(root: Path) -> list[dict]:
    """Retourne les skills du repo (hors _template), triés par nom."""
    skills_dir = root / ".agents" / "skills"
    skills = []
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        if skill_md.parent.name.startswith("_"):
            continue
        info = parse_skill(skill_md)
        if info:
            skills.append(info)
    return sorted(skills, key=lambda s: s["name"])


def shorten(desc: str, max_len: int = MAX_TRIGGER) -> str:
    """Raccourcit une description à ~max_len caractères et l'échappe pour un tableau."""
    desc = " ".join(desc.split()).replace("|", "\\|")
    if len(desc) <= max_len:
        return desc
    return desc[: max_len - 1].rstrip() + "…"


def render_index(skills: list[dict], today: str) -> str:
    lines = [
        "# Index des skills — The Agency",
        "",
        "> Généré par scripts/build_index.py — ne pas éditer à la main.",
        f"> Généré le {today} — {len(skills)} skills.",
        "",
    ]
    domains = sorted({s["domain"] for s in skills})
    for domain in domains:
        lines.append(f"## {domain}")
        lines.append("")
        lines.append("| Skill | Déclencheur | as_of | Skills liés |")
        lines.append("|---|---|---|---|")
        for s in skills:
            if s["domain"] != domain:
                continue
            link = f"[{s['name']}](.agents/skills/{s['name']}/SKILL.md)"
            related = ", ".join(s["related_skills"]) or "—"
            lines.append(
                f"| {link} | {shorten(s['description'])} | {s['as_of'] or '—'} | {related} |"
            )
        lines.append("")
    return "\n".join(lines)


def render_catalog(skills: list[dict], today: str) -> str:
    catalog = {
        "generated_at": today,
        "generator": "scripts/build_index.py",
        "count": len(skills),
        "skills": [
            {
                "name": s["name"],
                "description": s["description"],
                "domain": s["domain"],
                "tags": s["tags"],
                "related_skills": s["related_skills"],
                "as_of": s["as_of"],
                "version": s["version"],
            }
            for s in skills
        ],
    }
    return json.dumps(catalog, ensure_ascii=False, indent=2) + "\n"


def existing_index_date(index_path: Path) -> str | None:
    """Extrait la date de génération d'un INDEX.md existant (comparaison stable)."""
    if not index_path.is_file():
        return None
    m = DATE_RE.search(index_path.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Génère INDEX.md et catalog.json des skills.")
    parser.add_argument("--root", default=str(REPO_ROOT), help="racine du repo (défaut: repo)")
    parser.add_argument("--today", default=date.today().isoformat(),
                        help="date de génération YYYY-MM-DD (tests déterministes)")
    parser.add_argument("--check", action="store_true",
                        help="n'écrit rien, exit 1 si les fichiers générés divergent")
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not (root / ".agents" / "skills").is_dir():
        print(f"ERREUR: {root / '.agents' / 'skills'} introuvable", file=sys.stderr)
        return 1

    skills = scan_skills(root)
    index_path = root / "INDEX.md"
    catalog_path = root / "catalog.json"

    if args.check:
        # Régénérer avec la date du fichier existant pour une comparaison stable
        ref_date = existing_index_date(index_path) or args.today
        expected = {
            index_path: render_index(skills, ref_date),
            catalog_path: render_catalog(skills, ref_date),
        }
        stale = []
        for path, content in expected.items():
            if not path.is_file():
                stale.append(f"{path.name}: absent")
            elif path.read_text(encoding="utf-8") != content:
                stale.append(f"{path.name}: contenu différent (stale)")
        if stale:
            print("DIVERGENCES détectées (relancer: python scripts/build_index.py) :")
            for s in stale:
                print(f"  ✗ {s}")
            return 1
        print(f"OK: INDEX.md et catalog.json à jour ({len(skills)} skills)")
        return 0

    index_path.write_text(render_index(skills, args.today), encoding="utf-8")
    catalog_path.write_text(render_catalog(skills, args.today), encoding="utf-8")
    print(f"Généré: INDEX.md + catalog.json ({len(skills)} skills)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
