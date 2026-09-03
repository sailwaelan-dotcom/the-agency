#!/usr/bin/env python3
"""Auto-test de freshness_report.py — vérifie le calcul d'âge des skills (as_of),
le tri du plus ancien au plus récent, le format markdown, le statut SANS DATE
et le seuil --fail-after-months sur des fixtures temporaires."""
import contextlib
import io
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import freshness_report  # noqa: E402

FAILURES = []

SKILL_TEMPLATE = """---
name: {name}
description: "Utilisez quand on teste."
version: 0.1.0
license: MIT
metadata:
  tags: [test]
  domain: finance
  language: fr
{as_of_line}---

# {name}

## Overview

Skill de test.

## When to Use

- test
"""


def make_skill(root: Path, name: str, as_of: str | None) -> Path:
    d = root / ".agents" / "skills" / name
    d.mkdir(parents=True, exist_ok=True)
    as_of_line = f'  as_of: "{as_of}"\n' if as_of else ""
    (d / "SKILL.md").write_text(
        SKILL_TEMPLATE.format(name=name, as_of_line=as_of_line), encoding="utf-8")
    return d


def run(root: Path, *args: str) -> tuple[int, str]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = freshness_report.main(["--root", str(root), "--today", "2026-08", *args])
    return code, buf.getvalue()


def check(label: str, cond: bool, detail: str = ""):
    if not cond:
        FAILURES.append(f"FAIL {label}: {detail}")


with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    make_skill(tmp, "skill-recent", "2026-07")   # 1 mois
    make_skill(tmp, "skill-limite", "2026-02")   # 6 mois = seuil par défaut, encore OK
    make_skill(tmp, "skill-vieux", "2025-01")    # 19 mois
    make_skill(tmp, "skill-sans-date", None)

    # 1. Un skill dépassé → exit 1
    code, out = run(tmp)
    check("depasse-exit1", code == 1, f"exit={code}")

    # 2. Tri du plus ancien au plus récent (SANS DATE en tête)
    positions = [out.find(n) for n in
                 ("skill-sans-date", "skill-vieux", "skill-limite", "skill-recent")]
    check("tri-ordre", all(p != -1 for p in positions) and positions == sorted(positions),
          f"positions={positions}")

    # 3. Statuts et âge en mois
    check("statut-sans-date", "SANS DATE" in out, "statut SANS DATE absent")
    check("statut-a-revoir", "À REVOIR" in out, "statut À REVOIR absent")
    check("statut-ok", "OK" in out, "statut OK absent")
    check("age-mois", "19" in out, "âge 19 mois absent")

    # 4. Seuil paramétrable : 24 mois → seul le sans-date fait échouer ;
    #    sans le skill sans date, exit 0
    (tmp / ".agents" / "skills" / "skill-sans-date" / "SKILL.md").write_text(
        SKILL_TEMPLATE.format(name="skill-sans-date", as_of_line='  as_of: "2026-06"\n'),
        encoding="utf-8")
    code, _ = run(tmp, "--fail-after-months", "24")
    check("seuil-24-exit0", code == 0, f"exit={code} avec seuil 24")
    code, _ = run(tmp, "--fail-after-months", "3")
    check("seuil-3-exit1", code == 1, f"exit={code} avec seuil 3")

    # 5. Format markdown : tableau avec colonnes attendues
    code, out = run(tmp, "--fail-after-months", "24", "--markdown")
    check("markdown-exit0", code == 0, f"exit={code}")
    check("markdown-entete", "| Skill |" in out and "as_of" in out,
          "en-tête du tableau absent")
    check("markdown-separateur", "|---" in out, "séparateur de tableau absent")
    check("markdown-statut", "À REVOIR" not in out or "skill-vieux" not in out,
          "skill-vieux encore marqué À REVOIR avec seuil 24")

    # 6. Tous frais → exit 0 et aucun À REVOIR
    make_skill(tmp, "skill-vieux", "2026-05")
    code, out = run(tmp)
    check("tous-frais-exit0", code == 0, f"exit={code}")
    check("tous-frais-clean", "À REVOIR" not in out, "À REVOIR présent alors que tout est frais")

if FAILURES:
    print("ÉCHECS:")
    for f in FAILURES:
        print(f"  {f}")
    sys.exit(1)
print("OK: auto-tests freshness_report passent")
