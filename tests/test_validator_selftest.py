#!/usr/bin/env python3
"""Auto-test du validateur de skills — vérifie que les règles critiques rejettent
les mauvais skills et acceptent un skill conforme."""
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import validate_skills  # noqa: E402

FAILURES = []

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "_template"
PILOT_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "be-invoicing-peppol"


def make_skill(base: Path, name: str, frontmatter_overrides: dict | None = None,
               body_append: str = "", body_replace: tuple[str, str] | None = None) -> Path:
    """Crée un skill de test en copiant le pilote puis en modifiant le frontmatter."""
    src = PILOT_DIR if PILOT_DIR.is_dir() else TEMPLATE_DIR
    dst = base / name
    shutil.copytree(src, dst)
    skill_md = dst / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8")

    if frontmatter_overrides:
        end = content.find("\n---", 3)
        fm_raw = content[3:end]
        body = content[end + 4 :]
        import yaml
        fm = yaml.safe_load(fm_raw)
        fm.update(frontmatter_overrides)
        new_fm = yaml.dump(fm, allow_unicode=True, sort_keys=False)
        content = f"---\n{new_fm}---\n{body}"
    if body_replace:
        content = content.replace(body_replace[0], body_replace[1])
    if body_append:
        content += body_append
    skill_md.write_text(content, encoding="utf-8")
    return dst


def check(label: str, skill_dir: Path, expect_valid: bool, expect_error_substr: str | None = None):
    errors = validate_skills.validate_skill(skill_dir)
    if expect_valid and errors:
        FAILURES.append(f"FAIL {label}: attendu valide, erreurs: {errors[:2]}")
    elif not expect_valid and not errors:
        FAILURES.append(f"FAIL {label}: attendu invalide, mais validé")
    elif expect_error_substr and errors:
        if not any(expect_error_substr in e for e in errors):
            FAILURES.append(f"FAIL {label}: erreur attendue '{expect_error_substr}' absente de {errors[:2]}")


with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)

    # 1. Copie du pilote → doit être valide
    valid = make_skill(tmp, "be-invoicing-peppol")
    check("pilote-copie", valid, expect_valid=True)

    # 2. Champ harness-spécifique interdit → rejeté
    bad_tools = make_skill(tmp, "bad-tools", frontmatter_overrides={"allowed-tools": "Bash"})
    check("allowed-tools-interdit", bad_tools, expect_valid=False, expect_error_substr="allowed-tools")

    # 3. name != dossier → rejeté
    bad_name = make_skill(tmp, "real-folder", frontmatter_overrides={"name": "other-name"})
    check("name-mismatch", bad_name, expect_valid=False, expect_error_substr="!= dossier")

    # 4. Description sans trigger → rejeté
    bad_desc = make_skill(tmp, "be-invoicing-peppol2", frontmatter_overrides={
        "name": "be-invoicing-peppol2",
        "description": "Aide pour la facturation belge.",
    })
    check("desc-sans-trigger", bad_desc, expect_valid=False, expect_error_substr="trigger")

    # 5. Tag finance sans disclaimer → rejeté
    no_disc = make_skill(tmp, "be-invoicing-peppol3",
                         frontmatter_overrides={"name": "be-invoicing-peppol3"},
                         body_replace=("> ⚠️ **Disclaimer**", "> **Note**"))
    check("disclaimer-manquant", no_disc, expect_valid=False, expect_error_substr="Disclaimer")

    # 6. Champ metadata inconnu → rejeté
    bad_meta = make_skill(tmp, "be-invoicing-peppol4", frontmatter_overrides={
        "name": "be-invoicing-peppol4",
        "metadata": {"tags": ["finance"], "evil_field": "x"},
    })
    check("metadata-inconnu", bad_meta, expect_valid=False, expect_error_substr="metadata")

    # 7. Section Overview manquante → rejeté
    no_ov = make_skill(tmp, "be-invoicing-peppol5",
                       frontmatter_overrides={"name": "be-invoicing-peppol5"},
                       body_replace=("## Overview", "## Résumé"))
    check("overview-manquant", no_ov, expect_valid=False, expect_error_substr="Overview")

if FAILURES:
    print("ÉCHECS:")
    for f in FAILURES:
        print(f"  {f}")
    sys.exit(1)
print("OK: 7/7 auto-tests du validateur passent")
