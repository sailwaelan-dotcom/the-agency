#!/usr/bin/env python3
"""
Test End-to-End (E2E) en direct du serveur MCP agency-be-mcp.
Démarre le serveur en sous-processus via stdio (JSON-RPC 2.0),
exécute le handshake de démarrage, liste les outils et appelle chaque outil en conditions réelles (APIs en direct).
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


def run_e2e_live():
    print("==================================================================")
    print("🚀 Démarrage du serveur MCP agency-be-mcp (stdio JSON-RPC 2.0)...")
    print("==================================================================")

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
            raise RuntimeError(f"Serveur arrêté inopinément. Stderr: {err}")
        return json.loads(resp_line.strip())

    try:
        # 1. Initialize
        print("\n[1/7] 🤝 Handshake client-serveur (initialize)...")
        init_res = send_rpc("initialize", {})
        print("Réponse serveur :")
        print(json.dumps(init_res, indent=2, ensure_ascii=False))

        # 2. Tools List
        print("\n[2/7] 📋 Découverte des outils disponibles (tools/list)...")
        tools_res = send_rpc("tools/list", {})
        tools = tools_res.get("result", {}).get("tools", [])
        print(f"Outils découverts ({len(tools)}) :")
        for t in tools:
            print(f"  • {t['name']}: {t['description'][:75]}...")

        # 3. Test validate_bce_number (Offline Modulo 97)
        print("\n[3/7] 🔍 Test validate_bce_number...")
        valid_call = send_rpc("tools/call", {
            "name": "validate_bce_number",
            "arguments": {"bce_number": "0202.239.951"}
        })
        content_text = valid_call["result"]["content"][0]["text"]
        print("  -> BCE valide ('0202.239.951') :")
        print("    ", content_text)

        invalid_call = send_rpc("tools/call", {
            "name": "validate_bce_number",
            "arguments": {"bce_number": "0202.239.999"}
        })
        print("  -> BCE checksum invalide ('0202.239.999') :")
        print("    ", invalid_call["result"]["content"][0]["text"])

        # 4. Test get_be_tax_calendar
        print("\n[4/7] 📅 Test get_be_tax_calendar (2026, trimestriel)...")
        calendar_call = send_rpc("tools/call", {
            "name": "get_be_tax_calendar",
            "arguments": {"year": 2026, "regime": "trimestriel"}
        })
        cal_data = json.loads(calendar_call["result"]["content"][0]["text"])
        print(f"  Nombre total d'échéances générées : {len(cal_data)}")
        print("  Extrait des 3 premières échéances de l'année :")
        for item in cal_data[:3]:
            print(f"    - {item['deadline']} [{item['type'].upper()}] : {item['title']} (Alerte J-14: {item['alert_j14']})")

        # 5. Test calc_inasti_provision
        print("\n[5/7] 💶 Test calc_inasti_provision (Revenu net 45 000 €)...")
        inasti_call = send_rpc("tools/call", {
            "name": "calc_inasti_provision",
            "arguments": {"annual_net_income": 45000.0, "is_starter": False, "year": 2026}
        })
        inasti_data = json.loads(inasti_call["result"]["content"][0]["text"])
        print("  Résultat de la simulation légale :")
        print(f"    • Cotisation de base trimestrielle : {inasti_data['quarterly_base_contribution']} €")
        print(f"    • Frais de caisse estimés (3,5 %)  : {inasti_data['quarterly_management_fee']} €")
        print(f"    • Total trimestriel à provisionner : {inasti_data['total_quarterly_due']} €")
        print(f"    • Total annuel estimé              : {inasti_data['annual_estimated_total']} €")
        print(f"    • Réf / Date d'application         : as_of {inasti_data['as_of']}")

        # 6. Test check_vat_vies (Live Network Call to European Commission)
        print("\n[6/7] 🌐 Test check_vat_vies (Appel REST en direct - Commission Européenne VIES)...")
        print("  Interrogation de ec.europa.eu pour le numéro BE 0202239951...")
        vies_call = send_rpc("tools/call", {
            "name": "check_vat_vies",
            "arguments": {"vat_number": "0202239951", "country_code": "BE"}
        })
        print("  Réponse en direct VIES :")
        print("  ", vies_call["result"]["content"][0]["text"])

        # 7. Test lookup_peppol_participant (Live Network Call to OpenPeppol Directory)
        print("\n[7/7] 📨 Test lookup_peppol_participant (Appel en direct - OpenPeppol Directory)...")
        print("  Interrogation de directory.peppol.eu pour le numéro 0202239951...")
        peppol_call = send_rpc("tools/call", {
            "name": "lookup_peppol_participant",
            "arguments": {"bce_number": "0202239951"}
        })
        print("  Réponse en direct Peppol :")
        print("  ", peppol_call["result"]["content"][0]["text"])

        print("\n==================================================================")
        print("✅ Tous les appels E2E JSON-RPC 2.0 stdio ont répondu avec succès !")
        print("==================================================================")

    finally:
        try:
            proc.stdin.close()
            proc.terminate()
            proc.wait(timeout=2)
        except Exception:
            pass


if __name__ == "__main__":
    run_e2e_live()
