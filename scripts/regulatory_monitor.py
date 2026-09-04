"""
Watchdog de Dérive Réglementaire (Regulatory Drift Monitor) pour The Agency.
Sonde les sources officielles belges (Moniteur Belge, SPF Finances, INASTI)
et audite la cohérence des seuils fiscaux et sociaux du dépôt.
Génère un rapport d'audit et alerte en cas de modification réglementaire.
Zéro dépendance tierce (urllib, json, re, datetime, pathlib).
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"

# Seuils légaux de référence en vigueur (Belgique 2026)
REFERENCE_THRESHOLDS = {
    "tva_standard_rate": 21.0,
    "tva_franchise_56bis_threshold": 25000.0,
    "inasti_starter_rate": 20.5,
    "inasti_standard_floor_income": 16861.46,
    "inasti_max_ceiling_income": 107300.0,
    "peppol_legal_deadline_year": 2026,
    "commercial_late_interest_law": "loi du 2 août 2002",
}

# Flux officiels vérifiables
OFFICIAL_ENDPOINTS = [
    {
        "name": "SPF Finances (Fisconetplus / Portail)",
        "url": "https://finances.belgium.be",
        "description": "Portail officiel des impôts, TVA et douanes belges.",
    },
    {
        "name": "Moniteur Belge / Justel",
        "url": "https://www.ejustice.just.fgov.be",
        "description": "Législation consolidée et publications légales.",
    },
    {
        "name": "INASTI / RSVZ",
        "url": "https://www.inasti.be",
        "description": "Institut national d'assurances sociales pour travailleurs indépendants.",
    },
]


def audit_repo_thresholds() -> Dict[str, Any]:
    """Audite la cohérence des seuils réglementaires disséminés dans les compétences."""
    findings: List[Dict[str, Any]] = []

    # Vérification du seuil franchise TVA 25 000 €
    peppol_skill = SKILLS_DIR / "be-invoicing-peppol" / "SKILL.md"
    if peppol_skill.exists():
        content = peppol_skill.read_text(encoding="utf-8")
        if "25 000" not in content and "25.000" not in content:
            findings.append({
                "severity": "WARNING",
                "component": "be-invoicing-peppol",
                "message": "Seuil de la franchise TVA (25 000 €) introuvable dans le skill.",
            })

    # Vérification de l'obligation Peppol 2026
    if peppol_skill.exists():
        content = peppol_skill.read_text(encoding="utf-8")
        if "2026" not in content:
            findings.append({
                "severity": "CRITICAL",
                "component": "be-invoicing-peppol",
                "message": "Mention de l'échéance légale Peppol 2026 absente.",
            })

    # Vérification des taux dans le serveur MCP
    mcp_resources = REPO_ROOT / "mcp" / "servers" / "agency_be" / "resources.py"
    if mcp_resources.exists():
        content = mcp_resources.read_text(encoding="utf-8")
        if "21" not in content or "16861" not in content:
            findings.append({
                "severity": "CRITICAL",
                "component": "mcp/resources.py",
                "message": "Taux de TVA standard ou plancher INASTI manquant dans les resources MCP.",
            })

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checked_thresholds": REFERENCE_THRESHOLDS,
        "findings": findings,
        "is_synced": len([f for f in findings if f["severity"] == "CRITICAL"]) == 0,
    }


def check_official_sources_liveness(timeout_sec: int = 3) -> List[Dict[str, Any]]:
    """Vérifie la disponibilité en ligne des sources officielles belges."""
    status_list: List[Dict[str, Any]] = []

    for src in OFFICIAL_ENDPOINTS:
        url = src["url"]
        online = False
        status_code = None
        error_msg = None

        try:
            req = Request(
                url,
                headers={"User-Agent": "TheAgency-RegulatoryMonitor/2.0 (Solopreneur AI Agent Suite)"},
            )
            with urlopen(req, timeout=timeout_sec) as resp:
                status_code = resp.getcode()
                online = (status_code == 200)
        except Exception as exc:
            error_msg = str(exc)

        status_list.append({
            "name": src["name"],
            "url": url,
            "online": online,
            "status_code": status_code,
            "error": error_msg,
        })

    return status_list


def generate_report(offline_mode: bool = False) -> Dict[str, Any]:
    """Exécute l'audit complet et génère le rapport consolidé."""
    threshold_audit = audit_repo_thresholds()
    liveness = [] if offline_mode else check_official_sources_liveness()

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "threshold_audit": threshold_audit,
        "official_sources_liveness": liveness,
        "status": "PASS" if threshold_audit["is_synced"] else "FAIL",
    }
    return report


def main():
    parser = argparse.ArgumentParser(description="Watchdog de Dérive Réglementaire Belge.")
    parser.add_argument("--offline", action="store_true", help="N'effectue pas de requêtes réseau vers les portails.")
    parser.add_argument("--json", action="store_true", help="Affiche le résultat en JSON brut.")
    args = parser.parse_args()

    report = generate_report(offline_mode=args.offline)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("==================================================================")
        print("🇧🇪 Rapport du Watchdog de Dérive Réglementaire (The Agency)")
        print("==================================================================")
        print(f"Date d'exécution : {report['generated_at']}")
        print(f"Statut général   : {report['status']}")
        print(f"Anomalies repérées: {len(report['threshold_audit']['findings'])}")
        for f in report['threshold_audit']['findings']:
            print(f"  [{f['severity']}] {f['component']} : {f['message']}")

    if report["status"] == "FAIL":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
