#!/usr/bin/env python3
"""
TDD Tests — Guardrails d'Exécution & Intercepteur Runtime pour The Agency (Phase RED -> GREEN).
Vérifie le blocage pré-vol des opérations illégales et la désensibilisation (PII / anti-leak).
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


# ============================================================================
# 1. Tests Pre-flight Guardrail
# ============================================================================

def test_guardrail_valid_bce():
    from agency_be.guardrails import validate_preflight
    ok, err = validate_preflight("lookup_peppol_participant", {"bce_number": "0202.239.951"})
    assert ok is True
    assert err is None


def test_guardrail_block_invalid_bce():
    from agency_be.guardrails import validate_preflight
    # 0202.239.999 a un checksum invalide
    ok, err = validate_preflight("lookup_peppol_participant", {"bce_number": "0202.239.999"})
    assert ok is False
    assert "Modulo 97" in err


def test_guardrail_block_illegal_vat_rate():
    from agency_be.guardrails import validate_preflight
    bad_invoice = {
        "invoice_number": "INV-1",
        "supplier": {"bce_number": "0202.239.951"},
        "customer": {"bce_number": "0202.239.951"},
        "lines": [{"unit_price": 100.0, "quantity": 1.0, "vat_rate": 0.15}],  # 15% n'existe pas en Belgique
    }
    ok, err = validate_preflight("generate_peppol_ubl", {"invoice_data": bad_invoice})
    assert ok is False
    assert "TVA" in err
    assert "0.15" in err


def test_guardrail_allow_legal_vat_rates():
    from agency_be.guardrails import validate_preflight
    for legal_rate in [0.21, 0.12, 0.06, 0.00]:
        invoice = {
            "invoice_number": "INV-1",
            "supplier": {"bce_number": "0202.239.951"},
            "customer": {"bce_number": "0202.239.951"},
            "lines": [{"unit_price": 100.0, "quantity": 1.0, "vat_rate": legal_rate}],
        }
        ok, err = validate_preflight("generate_peppol_ubl", {"invoice_data": invoice})
        assert ok is True, f"Taux légal rejeté à tort : {legal_rate}"


# ============================================================================
# 2. Tests Post-flight Sanitization (PII & Leak Masking)
# ============================================================================

def test_guardrail_sanitize_national_register_number():
    from agency_be.guardrails import sanitize_postflight
    text_with_niss = "Le dirigeant a le NISS 85.07.15-123.45 enregistré."
    clean = sanitize_postflight(text_with_niss)
    assert "85.07.15-123.45" not in clean
    assert "[REGISTRE_NATIONAL_MASQUE]" in clean


def test_guardrail_sanitize_machine_path():
    from agency_be.guardrails import sanitize_postflight
    raw_payload = {"log": "Fichier stocké dans C:\\Users\\MonNom\\Documents\\facture.xml"}
    clean_payload = sanitize_postflight(raw_payload)
    assert "C:\\Users\\MonNom" not in clean_payload["log"]
    assert "[CHEMIN_MACHINE_MASQUE]" in clean_payload["log"]


# ============================================================================
# 3. Tests Intégration Serveur MCP Intercepteur
# ============================================================================

def test_mcp_server_guardrail_interceptor():
    from agency_be.server import handle_call_tool
    # Appel de lookup_peppol_participant avec paramètre corrompu : doit lever ValueError
    if pytest is not None:
        with pytest.raises(ValueError) as exc:
            handle_call_tool("lookup_peppol_participant", {"bce_number": "0202.239.999"})
        assert "Guardrail" in str(exc.value)
    else:
        with assert_raises(ValueError):
            handle_call_tool("lookup_peppol_participant", {"bce_number": "0202.239.999"})


if __name__ == "__main__":
    tests = [
        test_guardrail_valid_bce,
        test_guardrail_block_invalid_bce,
        test_guardrail_block_illegal_vat_rate,
        test_guardrail_allow_legal_vat_rates,
        test_guardrail_sanitize_national_register_number,
        test_guardrail_sanitize_machine_path,
        test_mcp_server_guardrail_interceptor,
    ]
    failures = []
    print("Exécution des tests Guardrails...")
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

    print(f"\nGREEN — Tous les {len(tests)} tests Guardrails passent !")
    sys.exit(0)
