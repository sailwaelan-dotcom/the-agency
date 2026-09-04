#!/usr/bin/env python3
"""
Test End-to-End (E2E) automatisé pour le serveur MCP agency-be-mcp.
Démarre le serveur en sous-processus réel, échange des trames JSON-RPC 2.0
sur l'entrée/sortie standard (stdio) et valide les réponses de chaque outil.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SERVERS_DIR = REPO_ROOT / "mcp" / "servers"

env = os.environ.copy()
env["PYTHONPATH"] = str(SERVERS_DIR)


def test_mcp_stdio_e2e():
    proc = subprocess.Popen(
        [sys.executable, "-m", "agency_be.server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(REPO_ROOT),
        env=env,
        bufsize=1,
    )

    req_id = 1

    def send_rpc(method, params=None):
        nonlocal req_id
        payload = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": method,
        }
        if params is not None:
            payload["params"] = params
        req_id += 1

        line = json.dumps(payload) + "\n"
        proc.stdin.write(line)
        proc.stdin.flush()

        resp_line = proc.stdout.readline()
        if not resp_line:
            err = proc.stderr.read()
            raise RuntimeError(f"Le serveur MCP s'est arrêté inopinément. Stderr: {err}")
        return json.loads(resp_line.strip())

    try:
        # 1. Initialize
        init_res = send_rpc("initialize", {})
        assert init_res.get("jsonrpc") == "2.0"
        server_info = init_res.get("result", {}).get("serverInfo", {})
        assert server_info.get("name") == "agency-be-mcp"
        assert server_info.get("version") == "1.0.0"

        # 2. tools/list
        tools_res = send_rpc("tools/list", {})
        tools = tools_res.get("result", {}).get("tools", [])
        assert len(tools) >= 5
        tool_names = {t["name"] for t in tools}
        assert "validate_bce_number" in tool_names
        assert "get_be_tax_calendar" in tool_names
        assert "calc_inasti_provision" in tool_names
        assert "check_vat_vies" in tool_names
        assert "lookup_peppol_participant" in tool_names
        assert "generate_peppol_ubl" in tool_names
        assert "validate_peppol_ubl" in tool_names

        # 3. tools/call: validate_bce_number
        bce_call = send_rpc("tools/call", {
            "name": "validate_bce_number",
            "arguments": {"bce_number": "0202.239.951"}
        })
        bce_data = json.loads(bce_call["result"]["content"][0]["text"])
        assert bce_data["is_valid"] is True
        assert bce_data["normalized"] == "0202239951"
        assert bce_data["formatted"] == "BE 0202.239.951"

        # 4. tools/call: get_be_tax_calendar
        cal_call = send_rpc("tools/call", {
            "name": "get_be_tax_calendar",
            "arguments": {"year": 2026, "regime": "trimestriel"}
        })
        cal_data = json.loads(cal_call["result"]["content"][0]["text"])
        assert isinstance(cal_data, list)
        assert len(cal_data) == 12
        assert any(e["type"] == "tva" for e in cal_data)
        assert any(e["type"] == "versement_anticipe" for e in cal_data)
        assert any(e["type"] == "inasti" for e in cal_data)

        # 5. tools/call: calc_inasti_provision
        inasti_call = send_rpc("tools/call", {
            "name": "calc_inasti_provision",
            "arguments": {"annual_net_income": 40000.0, "is_starter": False, "year": 2026}
        })
        inasti_data = json.loads(inasti_call["result"]["content"][0]["text"])
        assert inasti_data["quarterly_base_contribution"] == 2050.0
        assert inasti_data["is_minimum_applied"] is False
        assert inasti_data["is_ceiling_applied"] is False

        # 6. tools/call: check_vat_vies (vérifie que l'appel renvoie une structure valide)
        vies_call = send_rpc("tools/call", {
            "name": "check_vat_vies",
            "arguments": {"vat_number": "0202239951", "country_code": "BE"}
        })
        vies_data = json.loads(vies_call["result"]["content"][0]["text"])
        assert "is_valid" in vies_data
        assert "country_code" in vies_data

        # 7. tools/call: lookup_peppol_participant (vérifie que l'appel renvoie une structure valide)
        peppol_call = send_rpc("tools/call", {
            "name": "lookup_peppol_participant",
            "arguments": {"bce_number": "0202239951"}
        })
        peppol_data = json.loads(peppol_call["result"]["content"][0]["text"])
        assert "is_registered" in peppol_data
        assert "participant_id" in peppol_data

    finally:
        try:
            proc.stdin.close()
            proc.terminate()
            proc.wait(timeout=2)
        except Exception:
            pass


if __name__ == "__main__":
    print("Exécution du test E2E du serveur MCP stdio...")
    try:
        test_mcp_stdio_e2e()
        print("GREEN — Le serveur MCP stdio répond parfaitement de bout en bout !")
        sys.exit(0)
    except Exception as exc:
        print(f"RED — Échec du test E2E : {exc}")
        sys.exit(1)
