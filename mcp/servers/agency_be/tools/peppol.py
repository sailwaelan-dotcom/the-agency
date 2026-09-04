"""
Vérification d'enregistrement sur le réseau Peppol via l'annuaire public OpenPeppol Directory.
Format d'identifiant participant belge : iso6523-actorid-upis::0208:<BCE_10_chiffres>.
"""
import json
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict


def _get_ssl_context() -> Any:
    """Construit un contexte SSL sécurisé avec les certificats système ou certifi."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        try:
            return ssl.create_default_context()
        except Exception:
            return None


def build_peppol_participant_id(bce_number: str, scheme: str = "0208") -> str:
    """
    Construit l'identifiant Peppol standard pour une entreprise belge.
    Schéma officiel : 0208 (Numéro d'entreprise BCE).
    """
    clean = re.sub(r"^(?i:BE)", "", bce_number.strip())
    raw = re.sub(r"[^0-9]", "", clean)
    if len(raw) == 9:
        raw = "0" + raw
    return f"iso6523-actorid-upis::{scheme}:{raw}"


def lookup_peppol_participant(bce_number: str, timeout: int = 10) -> Dict[str, Any]:
    """
    Interroge l'annuaire Peppol Directory (directory.peppol.eu) pour vérifier
    si une entreprise est enregistrée pour recevoir des factures électroniques UBL.
    """
    clean = re.sub(r"^(?i:BE)", "", bce_number.strip())
    raw = re.sub(r"[^0-9]", "", clean)
    if len(raw) == 9:
        raw = "0" + raw

    expected_pid = build_peppol_participant_id(raw)
    query_url = f"https://directory.peppol.eu/search/1.0/json?q={urllib.parse.quote(raw)}"

    try:
        req = urllib.request.Request(
            query_url,
            headers={
                "User-Agent": "TheAgency-MCP/1.0 (Belgian Solopreneurs Open-Source)",
                "Accept": "application/json",
            },
        )

        ctx = _get_ssl_context()
        open_kwargs = {"timeout": timeout}
        if ctx is not None:
            open_kwargs["context"] = ctx

        try:
            resp = urllib.request.urlopen(req, **open_kwargs)
        except TypeError:
            resp = urllib.request.urlopen(req, timeout=timeout)

        with resp as response:
            data = json.loads(response.read().decode("utf-8"))
            matches = data.get("matches", [])

            if not matches:
                return {
                    "is_registered": False,
                    "bce_number": raw,
                    "participant_id": expected_pid,
                    "entity_name": None,
                    "directory_url": query_url,
                }

            # Recherche du match correspondant
            target_match = matches[0]
            for m in matches:
                pid_info = m.get("participantID", {})
                scheme = pid_info.get("scheme", "")
                val = pid_info.get("value", "")
                full_pid = f"{scheme}::{val}" if scheme and val else ""
                if full_pid == expected_pid or val == f"0208:{raw}":
                    target_match = m
                    break

            # Extraction de la raison sociale (supporte les formats 'name' et 'value')
            entities = target_match.get("entities", [])
            entity_name = "Inconnu"
            if entities:
                names = entities[0].get("name", [])
                if names:
                    first_item = names[0]
                    entity_name = first_item.get("name") or first_item.get("value") or "Inconnu"

            pid_dict = target_match.get("participantID", {})
            full_pid = f"{pid_dict.get('scheme', 'iso6523-actorid-upis')}::{pid_dict.get('value', f'0208:{raw}')}"

            return {
                "is_registered": True,
                "bce_number": raw,
                "participant_id": full_pid,
                "entity_name": entity_name,
                "directory_url": query_url,
                "raw_match": target_match,
            }
    except Exception as exc:
        return {
            "is_registered": False,
            "bce_number": raw,
            "participant_id": expected_pid,
            "entity_name": None,
            "error": str(exc),
            "directory_url": query_url,
        }
