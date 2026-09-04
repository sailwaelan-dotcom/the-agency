"""
Vérification des numéros de TVA intracommunautaires via l'API REST officielle VIES de la Commission Européenne.
"""
import json
import re
import ssl
import urllib.error
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


def build_vies_url(vat_number: str, country_code: str = "BE") -> str:
    """
    Construit l'URL de l'API REST officielle VIES pour un numéro de TVA et un État membre.
    """
    clean_country = country_code.strip().upper()
    # Nettoyage : uniquement caractères alphanumériques
    clean_vat = re.sub(r"[^0-9A-Za-z]", "", vat_number.strip())
    # Si le numéro commence par le code pays, le retirer du paramètre vat
    if clean_vat.upper().startswith(clean_country):
        clean_vat = clean_vat[len(clean_country):]

    return f"https://ec.europa.eu/taxation_customs/vies/rest-api/ms/{clean_country}/vat/{clean_vat}"


def check_vat_vies(vat_number: str, country_code: str = "BE", timeout: int = 10) -> Dict[str, Any]:
    """
    Interroge le service VIES de l'Union Européenne pour vérifier la validité d'un numéro de TVA.
    Retourne la raison sociale, l'adresse enregistrée et la date de la requête.
    """
    clean_country = country_code.strip().upper()
    clean_vat = re.sub(r"[^0-9A-Za-z]", "", vat_number.strip())
    if clean_vat.upper().startswith(clean_country):
        clean_vat = clean_vat[len(clean_country):]

    url = build_vies_url(vat_number=clean_vat, country_code=clean_country)

    try:
        req = urllib.request.Request(
            url,
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
            # Fallback compatible avec les mocks de tests sans argument context
            resp = urllib.request.urlopen(req, timeout=timeout)

        with resp as response:
            raw_data = response.read().decode("utf-8")
            data = json.loads(raw_data)

            return {
                "is_valid": bool(data.get("isValid", False)),
                "name": data.get("name"),
                "address": data.get("address"),
                "country_code": clean_country,
                "vat_number": clean_vat,
                "request_date": data.get("requestDate"),
                "user_error": data.get("userError"),
                "vies_url": url,
            }
    except Exception as exc:
        return {
            "is_valid": False,
            "error": str(exc),
            "country_code": clean_country,
            "vat_number": clean_vat,
            "vies_url": url,
        }
