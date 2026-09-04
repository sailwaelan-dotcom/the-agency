"""
Tests unitaires pour l'Architecture Two-Tier Context et le chargement on-demand.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SERVERS_DIR = REPO_ROOT / "mcp" / "servers"
sys.path.insert(0, str(SERVERS_DIR))
sys.path.insert(0, str(REPO_ROOT))

from agency_be.server import handle_call_tool, get_server_tools


def test_catalog_lite_exists_and_complete():
    catalog_path = REPO_ROOT / ".agents" / "catalog_lite.json"
    assert catalog_path.exists(), "catalog_lite.json doit être généré."
    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    skills = data.get("skills", [])
    assert len(skills) == 22, f"Attendu 22 skills, trouvé {len(skills)}"

    names = {s["name"] for s in skills}
    assert "be-invoicing-peppol" in names
    assert "be-devis-quotes" in names
    assert "activate-agency" in names
    print("  ✓ test_catalog_lite_exists_and_complete")


def test_catalog_lite_token_budget():
    catalog_path = REPO_ROOT / ".agents" / "catalog_lite.json"
    content = catalog_path.read_text(encoding="utf-8")
    est_tokens = len(content) / 4
    # Doit rester ultra-léger (< 4 000 tokens)
    assert est_tokens < 4000, f"Le catalogue léger dépasse le budget token : ~{est_tokens} tokens"
    print(f"  ✓ test_catalog_lite_token_budget (~{round(est_tokens)} tokens)")


def test_load_skill_context_via_mcp():
    res = handle_call_tool("load_skill_context", {"skill_name": "be-invoicing-peppol"})
    assert res["skill_name"] == "be-invoicing-peppol"
    assert "Peppol" in res["content"]
    assert "Workflow" in res["content"]
    print("  ✓ test_load_skill_context_via_mcp")


def test_load_skill_context_unknown_error():
    try:
        handle_call_tool("load_skill_context", {"skill_name": "competence_fantome_inconnue"})
        assert False, "Devait lever ValueError sur skill inconnu"
    except ValueError as e:
        assert "introuvable" in str(e)
    print("  ✓ test_load_skill_context_unknown_error")


def test_server_tools_list_includes_two_tier_and_kbo():
    tools = get_server_tools()
    tool_names = {t["name"] for t in tools}
    assert "load_skill_context" in tool_names
    assert "search_bce_by_name" in tool_names
    assert "vault_save_client" in tool_names
    assert "vault_get_client" in tool_names
    print("  ✓ test_server_tools_list_includes_two_tier_and_kbo")


if __name__ == "__main__":
    print("Exécution des tests Two-Tier Context Engineering...")
    test_catalog_lite_exists_and_complete()
    test_catalog_lite_token_budget()
    test_load_skill_context_via_mcp()
    test_load_skill_context_unknown_error()
    test_server_tools_list_includes_two_tier_and_kbo()
    print("\nGREEN — Tous les 5 tests Two-Tier Context passent !")
    sys.exit(0)
