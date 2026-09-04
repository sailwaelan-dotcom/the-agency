"""
Tests unitaires et end-to-end pour le CLI Solopreneur (agency/cli.py).
"""
import io
import os
import sys
from contextlib import redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SERVERS_DIR = REPO_ROOT / "mcp" / "servers"
sys.path.insert(0, str(SERVERS_DIR))
sys.path.insert(0, str(REPO_ROOT))

from agency.cli import build_parser, cmd_bce, cmd_inasti, cmd_deadlines, cmd_vault


def test_cli_bce():
    parser = build_parser()
    args = parser.parse_args(["bce", "0202.239.951"])
    f = io.StringIO()
    with redirect_stdout(f):
        cmd_bce(args)
    out = f.getvalue()
    assert "✓ VALIDE" in out
    assert "PROXIMUS" in out
    assert "BE 0202.239.951" in out
    print("  ✓ test_cli_bce")


def test_cli_inasti():
    parser = build_parser()
    args = parser.parse_args(["inasti", "--income", "45000", "--year", "2026"])
    f = io.StringIO()
    with redirect_stdout(f):
        cmd_inasti(args)
    out = f.getvalue()
    assert "45,000.00 €" in out
    assert "TOTAL TRIMESTRIEL DÛ" in out
    assert "2,386.97 €" in out
    print("  ✓ test_cli_inasti")


def test_cli_deadlines():
    parser = build_parser()
    args = parser.parse_args(["deadlines", "--year", "2026"])
    f = io.StringIO()
    with redirect_stdout(f):
        cmd_deadlines(args)
    out = f.getvalue()
    assert "2026-04-20" in out
    assert "TVA Trimestre 1 2026" in out
    assert "J-14" in out
    print("  ✓ test_cli_deadlines")


def test_cli_vault_list():
    parser = build_parser()
    args = parser.parse_args(["vault", "list"])
    f = io.StringIO()
    with redirect_stdout(f):
        cmd_vault(args)
    out = f.getvalue()
    assert "Fiches Clients" in out
    print("  ✓ test_cli_vault_list")


if __name__ == "__main__":
    print("Exécution des tests CLI Solopreneur...")
    test_cli_bce()
    test_cli_inasti()
    test_cli_deadlines()
    test_cli_vault_list()
    print("\nGREEN — Tous les 4 tests du CLI Solopreneur passent !")
    sys.exit(0)
