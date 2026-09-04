#!/usr/bin/env python3
"""
TDD Tests — Moteur Peppol BIS 3.0 UBL 2.1 XML pour The Agency (Phase RED -> GREEN).
Vérifie la génération et la validation d'une facture électronique UBL conforme EN 16931.
"""
from contextlib import contextmanager
import json
import sys
from pathlib import Path

try:
    import pytest
except ImportError:
    pytest = None

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "mcp" / "servers"))


@contextmanager
def assert_raises(exc_type):
    try:
        yield
    except exc_type:
        return
    raise AssertionError(f"L'exception {exc_type} n'a pas été levée.")


SAMPLE_INVOICE_DATA = {
    "invoice_number": "INV-2026-0042",
    "issue_date": "2026-04-15",
    "due_date": "2026-05-15",
    "currency": "EUR",
    "payment_reference": "+++123/4567/89012+++",
    "supplier": {
        "bce_number": "0202239951",
        "vat_number": "BE0202239951",
        "name": "Consulting BE SRL",
        "street": "Avenue Louise 100",
        "postal_code": "1050",
        "city": "Bruxelles",
        "country_code": "BE",
        "iban": "BE68539007547034",
    },
    "customer": {
        "bce_number": "0202239951",
        "vat_number": "BE0202239951",
        "name": "Client Entreprise SA",
        "street": "Rue de la Loi 16",
        "postal_code": "1000",
        "city": "Bruxelles",
        "country_code": "BE",
    },
    "lines": [
        {
            "id": "1",
            "name": "Audit d'architecture IA",
            "description": "Prestation d'ingénierie IA solopreneur",
            "quantity": 2.0,
            "unit_price": 950.0,
            "vat_rate": 0.21,
        },
        {
            "id": "2",
            "name": "Accompagnement déploiement",
            "description": "Support technique mise en production",
            "quantity": 1.0,
            "unit_price": 600.0,
            "vat_rate": 0.21,
        },
    ],
}


# ============================================================================
# 1. Tests Générateur UBL 2.1
# ============================================================================

def test_generate_peppol_ubl_valid():
    from agency_be.tools.ubl_generator import generate_peppol_ubl_xml
    res = generate_peppol_ubl_xml(SAMPLE_INVOICE_DATA)
    assert res["success"] is True
    xml_str = res["xml"]
    assert "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" in xml_str
    assert "urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0" in xml_str
    assert "INV-2026-0042" in xml_str
    assert "Consulting BE SRL" in xml_str
    assert "Client Entreprise SA" in xml_str
    assert "0208:0202239951" in xml_str
    assert "+++123/4567/89012+++" in xml_str

    # Totaux attendus :
    # Ligne 1 : 2 * 950 = 1900 €
    # Ligne 2 : 1 * 600 = 600 €
    # Total HTVA = 2500 €
    # TVA 21% = 525 €
    # Total TTC = 3025 €
    assert res["total_htva"] == 2500.0
    assert res["total_tva"] == 525.0
    assert res["total_ttc"] == 3025.0


def test_generate_peppol_ubl_missing_fields():
    from agency_be.tools.ubl_generator import generate_peppol_ubl_xml
    # Données incomplètes sans lignes
    bad_data = {"invoice_number": "INV-1"}
    res = generate_peppol_ubl_xml(bad_data)
    assert res["success"] is False
    assert "error" in res


# ============================================================================
# 2. Tests Validateur UBL 2.1 Schematron
# ============================================================================

def test_validate_peppol_ubl_valid_xml():
    from agency_be.tools.ubl_generator import generate_peppol_ubl_xml
    from agency_be.tools.ubl_validator import validate_peppol_ubl_xml

    gen_res = generate_peppol_ubl_xml(SAMPLE_INVOICE_DATA)
    val_res = validate_peppol_ubl_xml(gen_res["xml"])

    assert val_res["is_valid"] is True
    assert val_res["invoice_number"] == "INV-2026-0042"
    assert val_res["supplier_bce"] == "0202239951"
    assert val_res["payable_amount"] == 3025.0
    assert len(val_res["errors"]) == 0


def test_validate_peppol_ubl_invalid_xml_syntax():
    from agency_be.tools.ubl_validator import validate_peppol_ubl_xml
    val_res = validate_peppol_ubl_xml("<Invoice>Ceci n'est pas un XML valide")
    assert val_res["is_valid"] is False
    assert any("syntax" in err.lower() or "xml" in err.lower() for err in val_res["errors"])


def test_validate_peppol_ubl_missing_customization_id():
    from agency_be.tools.ubl_validator import validate_peppol_ubl_xml
    fake_xml = """<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
        <ID>INV-1</ID>
    </Invoice>"""
    val_res = validate_peppol_ubl_xml(fake_xml)
    assert val_res["is_valid"] is False
    assert any("CustomizationID" in err for err in val_res["errors"])


# ============================================================================
# 3. Tests Intégration Serveur MCP Tools
# ============================================================================

def test_ubl_tools_in_mcp_server():
    from agency_be.server import get_server_tools, handle_call_tool
    tools = get_server_tools()
    tool_names = [t["name"] for t in tools]
    assert "generate_peppol_ubl" in tool_names
    assert "validate_peppol_ubl" in tool_names

    # Test appel via dispatcher
    call_res = handle_call_tool("generate_peppol_ubl", {"invoice_data": SAMPLE_INVOICE_DATA})
    assert call_res["success"] is True
    assert call_res["total_ttc"] == 3025.0


if __name__ == "__main__":
    tests = [
        test_generate_peppol_ubl_valid,
        test_generate_peppol_ubl_missing_fields,
        test_validate_peppol_ubl_valid_xml,
        test_validate_peppol_ubl_invalid_xml_syntax,
        test_validate_peppol_ubl_missing_customization_id,
        test_ubl_tools_in_mcp_server,
    ]
    failures = []
    print("Exécution des tests Peppol UBL...")
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

    print(f"\nGREEN — Tous les {len(tests)} tests Peppol UBL passent !")
    sys.exit(0)
