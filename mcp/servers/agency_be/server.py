"""
Serveur MCP agency-be-mcp : Fournit les outils réglementaires et administratifs belges.
Protocole : Model Context Protocol (JSON-RPC 2.0 via stdio).
Zero-dependency externe : utilise uniquement la bibliothèque standard Python.
"""
import json
import sys
from typing import Any, Dict, List

from agency_be.tools.bce import validate_bce_number
from agency_be.tools.inasti import calc_inasti_provision
from agency_be.tools.peppol import lookup_peppol_participant
from agency_be.tools.tax_calendar import get_be_tax_calendar
from agency_be.tools.vies import check_vat_vies

SERVER_INFO = {
    "name": "agency-be-mcp",
    "version": "1.0.0",
}


def get_server_tools() -> List[Dict[str, Any]]:
    """
    Retourne la liste des schémas d'outils disponibles pour le serveur MCP.
    """
    return [
        {
            "name": "validate_bce_number",
            "description": (
                "Valide un numéro d'entreprise belge (BCE / KBO) avec l'algorithme "
                "officiel Modulo 97 et retourne le format canonique ainsi que le lien direct vers le registre public."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "bce_number": {
                        "type": "string",
                        "description": "Numéro d'entreprise avec ou sans points/préfixe (ex: 0202.239.951 ou BE 0202 239 951).",
                    }
                },
                "required": ["bce_number"],
            },
        },
        {
            "name": "check_vat_vies",
            "description": (
                "Vérifie la validité d'un numéro de TVA intracommunautaire (UE) "
                "via l'API REST officielle VIES de la Commission Européenne. "
                "Retourne la raison sociale et l'adresse enregistrée."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "vat_number": {
                        "type": "string",
                        "description": "Numéro de TVA sans le code pays (ou avec). Ex: 0202239951.",
                    },
                    "country_code": {
                        "type": "string",
                        "description": "Code pays ISO (2 lettres). Par défaut 'BE'.",
                        "default": "BE",
                    },
                },
                "required": ["vat_number"],
            },
        },
        {
            "name": "lookup_peppol_participant",
            "description": (
                "Interroge l'annuaire officiel OpenPeppol Directory pour vérifier "
                "si une entreprise belge est enregistrée pour la facturation électronique (Peppol UBL)."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "bce_number": {
                        "type": "string",
                        "description": "Numéro d'entreprise BCE à 10 chiffres.",
                    }
                },
                "required": ["bce_number"],
            },
        },
        {
            "name": "get_be_tax_calendar",
            "description": (
                "Génère le calendrier fiscal et social belge pour une année donnée : "
                "TVA trimestrielle (Intervat), Versements Anticipés (VA1 à VA4 - SPF Finances), "
                "et cotisations INASTI. Inclut les alertes proactives J-14 et J-3."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "year": {
                        "type": "integer",
                        "description": "Année fiscale concernée (ex: 2026).",
                        "default": 2026,
                    },
                    "regime": {
                        "type": "string",
                        "description": "Régime de TVA (trimestriel ou mensuel).",
                        "default": "trimestriel",
                    },
                },
            },
        },
        {
            "name": "calc_inasti_provision",
            "description": (
                "Simule les cotisations sociales trimestrielles provisionnelles d'un "
                "indépendant à titre principal en Belgique selon les tranches légales et seuils INASTI en vigueur."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "annual_net_income": {
                        "type": "number",
                        "description": "Revenu net imposable annuel estimé en euros.",
                    },
                    "is_starter": {
                        "type": "boolean",
                        "description": "True si indépendant débutant (3 premières années).",
                        "default": False,
                    },
                    "year": {
                        "type": "integer",
                        "description": "Année de cotisation.",
                        "default": 2026,
                    },
                },
                "required": ["annual_net_income"],
            },
        },
    ]


def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Any:
    """
    Exécute l'outil demandé avec ses arguments et retourne le résultat brut.
    """
    if name == "validate_bce_number":
        bce_number = arguments.get("bce_number", "")
        return validate_bce_number(bce_number)

    if name == "check_vat_vies":
        vat_number = arguments.get("vat_number", "")
        country_code = arguments.get("country_code", "BE")
        return check_vat_vies(vat_number=vat_number, country_code=country_code)

    if name == "lookup_peppol_participant":
        bce_number = arguments.get("bce_number", "")
        return lookup_peppol_participant(bce_number=bce_number)

    if name == "get_be_tax_calendar":
        year = int(arguments.get("year", 2026))
        regime = arguments.get("regime", "trimestriel")
        return get_be_tax_calendar(year=year, regime=regime)

    if name == "calc_inasti_provision":
        annual_net_income = float(arguments.get("annual_net_income", 0.0))
        is_starter = bool(arguments.get("is_starter", False))
        year = int(arguments.get("year", 2026))
        return calc_inasti_provision(
            annual_net_income=annual_net_income, is_starter=is_starter, year=year
        )

    raise ValueError(f"Outil inconnu : {name}")


def _send_response(response: Dict[str, Any]) -> None:
    body = json.dumps(response, ensure_ascii=False)
    sys.stdout.write(body + "\n")
    sys.stdout.flush()


def run_stdio_server() -> None:
    """
    Boucle principale stdio du serveur MCP.
    Prend en charge JSON-RPC 2.0 (initialize, tools/list, tools/call, ping).
    """
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue

        msg_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "initialize":
            _send_response({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": SERVER_INFO,
                    "capabilities": {
                        "tools": {"listChanged": False},
                    },
                },
            })
        elif method == "notifications/initialized":
            # Notification client sans réponse requise
            pass
        elif method == "ping":
            _send_response({"jsonrpc": "2.0", "id": msg_id, "result": {}})
        elif method == "tools/list":
            _send_response({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": get_server_tools(),
                },
            })
        elif method == "tools/call":
            tool_name = params.get("name", "")
            tool_args = params.get("arguments", {})
            try:
                result = handle_call_tool(tool_name, tool_args)
                _send_response({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, ensure_ascii=False, indent=2),
                            }
                        ]
                    },
                })
            except Exception as err:
                _send_response({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32603,
                        "message": str(err),
                    },
                })
        else:
            if msg_id is not None:
                _send_response({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32601,
                        "message": f"Méthode non implémentée : {method}",
                    },
                })


if __name__ == "__main__":
    run_stdio_server()
