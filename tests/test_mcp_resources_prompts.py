#!/usr/bin/env python3
"""
TDD Tests — MCP Resources & Prompts pour The Agency (Phase RED -> GREEN).
Vérifie la conformité totale avec la spécification Model Context Protocol :
1. Primitives Resources (list, read, URIs belges réglementaires).
2. Primitives Prompts (list, get, workflows serveur déclaratifs).
3. Handshake initialize avec capabilities déclarées.
4. Intégration JSON-RPC 2.0 stdio.
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
# 1. Tests Resources MCP
# ============================================================================

def test_resources_list():
    from agency_be.resources import get_server_resources
    resources = get_server_resources()
    assert isinstance(resources, list)
    assert len(resources) >= 3

    uris = [r["uri"] for r in resources]
    assert "belgian-tax://2026/rates" in uris
    assert "inasti://2026/brackets" in uris
    assert "cir92://deductibility/rules" in uris

    for r in resources:
        assert "uri" in r
        assert "name" in r
        assert "description" in r
        assert "mimeType" in r


def test_resource_read_tax_rates():
    from agency_be.resources import handle_read_resource
    res = handle_read_resource("belgian-tax://2026/rates")
    assert res["uri"] == "belgian-tax://2026/rates"
    assert res["mimeType"] == "application/json"
    data = json.loads(res["text"])
    assert "rates" in data
    assert data["rates"]["standard"] == 0.21
    assert "franchise_56bis" in data
    assert data["franchise_56bis"]["threshold"] == 25000.0


def test_resource_read_inasti_brackets():
    from agency_be.resources import handle_read_resource
    res = handle_read_resource("inasti://2026/brackets")
    assert res["uri"] == "inasti://2026/brackets"
    data = json.loads(res["text"])
    assert data["minimum_annual_income"] == 16861.46
    assert data["rate_bracket_1"] == 0.205
    assert data["rate_bracket_2"] == 0.1416


def test_resource_read_cir92_rules():
    from agency_be.resources import handle_read_resource
    res = handle_read_resource("cir92://deductibility/rules")
    data = json.loads(res["text"])
    assert data["restaurant_expenses"]["deductibility_rate"] == 0.69
    assert data["reception_expenses"]["deductibility_rate"] == 0.50


def test_resource_read_unknown():
    from agency_be.resources import handle_read_resource
    if pytest is not None:
        with pytest.raises(ValueError):
            handle_read_resource("unknown://uri")
    else:
        with assert_raises(ValueError):
            handle_read_resource("unknown://uri")


# ============================================================================
# 2. Tests Prompts MCP
# ============================================================================

def test_prompts_list():
    from agency_be.prompts import get_server_prompts
    prompts = get_server_prompts()
    assert isinstance(prompts, list)
    assert len(prompts) >= 2

    names = [p["name"] for p in prompts]
    assert "audit_client_peppol" in names
    assert "prepare_quarterly_tax_closing" in names

    for p in prompts:
        assert "name" in p
        assert "description" in p
        assert "arguments" in p


def test_prompt_get_audit_client():
    from agency_be.prompts import handle_get_prompt
    res = handle_get_prompt("audit_client_peppol", {"bce_number": "0202.239.951"})
    assert "description" in res
    assert "messages" in res
    assert len(res["messages"]) >= 1
    content = res["messages"][0]["content"]["text"]
    assert "0202.239.951" in content
    assert "BCE" in content
    assert "Peppol" in content


def test_prompt_get_unknown():
    from agency_be.prompts import handle_get_prompt
    if pytest is not None:
        with pytest.raises(ValueError):
            handle_get_prompt("unknown_prompt", {})
    else:
        with assert_raises(ValueError):
            handle_get_prompt("unknown_prompt", {})


# ============================================================================
# 3. Tests Intégration Serveur MCP (Handshake & Dispatch)
# ============================================================================

def test_server_capabilities():
    from agency_be.server import get_server_capabilities
    caps = get_server_capabilities()
    assert "tools" in caps
    assert "resources" in caps
    assert "prompts" in caps


if __name__ == "__main__":
    tests = [
        test_resources_list,
        test_resource_read_tax_rates,
        test_resource_read_inasti_brackets,
        test_resource_read_cir92_rules,
        test_resource_read_unknown,
        test_prompts_list,
        test_prompt_get_audit_client,
        test_prompt_get_unknown,
        test_server_capabilities,
    ]
    failures = []
    print("Exécution des tests MCP Resources & Prompts...")
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

    print(f"\nGREEN — Tous les {len(tests)} tests Resources & Prompts passent !")
    sys.exit(0)
