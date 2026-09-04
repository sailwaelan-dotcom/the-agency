"""
Tests unitaires pour le micro-moteur KBO / BCE SQLite hors-ligne.
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SERVERS_DIR = REPO_ROOT / "mcp" / "servers"
sys.path.insert(0, str(SERVERS_DIR))

from agency_be.tools.kbo_db import (
    init_kbo_db,
    lookup_bce_offline,
    search_bce_by_name,
    normalize_bce,
)


def test_normalize_bce():
    assert normalize_bce("0202.239.951") == "0202239951"
    assert normalize_bce("BE 0202 239 951") == "0202239951"
    assert normalize_bce("202239951") == "0202239951"
    print("  ✓ test_normalize_bce")


def test_kbo_in_memory_db():
    conn = init_kbo_db(":memory:", seed=True)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM enterprises")
    count = cur.fetchone()[0]
    assert count >= 5
    conn.close()
    print("  ✓ test_kbo_in_memory_db")


def test_lookup_bce_offline():
    res = lookup_bce_offline("0202239951")
    assert res is not None
    assert "PROXIMUS" in res["denomination"]
    assert res["status"] == "AC"
    assert res["postal_code"] == "1030"

    # Inexistant
    assert lookup_bce_offline("0000000000") is None
    print("  ✓ test_lookup_bce_offline")


def test_search_bce_by_name():
    results = search_bce_by_name("RTBF")
    assert len(results) >= 1
    assert "RTBF" in results[0]["denomination"]

    # Avec code postal
    results_solvay = search_bce_by_name("SOLVAY", postal_code="1120")
    assert len(results_solvay) == 1
    assert "SOLVAY" in results_solvay[0]["denomination"]

    # Recherche sans résultat
    empty = search_bce_by_name("ENTREPRISE_TOTALEMENT_INEXISTANTE_XYZ")
    assert len(empty) == 0
    print("  ✓ test_search_bce_by_name")


if __name__ == "__main__":
    print("Exécution des tests KBO SQLite hors-ligne...")
    test_normalize_bce()
    test_kbo_in_memory_db()
    test_lookup_bce_offline()
    test_search_bce_by_name()
    print("\nGREEN — Tous les 4 tests KBO offline passent !")
    sys.exit(0)
