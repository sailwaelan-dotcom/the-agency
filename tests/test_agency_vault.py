"""
Tests unitaires pour le coffre-fort local RGPD et mémoire épistémique (agency/vault.py).
"""
import os
import shutil
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SERVERS_DIR = REPO_ROOT / "mcp" / "servers"
sys.path.insert(0, str(SERVERS_DIR))
sys.path.insert(0, str(REPO_ROOT))

# Configuration d'un coffre temporaire isolé
TEMP_VAULT_DIR = Path(tempfile.mkdtemp(prefix="agency_test_vault_"))
os.environ["AGENCY_VAULT_DIR"] = str(TEMP_VAULT_DIR)

from agency.vault import (
    save_client,
    get_client,
    list_clients,
    delete_client,
    record_instinct,
    get_instincts,
)
from agency_be.server import handle_call_tool


def test_vault_save_and_get_client():
    client_data = {
        "bce_number": "0202.239.951",
        "name": "Proximus Test",
        "vat_regime": "normal",
        "payment_terms_days": 30,
        "notes": "Client historique télécoms.",
    }
    saved = save_client(client_data)
    assert saved["bce_number"] == "0202239951"
    assert saved["vat_number"] == "BE0202239951"
    assert saved["payment_terms_days"] == 30

    fetched = get_client("0202239951")
    assert fetched is not None
    assert fetched["name"] == "Proximus Test"
    print("  ✓ test_vault_save_and_get_client")


def test_vault_list_and_delete_client():
    # Enregistrer un deuxième client
    save_client({
        "bce_number": "0403.201.185",
        "name": "Solvay Test",
        "payment_terms_days": 60,
    })

    clients = list_clients()
    assert len(clients) >= 2

    # Droit à l'oubli / Suppression
    deleted = delete_client("0403.201.185")
    assert deleted is True
    assert get_client("0403201185") is None

    # Tentative de suppression d'un client inexistant
    assert delete_client("9999999999") is False
    print("  ✓ test_vault_list_and_delete_client")


def test_vault_instincts_recording():
    record_instinct(
        topic="facturation",
        rule="Toujours inclure le numéro de PO avant émission.",
        confidence=0.95,
    )
    record_instinct(
        topic="relances",
        rule="Relancer le mardi matin à 10h plutôt que le lundi.",
        confidence=0.90,
    )

    all_instincts = get_instincts()
    assert len(all_instincts) >= 2

    facturation_instincts = get_instincts(topic="facturation")
    assert len(facturation_instincts) == 1
    assert "PO" in facturation_instincts[0]["rule"]
    print("  ✓ test_vault_instincts_recording")


def test_mcp_vault_tools_and_guardrail():
    # Appel via MCP
    saved = handle_call_tool("vault_save_client", {
        "client_data": {
            "bce_number": "0214.596.464",
            "name": "RTBF Test MCP",
            "payment_terms_days": 45,
        }
    })
    assert saved["bce_number"] == "0214596464"

    # Tentative de sauvegarde avec numéro BCE invalide -> Guardrail pré-vol doit bloquer
    try:
        handle_call_tool("vault_save_client", {
            "client_data": {
                "bce_number": "0202.239.999",  # Modulo 97 erroné
                "name": "Faux Client",
            }
        })
        assert False, "Le guardrail pré-vol devait bloquer ce numéro BCE erroné"
    except ValueError as e:
        assert "Modulo 97" in str(e)
    print("  ✓ test_mcp_vault_tools_and_guardrail")


def cleanup():
    if TEMP_VAULT_DIR.exists():
        shutil.rmtree(TEMP_VAULT_DIR, ignore_errors=True)


if __name__ == "__main__":
    print("Exécution des tests du Vault RGPD & Mémoire locale...")
    try:
        test_vault_save_and_get_client()
        test_vault_list_and_delete_client()
        test_vault_instincts_recording()
        test_mcp_vault_tools_and_guardrail()
        print("\nGREEN — Tous les 4 tests du Vault RGPD passent !")
    finally:
        cleanup()
    sys.exit(0)
