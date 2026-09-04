"""
Guardrails d'Exécution & Intercepteur Runtime pour The Agency (agency-be-mcp).
Assure un contrôle pré-vol déterministe avant chaque opération et la désensibilisation en sortie.
"""
import re
from typing import Any, Dict, Optional, Tuple

from agency_be.tools.bce import validate_bce_number

LEGAL_VAT_RATES = {0.21, 0.12, 0.06, 0.00}

# Motifs de détection des données sensibles
NISS_PATTERN = re.compile(r"\b\d{2}\.\d{2}\.\d{2}-\d{3}\.\d{2}\b")
WINDOWS_USER_PATH_PATTERN = re.compile(r"[a-zA-Z]:\\[Uu]sers\\[a-zA-Z0-9_.-]+")
UNIX_USER_PATH_PATTERN = re.compile(r"/home/[a-zA-Z0-9_.-]+")


def validate_preflight(tool_name: str, arguments: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Vérifie les arguments d'un outil avant son exécution.
    Bloque toute opération basée sur un numéro d'entreprise mathématiquement erroné
    ou un taux fiscal non légal en Belgique.
    """
    # 1. Vérification du numéro BCE pour les outils opérationnels (lookup Peppol, VIES)
    if tool_name in {"lookup_peppol_participant", "check_vat_vies"}:
        bce_input = arguments.get("bce_number") or arguments.get("vat_number")
        if bce_input and isinstance(bce_input, str):
            clean_bce = re.sub(r"^(?i:BE)", "", bce_input.strip())
            raw_digits = re.sub(r"[^0-9]", "", clean_bce)
            if len(raw_digits) in (9, 10):
                val_res = validate_bce_number(raw_digits)
                if not val_res.get("is_valid", False):
                    exp = val_res.get("expected_checksum")
                    act = val_res.get("actual_checksum")
                    return (
                        False,
                        f"Guardrail d'exécution : Numéro BCE '{bce_input}' invalide selon l'algorithme Modulo 97 "
                        f"(clé attendue : {exp}, reçue : {act}). Opération bloquée.",
                    )

    # 2. Vérification des taux de TVA pour la génération Peppol UBL
    if tool_name == "generate_peppol_ubl":
        invoice_data = arguments.get("invoice_data", {})
        lines = invoice_data.get("lines", [])
        for idx, line in enumerate(lines, start=1):
            rate = float(line.get("vat_rate", 0.21))
            if rate not in LEGAL_VAT_RATES:
                return (
                    False,
                    f"Guardrail d'exécution : Taux TVA {rate} (ligne {idx}) non conforme en Belgique. "
                    f"Taux légaux autorisés : 21% (0.21), 12% (0.12), 6% (0.06), 0% (0.00). "
                    f"Fondement : Arrêté Royal n° 20 du Code de la TVA.",
                )

    return True, None


def _sanitize_string(text: str) -> str:
    """Applique les masquages de sécurité sur une chaîne de caractères."""
    clean = NISS_PATTERN.sub("[REGISTRE_NATIONAL_MASQUE]", text)
    clean = WINDOWS_USER_PATH_PATTERN.sub("[CHEMIN_MACHINE_MASQUE]", clean)
    clean = UNIX_USER_PATH_PATTERN.sub("[CHEMIN_MACHINE_MASQUE]", clean)
    return clean


def sanitize_postflight(data: Any) -> Any:
    """
    Parcourt récursivement la charge de données et neutralise toute donnée personnelle (NISS)
    ou chemin machine local avant envoi au LLM ou journalisation.
    """
    if isinstance(data, str):
        return _sanitize_string(data)
    if isinstance(data, dict):
        return {k: sanitize_postflight(v) for k, v in data.items()}
    if isinstance(data, list):
        return [sanitize_postflight(item) for item in data]
    return data
