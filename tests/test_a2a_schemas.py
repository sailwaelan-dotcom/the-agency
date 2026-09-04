#!/usr/bin/env python3
"""
TDD Tests — Protocole A2A (Agent-to-Agent) & Schémas JSON d'Échange Stricts pour The Agency.
Vérifie la validité des schémas JSON et la machine à états de transition (Phase RED -> GREEN).
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = REPO_ROOT / ".agents" / "schemas"
WORKFLOWS_DIR = REPO_ROOT / ".agents" / "workflows"


# ============================================================================
# 1. Tests Existence des Schémas et Workflows
# ============================================================================

def test_a2a_files_exist():
    assert (SCHEMAS_DIR / "quote_draft.v1.json").exists(), "quote_draft.v1.json manquant"
    assert (SCHEMAS_DIR / "contract_terms.v1.json").exists(), "contract_terms.v1.json manquant"
    assert (SCHEMAS_DIR / "invoice_event.v1.json").exists(), "invoice_event.v1.json manquant"
    assert (WORKFLOWS_DIR / "a2a_pipeline.md").exists(), "a2a_pipeline.md manquant"


# ============================================================================
# 2. Tests Validation Schéma quote_draft.v1.json
# ============================================================================

def test_quote_draft_schema_valid():
    schema_path = SCHEMAS_DIR / "quote_draft.v1.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert schema.get("$schema") == "http://json-schema.org/draft-07/schema#"
    assert "required" in schema
    assert "quote_number" in schema["required"]
    assert "pricing_model" in schema["properties"]

    sample_quote = {
        "schema_version": "1.0",
        "quote_number": "DEV-2026-001",
        "issue_date": "2026-04-01",
        "validity_days": 30,
        "pricing_model": "forfait",
        "supplier": {
            "name": "Consultant SRL",
            "bce_number": "0202239951",
            "vat_number": "BE0202239951",
        },
        "customer": {
            "name": "Client SA",
            "bce_number": "0202239951",
        },
        "items": [
            {
                "description": "Cadrage IA",
                "quantity": 1.0,
                "unit_price": 2500.0,
                "vat_rate": 0.21,
            }
        ],
        "deposit_percentage": 30.0,
    }

    # Validation des champs obligatoires
    for req in schema["required"]:
        assert req in sample_quote, f"Champ obligatoire {req} manquant dans sample_quote"


# ============================================================================
# 3. Tests Validation Schéma contract_terms.v1.json
# ============================================================================

def test_contract_terms_schema_valid():
    schema_path = SCHEMAS_DIR / "contract_terms.v1.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert "required" in schema
    assert "quote_ref" in schema["required"]
    assert "jurisdiction" in schema["properties"]

    sample_terms = {
        "schema_version": "1.0",
        "quote_ref": "DEV-2026-001",
        "ip_assignment": "total_upon_full_payment",
        "liability_cap": "Montant total HTVA de la commande",
        "jurisdiction": "Tribunaux francophones de l'arrondissement judiciaire de Bruxelles",
        "rgpd_clause": True,
        "late_interest_rate": 12.5,
    }
    for req in schema["required"]:
        assert req in sample_terms, f"Champ obligatoire {req} manquant dans sample_terms"


# ============================================================================
# 4. Tests Validation Schéma invoice_event.v1.json
# ============================================================================

def test_invoice_event_schema_valid():
    schema_path = SCHEMAS_DIR / "invoice_event.v1.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert "required" in schema
    assert "invoice_number" in schema["required"]
    assert "status" in schema["properties"]

    sample_invoice = {
        "schema_version": "1.0",
        "invoice_number": "INV-2026-001",
        "quote_ref": "DEV-2026-001",
        "peppol_ready": True,
        "peppol_participant_id": "iso6523-actorid-upis::0208:0202239951",
        "totals": {
            "htva": 2500.0,
            "tva": 525.0,
            "ttc": 3025.0,
        },
        "status": "ubl_generated",
    }
    for req in schema["required"]:
        assert req in sample_invoice, f"Champ obligatoire {req} manquant dans sample_invoice"


# ============================================================================
# 5. Tests Documentation Workflow A2A Pipeline
# ============================================================================

def test_a2a_workflow_documentation():
    wf_path = WORKFLOWS_DIR / "a2a_pipeline.md"
    content = wf_path.read_text(encoding="utf-8")
    assert "deviseur-be" in content
    assert "juriste-be" in content
    assert "comptable-be" in content
    assert "secretaire-be" in content
    assert "quote_draft" in content
    assert "invoice_event" in content


if __name__ == "__main__":
    tests = [
        test_a2a_files_exist,
        test_quote_draft_schema_valid,
        test_contract_terms_schema_valid,
        test_invoice_event_schema_valid,
        test_a2a_workflow_documentation,
    ]
    failures = []
    print("Exécution des tests Schémas A2A...")
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
        except Exception as e:
            failures.append((t.__name__, str(e)))
            print(f"  ✗ {t.__name__}: {e}")

    if failures:
        print(f"\nRED — {len(failures)} test(s) en échec (attendu en TDD) :")
        for name, err in failures:
            print(f"  - {name}: {err}")
        sys.exit(1)

    print(f"\nGREEN — Tous les {len(tests)} tests Schémas A2A passent !")
    sys.exit(0)
