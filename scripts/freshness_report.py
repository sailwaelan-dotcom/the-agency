#!/usr/bin/env python3
"""
Rapport de fraîcheur des skills — The Agency.
Parse metadata.as_of ("YYYY-MM") de chaque skill et calcule l'âge en mois par
rapport à aujourd'hui. Rapport trié du plus ancien au plus récent.

Usage: python scripts/freshness_report.py [--root DIR] [--today YYYY-MM]
                                          [--markdown] [--fail-after-months N]
--fail-after-months N (défaut 6) : exit 1 si au moins un skill dépasse N mois.
Un skill sans as_of est signalé (statut SANS DATE) et compte comme dépassé.
Exit 0 si tous les skills sont frais.
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

AS_OF_RE = re.compile(r"^(\d{4})-(\d{2})$")


def parse_as_of(skill_md: Path) -> str | None:
    """Extrait metadata.as_of d'un SKILL.md. None si absent ou illisible."""
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
    as_of = meta.get("as_of")
    return str(as_of) if as_of else None


def age_in_months(as_of: str, ref: tuple[int, int]) -> int | None:
    """Âge en mois entre as_of ("YYYY-MM") et le mois de référence. None si invalide."""
    m = AS_OF_RE.match(as_of)
    if not m:
        return None
    return (ref[0] - int(m.group(1))) * 12 + (ref[1] - int(m.group(2)))


def collect(root: Path, ref: tuple[int, int], fail_after: int) -> list[dict]:
    """Retourne [{name, as_of, age, status}] trié du plus ancien au plus récent.

    Les skills sans date (ou date invalide) passent en tête : ils comptent
    comme les plus anciens.
    """
    skills_dir = root / ".agents" / "skills"
    entries = []
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        name = skill_md.parent.name
        if name.startswith("_"):
            continue
        as_of = parse_as_of(skill_md)
        age = age_in_months(as_of, ref) if as_of else None
        if age is None:
            status = "SANS DATE"
        elif age > fail_after:
            status = "À REVOIR"
        else:
            status = "OK"
        entries.append({"name": name, "as_of": as_of or "—", "age": age, "status": status})
    # Tri : sans date d'abord, puis âge décroissant
    entries.sort(key=lambda e: (e["age"] is not None, -(e["age"] or 0), e["name"]))
    return entries


def render_text(entries: list[dict], ref_label: str) -> str:
    lines = [f"Rapport de fraîcheur des skills (référence: {ref_label})", ""]
    for e in entries:
        age = f"âge={e['age']} mois" if e["age"] is not None else "aucun as_of"
        lines.append(f"  {e['status']:<10} {e['name']:<28} as_of={e['as_of']:<8} {age}")
    return "\n".join(lines)


def render_markdown(entries: list[dict], ref_label: str) -> str:
    lines = [
        f"# Rapport de fraîcheur des skills (référence: {ref_label})",
        "",
        "| Skill | as_of | Âge (mois) | Statut |",
        "|---|---|---|---|",
    ]
    for e in entries:
        age = str(e["age"]) if e["age"] is not None else "—"
        lines.append(f"| {e['name']} | {e['as_of']} | {age} | {e['status']} |")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rapport de fraîcheur des skills (as_of).")
    parser.add_argument("--root", default=str(REPO_ROOT), help="racine du repo (défaut: repo)")
    parser.add_argument("--today", default=date.today().strftime("%Y-%m"),
                        help="mois de référence YYYY-MM (tests déterministes)")
    parser.add_argument("--markdown", action="store_true", help="sortie en tableau markdown")
    parser.add_argument("--fail-after-months", type=int, default=6,
                        help="seuil en mois au-delà duquel exit 1 (défaut: 6)")
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not (root / ".agents" / "skills").is_dir():
        print(f"ERREUR: {root / '.agents' / 'skills'} introuvable", file=sys.stderr)
        return 1

    m = AS_OF_RE.match(args.today)
    if not m:
        print(f"ERREUR: --today '{args.today}' invalide (format YYYY-MM)", file=sys.stderr)
        return 1
    ref = (int(m.group(1)), int(m.group(2)))

    entries = collect(root, ref, args.fail_after_months)
    render = render_markdown if args.markdown else render_text
    print(render(entries, args.today))

    stale = [e for e in entries if e["status"] != "OK"]
    if stale:
        names = ", ".join(e["name"] for e in stale)
        print(f"\nÉCHEC: {len(stale)} skill(s) dépassent {args.fail_after_months} mois "
              f"ou n'ont pas de as_of : {names}")
        return 1
    print(f"\nOK: {len(entries)} skill(s) frais (seuil: {args.fail_after_months} mois)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
