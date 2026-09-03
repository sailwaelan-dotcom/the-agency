#!/usr/bin/env python3
"""Auto-test de build_index.py — vérifie la génération de INDEX.md et catalog.json
sur des fixtures temporaires (faux skills dans un tmpdir), le groupement par domaine,
l'exclusion de _template et la détection de staleness par --check."""
import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build_index  # noqa: E402

FAILURES = []

SKILL_TEMPLATE = """---
name: {name}
description: "{desc}"
version: 0.1.0
license: MIT
metadata:
  tags: [{tags}]
  related_skills: [{related}]
  domain: {domain}
  language: fr
  as_of: "{as_of}"
---

# {name}

## Overview

Skill de test.

## When to Use

- test
"""


def make_skill(root: Path, name: str, desc: str = "Utilisez quand on teste.",
               tags: str = "test", related: str = "", domain: str = "finance",
               as_of: str = "2026-07") -> Path:
    d = root / ".agents" / "skills" / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(
        SKILL_TEMPLATE.format(name=name, desc=desc, tags=tags, related=related,
                              domain=domain, as_of=as_of),
        encoding="utf-8")
    return d


def run(root: Path, *args: str) -> tuple[int, str]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = build_index.main(["--root", str(root), *args])
    return code, buf.getvalue()


def check(label: str, cond: bool, detail: str = ""):
    if not cond:
        FAILURES.append(f"FAIL {label}: {detail}")


with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    make_skill(tmp, "skill-alpha", domain="finance", related="skill-beta")
    make_skill(tmp, "skill-beta", domain="veille")
    make_skill(tmp, "_template", domain="autre")  # doit être exclu

    # 1. Génération : exit 0, les deux fichiers existent
    code, _ = run(tmp, "--today", "2026-08-02")
    check("generation-exit0", code == 0, f"exit={code}")
    check("generation-index", (tmp / "INDEX.md").is_file(), "INDEX.md absent")
    check("generation-catalog", (tmp / "catalog.json").is_file(), "catalog.json absent")

    index = (tmp / "INDEX.md").read_text(encoding="utf-8")

    # 2. Contenu de l'en-tête : note d'avertissement + nombre de skills
    check("note-generation", "ne pas éditer" in index, "note absente")
    check("header-nombre", "2 skills" in index, "nombre de skills absent")
    check("header-date", "2026-08-02" in index, "date de génération absente")

    # 3. Groupement par domaine : sections triées, skills sous le bon domaine
    pos_finance = index.find("## finance")
    pos_veille = index.find("## veille")
    check("sections-domaines", pos_finance != -1 and pos_veille != -1,
          "sections domaines manquantes")
    check("tri-domaines", pos_finance < pos_veille, "domaines non triés alphabétiquement")
    check("lien-relatif",
          "[skill-alpha](.agents/skills/skill-alpha/SKILL.md)" in index,
          "lien relatif absent")
    check("skills-lies", "skill-beta" in index.split("## finance")[1].split("## veille")[0],
          "related_skills absent du tableau")

    # 4. _template exclu des deux sorties
    check("template-exclu-index", "_template" not in index, "_template présent dans INDEX.md")
    catalog = json.loads((tmp / "catalog.json").read_text(encoding="utf-8"))
    names = [s["name"] for s in catalog["skills"]]
    check("template-exclu-catalog", "_template" not in names, f"names={names}")
    check("catalog-count", len(names) == 2, f"names={names}")

    # 5. catalog.json : champs machine-readable complets
    alpha = next(s for s in catalog["skills"] if s["name"] == "skill-alpha")
    for field in ("name", "description", "domain", "tags", "related_skills", "as_of", "version"):
        check(f"catalog-champ-{field}", field in alpha, f"champ '{field}' absent")
    check("catalog-domain", alpha["domain"] == "finance", f"domain={alpha.get('domain')}")
    check("catalog-related", alpha["related_skills"] == ["skill-beta"],
          f"related={alpha.get('related_skills')}")

    # 6. --check : vert juste après génération
    code, _ = run(tmp, "--check")
    check("check-frais", code == 0, f"exit={code} sur fichiers frais")

    # 7. --check : détecte le staleness après modification d'un skill
    make_skill(tmp, "skill-alpha", domain="finance", related="skill-beta", as_of="2026-01")
    code, out = run(tmp, "--check")
    check("check-stale-exit1", code == 1, f"exit={code} après modification")
    check("check-stale-message", "INDEX.md" in out or "catalog.json" in out,
          f"message de divergence absent: {out!r}")
    # Restaurer pour la suite
    make_skill(tmp, "skill-alpha", domain="finance", related="skill-beta")
    run(tmp, "--today", "2026-08-02")

    # 8. Description raccourcie à ~120 caractères
    longue = "Utilisez quand " + "x" * 300
    make_skill(tmp, "skill-long", desc=longue, domain="finance")
    run(tmp, "--today", "2026-08-02")
    index = (tmp / "INDEX.md").read_text(encoding="utf-8")
    ligne = next(l for l in index.splitlines() if "skill-long" in l)
    cellule = ligne.split("|")[2].strip()
    check("desc-raccourcie", len(cellule) <= 121 and cellule.endswith("…"),
          f"cellule {len(cellule)} car.: {cellule[:60]!r}")

if FAILURES:
    print("ÉCHECS:")
    for f in FAILURES:
        print(f"  {f}")
    sys.exit(1)
print(f"OK: auto-tests build_index passent")
