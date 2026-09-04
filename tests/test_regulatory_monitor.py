"""
Tests unitaires pour le Watchdog de Dérive Réglementaire (regulatory_monitor.py).
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.regulatory_monitor import (
    audit_repo_thresholds,
    generate_report,
    REFERENCE_THRESHOLDS,
)


def test_reference_thresholds_validity():
    assert REFERENCE_THRESHOLDS["tva_standard_rate"] == 21.0
    assert REFERENCE_THRESHOLDS["tva_franchise_56bis_threshold"] == 25000.0
    assert REFERENCE_THRESHOLDS["inasti_starter_rate"] == 20.5
    assert REFERENCE_THRESHOLDS["peppol_legal_deadline_year"] == 2026
    print("  ✓ test_reference_thresholds_validity")


def test_repo_thresholds_audit():
    audit = audit_repo_thresholds()
    assert "timestamp" in audit
    assert "findings" in audit
    # Aucune anomalie critique ne doit être détectée dans le repo
    criticals = [f for f in audit["findings"] if f.get("severity") == "CRITICAL"]
    assert len(criticals) == 0
    assert audit["is_synced"] is True
    print("  ✓ test_repo_thresholds_audit")


def test_generate_report_offline():
    report = generate_report(offline_mode=True)
    assert report["status"] == "PASS"
    assert "threshold_audit" in report
    assert len(report["official_sources_liveness"]) == 0
    print("  ✓ test_generate_report_offline")


if __name__ == "__main__":
    print("Exécution des tests du Watchdog de dérive réglementaire...")
    test_reference_thresholds_validity()
    test_repo_thresholds_audit()
    test_generate_report_offline()
    print("\nGREEN — Tous les 3 tests du Watchdog passent !")
    sys.exit(0)
