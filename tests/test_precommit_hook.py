#!/usr/bin/env python3
"""
Le hook pre-commit (.githooks/pre-commit) lance les gates avant chaque commit :
présent, exécutable pour Git, et qui bloque un secret réel.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HOOK = REPO_ROOT / ".githooks" / "pre-commit"


def test_hook_is_executable_in_git():
    out = subprocess.run(
        ["git", "ls-files", "-s", ".githooks/pre-commit"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    assert out.startswith("100755"), f"mode Git attendu 100755, obtenu : {out!r}"
    print("  ✓ test_hook_is_executable_in_git")


def test_hook_blocks_a_secret():
    sh = shutil.which("sh")
    if sh is None:
        print("  - test_hook_blocks_a_secret (sh introuvable, ignoré)")
        return
    with tempfile.TemporaryDirectory(prefix="agency_hook_") as tmp:
        repo = Path(tmp)
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        shutil.copytree(REPO_ROOT / "scripts", repo / "scripts")
        shutil.copytree(REPO_ROOT / ".agents", repo / ".agents")
        clean = subprocess.run([sh, str(HOOK)], cwd=repo, capture_output=True, text=True)
        assert clean.returncode == 0, clean.stdout + clean.stderr

        (repo / "config.py").write_text('cle = "sk-aB3dE5fG7hI9jK1lM3nO5pQ7"\n', encoding="utf-8")
        leaked = subprocess.run([sh, str(HOOK)], cwd=repo, capture_output=True, text=True)
        assert leaked.returncode != 0, "le hook devait bloquer la clé"
    print("  ✓ test_hook_blocks_a_secret")


if __name__ == "__main__":
    print("Exécution des tests du hook pre-commit...")
    test_hook_is_executable_in_git()
    test_hook_blocks_a_secret()
    print("\nGREEN — Tous les 2 tests du hook pre-commit passent !")
    sys.exit(0)
