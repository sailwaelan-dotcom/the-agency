"""
Validation et formatage du numéro d'entreprise belge BCE / KBO.
Algorithme officiel : Modulo 97 (SPF Economie).
"""
import re
from typing import Any, Dict


def validate_bce_number(bce_number: str) -> Dict[str, Any]:
    """
    Valide et normalise un numéro d'entreprise BCE (Banque-Carrefour des Entreprises).

    Règles de validation :
    - 10 chiffres (si 9 chiffres fournis, un zéro initial est ajouté).
    - Les deux derniers chiffres représentent la clé de contrôle : 97 - (8 premiers chiffres % 97).
    - Si le reste vaut 0, la clé attendue est 97.
    """
    if not isinstance(bce_number, str):
        return {"is_valid": False, "error": "invalid_type"}

    # Nettoyage : suppression de "BE", espaces, points, tirets
    clean = re.sub(r"^(?i:BE)", "", bce_number.strip())
    raw = re.sub(r"[^0-9]", "", clean)

    if len(raw) == 9:
        raw = "0" + raw

    if len(raw) != 10:
        return {"is_valid": False, "error": "invalid_length"}

    base_num = int(raw[:8])
    actual_checksum = int(raw[8:])

    remainder = base_num % 97
    expected_checksum = 97 - remainder if remainder != 0 else 97

    if actual_checksum != expected_checksum:
        return {
            "is_valid": False,
            "error": "checksum_mismatch",
            "expected_checksum": expected_checksum,
            "actual_checksum": actual_checksum,
            "normalized": raw,
        }

    formatted = f"BE {raw[:4]}.{raw[4:7]}.{raw[7:]}"
    kbo_url = f"https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html?numero={raw}"

    return {
        "is_valid": True,
        "normalized": raw,
        "formatted": formatted,
        "kbo_url": kbo_url,
        "checksum": actual_checksum,
    }
