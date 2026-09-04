"""
Workflows et prompts déclaratifs MCP (MCP Prompts).
Fournit des chaînes d'instructions expertes prêtes à l'emploi pour les agents autonomes.
"""
from typing import Any, Dict, List

PROMPTS_CATALOG: List[Dict[str, Any]] = [
    {
        "name": "audit_client_peppol",
        "description": (
            "Workflow d'audit d'un client professionnel belge avant contractualisation et facturation : "
            "contrôle Modulo 97 BCE, statut TVA VIES et inscription sur l'annuaire OpenPeppol."
        ),
        "arguments": [
            {
                "name": "bce_number",
                "description": "Numéro d'entreprise BCE à 10 chiffres (ex: 0202.239.951).",
                "required": True,
            }
        ],
    },
    {
        "name": "prepare_quarterly_tax_closing",
        "description": (
            "Workflow de clôture trimestrielle pour solopreneur belge : "
            "cadrage des échéances TVA, vérification des versements anticipés (VA) et simulation INASTI."
        ),
        "arguments": [
            {
                "name": "quarter",
                "description": "Trimestre concerné (Q1, Q2, Q3, Q4).",
                "required": True,
            },
            {
                "name": "year",
                "description": "Année fiscale (par défaut 2026).",
                "required": False,
            },
        ],
    },
]


def get_server_prompts() -> List[Dict[str, Any]]:
    """Retourne la liste des prompts déclarés sur le serveur MCP."""
    return PROMPTS_CATALOG


def handle_get_prompt(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Génère les messages du prompt demandé avec ses arguments instanciés."""
    if name == "audit_client_peppol":
        bce_num = arguments.get("bce_number", "")
        return {
            "description": f"Audit de conformité client Peppol & BCE pour {bce_num}",
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": (
                            f"Réalise un audit complet de conformité pour l'entreprise cliente belge au numéro BCE {bce_num} :\n\n"
                            f"1. Valide le numéro BCE avec l'outil `validate_bce_number` (vérifie le Modulo 97 officiel).\n"
                            f"2. Vérifie la validité du numéro de TVA sur VIES via `check_vat_vies`.\n"
                            f"3. Interroge l'annuaire OpenPeppol via `lookup_peppol_participant` pour confirmer si le client "
                            f"peut recevoir des factures électroniques structurées UBL 2.1 (Peppol BIS 3.0).\n"
                            f"4. Rédige un compte-rendu clair précisant : raison sociale officielle, éligibilité Peppol "
                            f"et modalité de transmission obligatoire (Peppol ou PDF dérogatoire)."
                        ),
                    },
                }
            ],
        }

    if name == "prepare_quarterly_tax_closing":
        quarter = arguments.get("quarter", "Q1").upper()
        year = arguments.get("year", "2026")
        return {
            "description": f"Préparation de la clôture fiscale {quarter} {year}",
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": (
                            f"Prépare la feuille de route de clôture fiscale et sociale pour le trimestre {quarter} {year} :\n\n"
                            f"1. Utilise `get_be_tax_calendar` pour identifier les échéances exactes de TVA, de versement anticipé (VA) "
                            f"et de cotisation INASTI liées au trimestre {quarter}.\n"
                            f"2. Calcule les dates limites d'alerte de préparation (J-14) et d'exécution (J-3).\n"
                            f"3. Rappelle les communications structurées et les portails officiels (Intervat, MyMinfin, caisse d'assurances sociales).\n"
                            f"4. Propose la checklist d'archivage des pièces justificatives correspondantes."
                        ),
                    },
                }
            ],
        }

    raise ValueError(f"Prompt inconnu : {name}")
