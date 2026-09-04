#!/usr/bin/env python3
"""
TDD Tests — Couche MCP & APIs pour The Agency.
Tests écrits selon la méthodologie TDD.

Vérifie :
1. Algorithme de validation et formatage BCE (modulo 97, liens SPF Economie).
2. Calendrier fiscal belge dynamique (SPF Finances TVA/VA et INASTI, alertes J-14 / J-3).
3. Simulateur de cotisations sociales INASTI (taux légal, plafonds, minimums, frais de caisse).
4. Validation TVA VIES (formatage, URL officielle UE, mock et gestion réseau).
5. Annuaire Peppol Directory (identifiant participant iso6523, mock et gestion réseau).
6. Protocole et liste des outils du serveur MCP agency-be-mcp.
7. Fichiers de configuration harness (Claude Code, Cursor, Hermes, Kilocode).
"""
from contextlib import contextmanager
import json
import sys
from pathlib import Path
import yaml

try:
    import pytest
except ImportError:
    pytest = None

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "mcp" / "servers"))

# Emplacement du module MCP
MCP_DIR = REPO_ROOT / "mcp"
SERVERS_DIR = MCP_DIR / "servers" / "agency_be"
CONFIGS_DIR = MCP_DIR / "configs"


class SimpleMonkeyPatch:
    """Mock léger pour exécuter les tests hors environnement pytest complet."""
    def __init__(self):
        self._undo = []

    def setattr(self, target, name, value):
        old = getattr(target, name)
        self._undo.append((target, name, old))
        setattr(target, name, value)

    def undo(self):
        for target, name, old in reversed(self._undo):
            setattr(target, name, old)


@contextmanager
def assert_raises(exc_type):
    try:
        yield
    except exc_type:
        return
    raise AssertionError(f"L'exception {exc_type} n'a pas été levée.")


# ============================================================================
# 1. Tests Outil BCE : modulo 97, normalisation, formatage
# ============================================================================

def test_bce_validation_valid():
    from agency_be.tools.bce import validate_bce_number
    # 0202.239.951 est un numéro BCE mathématiquement valide :
    # 2022399 % 97 = 46 -> 97 - 46 = 51
    result = validate_bce_number("0202.239.951")
    assert result["is_valid"] is True
    assert result["normalized"] == "0202239951"
    assert result["formatted"] == "BE 0202.239.951"
    assert "kbopub.economie.fgov.be" in result["kbo_url"]


def test_bce_validation_with_prefix_and_spaces():
    from agency_be.tools.bce import validate_bce_number
    # Avec "BE " et espaces
    result = validate_bce_number("BE 0202 239 951")
    assert result["is_valid"] is True
    assert result["normalized"] == "0202239951"


def test_bce_validation_invalid_checksum():
    from agency_be.tools.bce import validate_bce_number
    # Même numéro mais checksum erroné 99 au lieu de 51
    result = validate_bce_number("0202.239.999")
    assert result["is_valid"] is False
    assert result["error"] == "checksum_mismatch"
    assert result["expected_checksum"] == 51
    assert result["actual_checksum"] == 99


def test_bce_validation_invalid_length():
    from agency_be.tools.bce import validate_bce_number
    result = validate_bce_number("12345")
    assert result["is_valid"] is False
    assert result["error"] == "invalid_length"


# ============================================================================
# 2. Tests Outil Calendrier Fiscal Belge : TVA, VA1-VA4, INASTI
# ============================================================================

def test_tax_calendar_2026_quarterly():
    from agency_be.tools.tax_calendar import get_be_tax_calendar
    calendar = get_be_tax_calendar(year=2026, regime="trimestriel")
    assert isinstance(calendar, list)
    assert len(calendar) >= 12  # 4 TVA + 4 VA + 4 INASTI

    # Vérification des types
    types = {item["type"] for item in calendar}
    assert "tva" in types
    assert "versement_anticipe" in types
    assert "inasti" in types

    # Vérification TVA T1 : 20 avril 2026
    tva_t1 = next(item for item in calendar if item["id"] == "tva_2026_q1")
    assert tva_t1["deadline"] == "2026-04-20"
    assert tva_t1["alert_j14"] == "2026-04-06"
    assert tva_t1["alert_j3"] == "2026-04-17"
    assert "Intervat" in tva_t1["procedure"]

    # Vérification Versements anticipés (VA1: 10 avril, VA4: 20 décembre)
    va1 = next(item for item in calendar if item["id"] == "va_2026_1")
    assert va1["deadline"] == "2026-04-10"
    va4 = next(item for item in calendar if item["id"] == "va_2026_4")
    assert va4["deadline"] == "2026-12-20"

    # Vérification INASTI Q1 : 31 mars 2026
    inasti_q1 = next(item for item in calendar if item["id"] == "inasti_2026_q1")
    assert inasti_q1["deadline"] == "2026-03-31"


# ============================================================================
# 3. Tests Outil INASTI : simulation cotisations sociales provisionnelles
# ============================================================================

def test_inasti_provision_calculation_minimum():
    from agency_be.tools.inasti import calc_inasti_provision
    # Revenu modeste (< seuil minimum légal) : doit appliquer la cotisation minimale
    res = calc_inasti_provision(annual_net_income=10000.0, is_starter=False, year=2026)
    assert res["is_minimum_applied"] is True
    assert res["annual_net_income"] == 10000.0
    assert res["quarterly_base_contribution"] > 800.0  # ~864 € / trimestre minimum légal
    assert res["management_fee_rate"] > 0
    assert res["total_quarterly_due"] > res["quarterly_base_contribution"]
    assert res["as_of"] == "2026-01-01"


def test_inasti_provision_calculation_standard():
    from agency_be.tools.inasti import calc_inasti_provision
    # Revenu net 40 000 € : taux plein 20.5%
    res = calc_inasti_provision(annual_net_income=40000.0, is_starter=False, year=2026)
    assert res["is_minimum_applied"] is False
    assert res["is_ceiling_applied"] is False
    # Base annuelle = 40 000 * 20.5% = 8 200 € -> par trimestre = 2 050 €
    expected_quarterly = (40000.0 * 0.205) / 4.0
    assert abs(res["quarterly_base_contribution"] - expected_quarterly) < 1.0


def test_inasti_provision_calculation_ceiling():
    from agency_be.tools.inasti import calc_inasti_provision
    # Revenu très élevé (ex: 200 000 €) : doit plafonner au maximum légal
    res = calc_inasti_provision(annual_net_income=200000.0, is_starter=False, year=2026)
    assert res["is_ceiling_applied"] is True
    assert res["quarterly_base_contribution"] < 5500.0  # Plafond légal ~4900-5000 €


# ============================================================================
# 4. Tests Outil VIES : formatage et URL officielle
# ============================================================================

def test_vies_request_url_builder():
    from agency_be.tools.vies import build_vies_url
    url = build_vies_url(vat_number="0123.456.789", country_code="BE")
    assert url == "https://ec.europa.eu/taxation_customs/vies/rest-api/ms/BE/vat/0123456789"


def test_vies_offline_mock(monkeypatch=None):
    from agency_be.tools.vies import check_vat_vies

    class MockResponse:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def read(self):
            return json.dumps({
                "isValid": True,
                "userError": "VALID",
                "name": "ACME BELGIUM SPRL",
                "address": "RUE DE LA LOI 16, 1000 BRUXELLES",
                "requestDate": "2026-09-04T12:00:00.000Z"
            }).encode("utf-8")

    def mock_urlopen(req, timeout=10):
        return MockResponse()

    created_mp = False
    if monkeypatch is None:
        monkeypatch = SimpleMonkeyPatch()
        created_mp = True

    import urllib.request
    monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen)

    try:
        res = check_vat_vies("0202.239.951", country_code="BE")
        assert res["is_valid"] is True
        assert res["name"] == "ACME BELGIUM SPRL"
        assert res["country_code"] == "BE"
        assert res["vat_number"] == "0202239951"
    finally:
        if created_mp:
            monkeypatch.undo()


# ============================================================================
# 5. Tests Outil Peppol Directory
# ============================================================================

def test_peppol_participant_id():
    from agency_be.tools.peppol import build_peppol_participant_id
    pid = build_peppol_participant_id("0202.239.951")
    assert pid == "iso6523-actorid-upis::0208:0202239951"


def test_peppol_lookup_mock(monkeypatch=None):
    from agency_be.tools.peppol import lookup_peppol_participant

    class MockResponse:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def read(self):
            return json.dumps({
                "matches": [
                    {
                        "participantID": {"scheme": "iso6523-actorid-upis", "value": "0208:0202239951"},
                        "entities": [{"name": [{"value": "ACME BELGIUM"}]}]
                    }
                ]
            }).encode("utf-8")

    def mock_urlopen(req, timeout=10):
        return MockResponse()

    created_mp = False
    if monkeypatch is None:
        monkeypatch = SimpleMonkeyPatch()
        created_mp = True

    import urllib.request
    monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen)

    try:
        res = lookup_peppol_participant("0202.239.951")
        assert res["is_registered"] is True
        assert res["participant_id"] == "iso6523-actorid-upis::0208:0202239951"
        assert "ACME BELGIUM" in res["entity_name"]
    finally:
        if created_mp:
            monkeypatch.undo()


# ============================================================================
# 6. Tests Serveur MCP : Liste des Outils & JSON-RPC
# ============================================================================

def test_mcp_server_tools_list():
    from agency_be.server import get_server_tools
    tools = get_server_tools()
    tool_names = [t["name"] for t in tools]
    expected = [
        "validate_bce_number",
        "check_vat_vies",
        "lookup_peppol_participant",
        "get_be_tax_calendar",
        "calc_inasti_provision",
    ]
    for name in expected:
        assert name in tool_names, f"Tool {name} manquant dans la liste du serveur MCP"

    for tool in tools:
        assert "description" in tool
        assert "inputSchema" in tool
        assert tool["inputSchema"]["type"] == "object"


def test_mcp_server_call_tool_dispatch():
    from agency_be.server import handle_call_tool
    # Test dispatch de validate_bce_number
    res = handle_call_tool("validate_bce_number", {"bce_number": "0202.239.951"})
    assert res["is_valid"] is True

    # Test dispatch de get_be_tax_calendar
    cal = handle_call_tool("get_be_tax_calendar", {"year": 2026})
    assert len(cal) >= 12

    # Test tool inconnu
    if pytest is not None:
        with pytest.raises(ValueError):
            handle_call_tool("unknown_tool", {})
    else:
        with assert_raises(ValueError):
            handle_call_tool("unknown_tool", {})


# ============================================================================
# 7. Tests Fichiers de Configuration Harness
# ============================================================================

def test_harness_config_claude_code():
    cfg_file = CONFIGS_DIR / "claude_code.json"
    assert cfg_file.exists(), "mcp/configs/claude_code.json manquant"
    data = json.loads(cfg_file.read_text(encoding="utf-8"))
    assert "mcpServers" in data
    assert "agency-be" in data["mcpServers"]
    server_cfg = data["mcpServers"]["agency-be"]
    assert "command" in server_cfg
    assert "args" in server_cfg


def test_harness_config_cursor():
    cfg_file = CONFIGS_DIR / "cursor_mcp.json"
    assert cfg_file.exists(), "mcp/configs/cursor_mcp.json manquant"
    data = json.loads(cfg_file.read_text(encoding="utf-8"))
    assert "mcpServers" in data
    assert "agency-be" in data["mcpServers"]


def test_harness_config_hermes():
    cfg_file = CONFIGS_DIR / "hermes_config.yaml"
    assert cfg_file.exists(), "mcp/configs/hermes_config.yaml manquant"
    data = yaml.safe_load(cfg_file.read_text(encoding="utf-8"))
    assert "mcp_servers" in data
    assert "agency_be" in data["mcp_servers"]


def test_harness_config_kilocode():
    cfg_file = CONFIGS_DIR / "kilocode_mcp.json"
    assert cfg_file.exists(), "mcp/configs/kilocode_mcp.json manquant"
    data = json.loads(cfg_file.read_text(encoding="utf-8"))
    assert "mcpServers" in data
    assert "agency-be" in data["mcpServers"]


# ============================================================================
# Exécution directe (CI compatible python tests/test_*.py)
# ============================================================================

if __name__ == "__main__":
    tests = [
        test_bce_validation_valid,
        test_bce_validation_with_prefix_and_spaces,
        test_bce_validation_invalid_checksum,
        test_bce_validation_invalid_length,
        test_tax_calendar_2026_quarterly,
        test_inasti_provision_calculation_minimum,
        test_inasti_provision_calculation_standard,
        test_inasti_provision_calculation_ceiling,
        test_vies_request_url_builder,
        test_vies_offline_mock,
        test_peppol_participant_id,
        test_peppol_lookup_mock,
        test_mcp_server_tools_list,
        test_mcp_server_call_tool_dispatch,
        test_harness_config_claude_code,
        test_harness_config_cursor,
        test_harness_config_hermes,
        test_harness_config_kilocode,
    ]
    failures = []
    print("Exécution des tests MCP & APIs...")
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
        except Exception as e:
            failures.append((t.__name__, str(e)))
            print(f"  ✗ {t.__name__}: {e}")

    if failures:
        print(f"\nRED — {len(failures)} test(s) en échec :")
        for name, err in failures:
            print(f"  - {name}: {err}")
        sys.exit(1)

    print(f"\nGREEN — Tous les {len(tests)} tests MCP & APIs passent avec succès !")
    sys.exit(0)
