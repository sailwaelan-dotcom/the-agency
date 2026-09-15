#!/usr/bin/env python3
"""
Validateur de skills — The Agency.
Vérifie que chaque .agents/skills/<name>/SKILL.md respecte la spec agentskills.io
ET les règles de portabilité harness-agnostic du repo.

Usage: python scripts/validate_skills.py
Exit 0 si tous les skills sont valides, 1 sinon.
"""
import os
import re
import sys
import yaml
from pathlib import Path

from skill_meta import split_list

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"

# --- Règles de frontmatter ---
# Spec agentskills.io : name, description, license, compatibility, metadata, allowed-tools.
# Le repo exige `license` et interdit `allowed-tools` (portabilité, voir FORBIDDEN_HARNESS_FIELDS).
REQUIRED_FIELDS = {"name", "description", "license"}
ALLOWED_TOP_FIELDS = REQUIRED_FIELDS | {"compatibility", "metadata"}
# Hors spec en top-level : à placer dans metadata (message de migration dédié)
MOVED_TO_METADATA = {"version", "author"}
# metadata = table de chaînes (spec) ; listes en chaîne « a, b, c » (voir skill_meta.split_list)
REQUIRED_METADATA_FIELDS = {"version", "tags"}
ALLOWED_METADATA_FIELDS = {"version", "author", "tags", "related_skills", "as_of", "domain", "language"}
LIST_METADATA_FIELDS = ("tags", "related_skills")
# Champs Claude-only / harness-spécifiques → INTERDITS en top-level (casse la promesse agnostic)
FORBIDDEN_HARNESS_FIELDS = {
    "allowed-tools", "disallowed-tools", "hooks", "model", "effort", "context",
    "agent", "shell", "disable-model-invocation", "user-invocable", "argument-hint",
    "paths", "mcp",
}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_DESC = 1024
MAX_NAME = 64
MAX_FILE = 100_000  # chars
WARN_FILE = 25_000

# Sections obligatoires pour être un skill "deep" utilisable
REQUIRED_SECTIONS = ["## Overview", "## When to Use", "## Questions à poser"]
RECOMMENDED_SECTIONS = ["## Common Pitfalls", "## Verification Checklist"]

# Disclaimer obligatoire si tags réglementaires
REGULATED_TAGS = {"finance", "tax", "legal", "compliance", "accounting", "fiscal", "social"}
DISCLAIMER_RE = re.compile(r"Disclaimer.{0,400}(comptable|avocat|expert-comptable|agréé)", re.I | re.S)


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_dir.name}: SKILL.md manquant"]

    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception as e:
        return [f"{skill_dir.name}: lecture impossible: {e}"]

    # --- Taille ---
    if len(content) > MAX_FILE:
        errors.append(f"{skill_dir.name}: {len(content)} chars > {MAX_FILE} max")
    elif len(content) > WARN_FILE:
        print(f"  WARN {skill_dir.name}: {len(content)} chars (envisager references/)", file=sys.stderr)

    # --- Frontmatter ---
    if not content.startswith("---"):
        errors.append(f"{skill_dir.name}: frontmatter doit commencer par '---' au byte 0")
        return errors
    end = content.find("\n---", 3)
    if end == -1:
        errors.append(f"{skill_dir.name}: frontmatter non fermé ('\\n---' manquant)")
        return errors

    fm_raw = content[3:end].strip()
    try:
        fm = yaml.safe_load(fm_raw)
    except yaml.YAMLError as e:
        errors.append(f"{skill_dir.name}: YAML frontmatter invalide: {e}")
        return errors
    if not isinstance(fm, dict):
        errors.append(f"{skill_dir.name}: frontmatter n'est pas un mapping YAML")
        return errors

    # --- Champs requis ---
    for field in REQUIRED_FIELDS:
        if field not in fm:
            errors.append(f"{skill_dir.name}: champ requis manquant: '{field}'")

    # --- Champs interdits (harness-specific) ---
    for field in fm:
        if field in FORBIDDEN_HARNESS_FIELDS:
            errors.append(
                f"{skill_dir.name}: champ non-portable '{field}' interdit en top-level "
                f"(Claude/harness-specific → casse l'agnosticité)"
            )
        elif field in MOVED_TO_METADATA:
            errors.append(
                f"{skill_dir.name}: champ '{field}' hors spec agentskills.io en top-level "
                f"→ le déplacer dans metadata.{field} (valeur chaîne)"
            )
        elif field not in ALLOWED_TOP_FIELDS:
            errors.append(f"{skill_dir.name}: champ inconnu '{field}' (whitelist: {sorted(ALLOWED_TOP_FIELDS)})")

    # --- name ---
    name = fm.get("name", "")
    if name:
        if len(name) > MAX_NAME:
            errors.append(f"{skill_dir.name}: name '{name}' > {MAX_NAME} chars")
        if not NAME_RE.match(name):
            errors.append(f"{skill_dir.name}: name '{name}' invalide (regex: {NAME_RE.pattern})")
        if name != skill_dir.name:
            errors.append(f"{skill_dir.name}: name '{name}' != dossier '{skill_dir.name}'")

    # --- description ---
    desc = fm.get("description", "")
    if desc:
        if len(desc) > MAX_DESC:
            errors.append(f"{skill_dir.name}: description {len(desc)} chars > {MAX_DESC}")
        # trigger-focused : doit contenir un marqueur de déclenchement
        if not re.search(r"(use when|utilisez|utiliser|quand|dès que|lors de|trigger)", desc, re.I):
            errors.append(
                f"{skill_dir.name}: description doit être trigger-focused "
                f"(commencer par 'Use when...' ou 'Utilisez quand...')"
            )

    # --- metadata : table de chaînes (spec agentskills.io) ---
    meta = fm.get("metadata")
    if meta is None:
        meta = {}
    elif not isinstance(meta, dict):
        errors.append(f"{skill_dir.name}: metadata doit être un mapping")
        meta = {}
    for k in sorted(REQUIRED_METADATA_FIELDS - set(meta)):
        errors.append(f"{skill_dir.name}: champ requis manquant: 'metadata.{k}'")
    for k, v in meta.items():
        if k not in ALLOWED_METADATA_FIELDS:
            errors.append(f"{skill_dir.name}: metadata.{k} inconnu (whitelist: {sorted(ALLOWED_METADATA_FIELDS)})")
        elif not isinstance(v, str):
            conseil = ("écrire la liste en chaîne « a, b, c »" if isinstance(v, list)
                       else "mettre la valeur entre guillemets")
            errors.append(f"{skill_dir.name}: metadata.{k} doit être une chaîne (spec agentskills.io) — {conseil}")
    if isinstance(meta.get("tags"), str) and not split_list(meta["tags"]):
        errors.append(f"{skill_dir.name}: metadata.tags doit être une chaîne non vide")
    for k in LIST_METADATA_FIELDS:
        if isinstance(meta.get(k), str):
            invalides = [item for item in split_list(meta[k]) if not NAME_RE.match(item)]
            if invalides:
                errors.append(
                    f"{skill_dir.name}: metadata.{k} : éléments invalides {invalides} "
                    f"(format « a, b, c » ; minuscules, chiffres, tirets)"
                )

    # --- Body ---
    body = content[end + 4 :].strip()
    if not body:
        errors.append(f"{skill_dir.name}: body vide après frontmatter")
        return errors

    for section in REQUIRED_SECTIONS:
        if section not in body:
            errors.append(f"{skill_dir.name}: section obligatoire manquante: '{section}'")
    for section in RECOMMENDED_SECTIONS:
        if section not in body:
            print(f"  WARN {skill_dir.name}: section recommandée absente: '{section}'", file=sys.stderr)

    # --- Questionnement explicite : la section doit contenir au moins une vraie question ---
    q_match = re.search(r"^## Questions à poser\s*$", body, re.M)
    if q_match:
        rest = body[q_match.end():]
        next_sec = re.search(r"^## ", rest, re.M)
        q_body = rest[: next_sec.start()] if next_sec else rest
        if "?" not in q_body:
            errors.append(
                f"{skill_dir.name}: section '## Questions à poser' sans question "
                f"(lister les questions à poser en une salve, chacune terminée par '?')"
            )

    # --- Disclaimer si réglementaire ---
    tags = set(split_list(meta.get("tags")))
    if tags & REGULATED_TAGS and not DISCLAIMER_RE.search(body):
        errors.append(
            f"{skill_dir.name}: tag réglementaire {sorted(tags & REGULATED_TAGS)} "
            f"mais bloc Disclaimer (comptable/avocat/expert-comptable) absent"
        )

    # --- as_of si contenu daté ---
    if re.search(r"(taux|TVA|cotisation|subside|montant|seuil|plafond|€)\s*\d", body, re.I):
        if "as_of" not in str(meta) and "as_of" not in body and not re.search(r"(à jour|as of|202[4-9])", body):
            print(f"  WARN {skill_dir.name}: contenu daté détecté sans marqueur as_of", file=sys.stderr)

    return errors


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"ERREUR: {SKILLS_DIR} introuvable", file=sys.stderr)
        return 1

    skill_dirs = sorted(
        d for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith("_")
    )
    if not skill_dirs:
        print("Aucun skill trouvé (hors _template).")
        return 0

    print(f"Validation de {len(skill_dirs)} skill(s)...\n")
    total_errors = 0
    for sd in skill_dirs:
        errs = validate_skill(sd)
        if errs:
            total_errors += len(errs)
            for e in errs:
                print(f"  ✗ {e}")
        else:
            print(f"  ✓ {sd.name}")

    print(f"\n{'=' * 50}")
    if total_errors:
        print(f"ÉCHEC: {total_errors} erreur(s)")
        return 1
    print(f"OK: {len(skill_dirs)} skill(s) valides")
    return 0


if __name__ == "__main__":
    sys.exit(main())
