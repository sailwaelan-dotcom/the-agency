#!/usr/bin/env python3
"""
Vérificateur de synchronisation README ↔ repo — The Agency.
Vérifie que les chiffres du README.md racine correspondent à la réalité :
- « N skills » / « N/N skills valides » ↔ nombre réel de dossiers skills (hors _template)
- « N liens » ↔ nombre réel de liens related_skills (même calcul que check_related_links.py)
- tableau « | Domaine | Skills | » ↔ ensemble réel des skills
- copies harness (.claude/.cursor/.hermes/.kilocode) ↔ aucun fichier tracké par git

Usage: python scripts/check_doc_sync.py [--root DIR]
Exit 0 si synchronisé, 1 en listant chaque divergence (motif, valeur README, valeur réelle).
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

# Dossiers de copies harness : créés après le clone par adapters/link-skills,
# jamais commités (.gitignore). Un fichier tracké ici = copie figée en double
# de la source canonique .agents/skills/.
HARNESS_DIRS = (".claude/skills", ".cursor/skills", ".hermes/skills",
                ".kilocode/skills")

# Motifs tolérants : « 18 skills », « 18/18 skills valides », « 53 liens »
SKILLS_RATIO_RE = re.compile(r"(\d+)\s*/\s*(\d+)\s*skills\b")
SKILLS_COUNT_RE = re.compile(r"(\d+)\s+skills\b")
LINKS_COUNT_RE = re.compile(r"(\d+)\s+liens\b")
BACKTICK_RE = re.compile(r"`([a-z0-9][a-z0-9-]*)`")


def real_skills(root: Path) -> set[str]:
    """Ensemble des noms de skills réels (dossiers hors _template/_...)."""
    skills_dir = root / ".agents" / "skills"
    if not skills_dir.is_dir():
        return set()
    return {d.name for d in skills_dir.iterdir()
            if d.is_dir() and not d.name.startswith("_")}


def count_related_links(root: Path) -> int:
    """Nombre total de liens related_skills — même calcul que check_related_links.py."""
    total = 0
    skills_dir = root / ".agents" / "skills"
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        if skill_md.parent.name.startswith("_"):
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
        total += len(meta.get("related_skills") or [])
    return total


def harness_tracked_files(root: Path) -> list[str]:
    """Fichiers de copies harness trackés par git (attendu : aucun).

    Retourne [] si git est absent ou si root n'est pas un dépôt — le check
    ne doit jamais créer de faux positif hors d'un contexte git réel.
    """
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--", *HARNESS_DIRS],
            capture_output=True, text=True)
    except FileNotFoundError:
        return []
    if proc.returncode != 0:
        return []
    return [line for line in proc.stdout.splitlines() if line.strip()]


def check_readme(root: Path) -> list[str]:
    """Retourne la liste des divergences entre README.md et la réalité du repo."""
    readme = root / "README.md"
    if not readme.is_file():
        return ["README.md: absent à la racine"]
    text = readme.read_text(encoding="utf-8")
    divergences: list[str] = []

    skills = real_skills(root)
    nb_skills = len(skills)
    nb_links = count_related_links(root)

    # --- Motif « N/N skills (valides) » : les deux nombres doivent égaler le réel ---
    ratio_spans = []
    for m in SKILLS_RATIO_RE.finditer(text):
        ratio_spans.append(m.span())
        a, b = int(m.group(1)), int(m.group(2))
        if a != b:
            divergences.append(
                f"[motif 'N/N skills']: README dit {a}/{b} (incohérent), réel = {nb_skills}")
        elif a != nb_skills:
            divergences.append(
                f"[motif 'N/N skills']: README dit {a}/{b}, réel = {nb_skills} skills")

    # --- Motif « N skills » (hors ratios déjà traités) ---
    def in_ratio(span: tuple[int, int]) -> bool:
        return any(s <= span[0] and span[1] <= e for s, e in ratio_spans)

    for m in SKILLS_COUNT_RE.finditer(text):
        if in_ratio(m.span()):
            continue
        n = int(m.group(1))
        if n != nb_skills:
            divergences.append(
                f"[motif 'N skills']: README dit {n}, réel = {nb_skills} skills")

    # --- Motif « N liens » ---
    for m in LINKS_COUNT_RE.finditer(text):
        n = int(m.group(1))
        if n != nb_links:
            divergences.append(
                f"[motif 'N liens']: README dit {n}, réel = {nb_links} liens related_skills")

    # --- Tableau « | Domaine | Skills | » : ensemble des skills listés ↔ réel ---
    lines = text.splitlines()
    in_table = False
    listed: set[str] = set()
    for line in lines:
        if re.match(r"^\s*\|.*[Dd]omaine.*\|.*[Ss]kills.*\|", line):
            in_table = True
            continue
        if in_table:
            if not line.strip().startswith("|"):
                in_table = False
                continue
            if re.match(r"^\s*\|[\s:-]+\|", line):  # ligne séparatrice |---|
                continue
            listed.update(BACKTICK_RE.findall(line))
    if listed or in_table:
        missing = sorted(skills - listed)
        unknown = sorted(listed - skills)
        if missing:
            divergences.append(
                f"[tableau des domaines]: skills réels absents du README: {', '.join(missing)}")
        if unknown:
            divergences.append(
                f"[tableau des domaines]: skills listés inexistants: {', '.join(unknown)}")

    # --- Copies harness trackées par git (attendu : aucune) ---
    tracked = harness_tracked_files(root)
    if tracked:
        echantillon = ", ".join(tracked[:3])
        divergences.append(
            f"[copies harness]: {len(tracked)} fichier(s) tracké(s) sous "
            f"{HARNESS_DIRS[0]}/{HARNESS_DIRS[1]}/… (gitignorés attendus) — "
            f"ex: {echantillon} — corriger avec: git rm -r --cached .claude .cursor .hermes .kilocode")

    return divergences


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Vérifie que les chiffres du README.md correspondent au repo.")
    parser.add_argument("--root", default=str(REPO_ROOT), help="racine du repo (défaut: repo)")
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not (root / ".agents" / "skills").is_dir():
        print(f"ERREUR: {root / '.agents' / 'skills'} introuvable", file=sys.stderr)
        return 1

    divergences = check_readme(root)
    nb_skills = len(real_skills(root))
    nb_links = count_related_links(root)
    print(f"Vérifié: README.md ↔ {nb_skills} skills, {nb_links} liens related_skills")
    if divergences:
        print(f"\nDIVERGENCES ({len(divergences)}):")
        for d in divergences:
            print(f"  ✗ {d}")
        return 1
    print("OK: README.md synchronisé avec le repo")
    return 0


if __name__ == "__main__":
    sys.exit(main())
