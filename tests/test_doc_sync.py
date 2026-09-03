#!/usr/bin/env python3
"""Auto-test de check_doc_sync.py — vérifie que le script détecte les divergences
entre les chiffres du README.md (nombre de skills, liens related_skills, tableau
des domaines) et la réalité du repo, sur des fixtures temporaires."""
import contextlib
import io
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_doc_sync  # noqa: E402

FAILURES = []

SKILL_TEMPLATE = """---
name: {name}
description: "Utilisez quand on teste."
version: 0.1.0
license: MIT
metadata:
  tags: [test]
  related_skills: [{related}]
  domain: finance
  language: fr
  as_of: "2026-07"
---

# {name}

## Overview

Skill de test.

## When to Use

- test
"""

README_TEMPLATE = """# Fake repo

**{nb_skills} skills** pour tester.

```bash
python scripts/validate_skills.py      # {nb_skills}/{nb_skills} skills valides
python scripts/check_related_links.py  # {nb_liens} liens, 0 morts
```

## Domaines couverts

| Domaine | Skills |
|---|---|
| Finance | {tableau} |
"""


def make_skill(root: Path, name: str, related: str = "") -> Path:
    d = root / ".agents" / "skills" / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(
        SKILL_TEMPLATE.format(name=name, related=related), encoding="utf-8")
    return d


def make_repo(root: Path, nb_skills: int = 2, nb_liens: int = 1,
              tableau: str = "`skill-a`, `skill-b`") -> Path:
    make_skill(root, "skill-a", related="skill-b")
    make_skill(root, "skill-b")
    (root / "README.md").write_text(
        README_TEMPLATE.format(nb_skills=nb_skills, nb_liens=nb_liens, tableau=tableau),
        encoding="utf-8")
    return root


def run(root: Path) -> tuple[int, str]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = check_doc_sync.main(["--root", str(root)])
    return code, buf.getvalue()


def check(label: str, cond: bool, detail: str = ""):
    if not cond:
        FAILURES.append(f"FAIL {label}: {detail}")


def fresh_repo(nb_skills: int = 2, nb_liens: int = 1,
               tableau: str = "`skill-a`, `skill-b`"):
    tmp = tempfile.TemporaryDirectory()
    make_repo(Path(tmp.name), nb_skills, nb_liens, tableau)
    return tmp


# 1. README synchronisé → exit 0
with fresh_repo() as tmp:
    code, out = run(Path(tmp))
    check("sync-exit0", code == 0, f"exit={code}, out={out!r}")

# 2. Mauvais nombre de skills → exit 1 avec motif/valeurs explicites
with fresh_repo(nb_skills=3) as tmp:
    code, out = run(Path(tmp))
    check("skills-exit1", code == 1, f"exit={code}")
    check("skills-message", "skills" in out and "3" in out and "2" in out,
          f"message incomplet: {out!r}")

# 3. Mauvais nombre de liens → exit 1
with fresh_repo(nb_liens=53) as tmp:
    code, out = run(Path(tmp))
    check("liens-exit1", code == 1, f"exit={code}")
    check("liens-message", "liens" in out and "53" in out and "1" in out,
          f"message incomplet: {out!r}")

# 4. Skill réel absent du tableau des domaines → exit 1
with fresh_repo(tableau="`skill-a`") as tmp:
    code, out = run(Path(tmp))
    check("tableau-manquant-exit1", code == 1, f"exit={code}")
    check("tableau-manquant-message", "skill-b" in out, f"message: {out!r}")

# 5. Skill inconnu dans le tableau → exit 1
with fresh_repo(tableau="`skill-a`, `skill-b`, `skill-fantome`") as tmp:
    code, out = run(Path(tmp))
    check("tableau-inconnu-exit1", code == 1, f"exit={code}")
    check("tableau-inconnu-message", "skill-fantome" in out, f"message: {out!r}")

# 6. _template ne compte pas comme skill
with fresh_repo() as tmp:
    make_skill(Path(tmp), "_template")
    code, out = run(Path(tmp))
    check("template-ignore", code == 0, f"exit={code}, out={out!r}")


def git(root: Path, *args: str) -> int:
    import subprocess
    proc = subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, text=True)
    return proc.returncode


def repo_with_git(root: Path) -> None:
    import subprocess
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    # identité minimale : git add suffit (aucun commit requis pour ls-files)
    subprocess.run(["git", "config", "core.autocrlf", "false"], cwd=root, check=True)


# 7. Copie harness trackée dans git → exit 1 avec le chemin du fichier
with fresh_repo() as tmp:
    root = Path(tmp)
    repo_with_git(root)
    stale = root / ".claude" / "skills" / "skill-a" / "SKILL.md"
    stale.parent.mkdir(parents=True)
    stale.write_text("copie figée", encoding="utf-8")
    git(root, "add", ".claude/skills/skill-a/SKILL.md")
    code, out = run(root)
    check("harness-tracke-exit1", code == 1, f"exit={code}, out={out!r}")
    check("harness-tracke-message", "harness" in out.lower() and ".claude" in out,
          f"message incomplet: {out!r}")

# 8. Copie harness présente sur disque mais NON trackée → exit 0
with fresh_repo() as tmp:
    root = Path(tmp)
    repo_with_git(root)
    stale = root / ".cursor" / "skills" / "skill-a" / "SKILL.md"
    stale.parent.mkdir(parents=True)
    stale.write_text("copie locale non suivie", encoding="utf-8")
    code, out = run(root)
    check("harness-non-tracke-exit0", code == 0, f"exit={code}, out={out!r}")

# 9. Pas de repo git (fixture sans .git) → pas de faux positif
with fresh_repo() as tmp:
    code, out = run(Path(tmp))
    check("sans-git-exit0", code == 0, f"exit={code}, out={out!r}")

if FAILURES:
    print("ÉCHECS:")
    for f in FAILURES:
        print(f"  {f}")
    sys.exit(1)
print("OK: auto-tests check_doc_sync passent")
