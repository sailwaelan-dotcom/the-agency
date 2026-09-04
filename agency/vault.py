"""
Vault RGPD & Mémoire Épistémique Locale pour The Agency.
Stocke hors-dépôt (~/.agency/vault/) l'annuaire des clients et les règles métiers apprises (instincts).
Conformité stricte APD / RGPD : droit à l'oubli, isolation locale, aucune transmission Cloud.
Zéro dépendance tierce (json, os, pathlib, datetime, re).
"""
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_VAULT_DIR = Path.home() / ".agency" / "vault"


def get_vault_dir() -> Path:
    """Retourne le répertoire configuré du coffre-fort local."""
    custom = os.getenv("AGENCY_VAULT_DIR")
    target = Path(custom) if custom else DEFAULT_VAULT_DIR
    target.mkdir(parents=True, exist_ok=True)
    return target


def _normalize_bce(raw_number: str) -> str:
    clean = re.sub(r"[^0-9]", "", str(raw_number))
    if len(clean) == 9:
        clean = "0" + clean
    return clean


# =====================================================================
# Compartiment 1 : Annuaire Sécurisé des Clients (entities.jsonl)
# =====================================================================

def save_client(client_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enregistre ou met à jour une fiche client dans le coffre local.
    Garantit l'unicité par numéro BCE normalisé.
    """
    vault = get_vault_dir()
    entities_file = vault / "entities.jsonl"

    raw_bce = client_data.get("bce_number", "")
    clean_bce = _normalize_bce(raw_bce)
    if not clean_bce or len(clean_bce) != 10:
        raise ValueError(f"Numéro BCE invalide pour le coffre : '{raw_bce}'")

    record = {
        "bce_number": clean_bce,
        "name": client_data.get("name", "Client Inconnu").strip(),
        "vat_number": f"BE{clean_bce}",
        "vat_regime": client_data.get("vat_regime", "normal"),
        "payment_terms_days": int(client_data.get("payment_terms_days", 30)),
        "peppol_supported": bool(client_data.get("peppol_supported", True)),
        "notes": client_data.get("notes", "").strip(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    # Lecture des entités existantes et remplacement ou ajout
    existing: List[Dict[str, Any]] = []
    if entities_file.exists():
        for line in entities_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    obj = json.loads(line)
                    if obj.get("bce_number") != clean_bce:
                        existing.append(obj)
                except Exception:
                    continue

    existing.append(record)

    # Réécriture atomique
    with entities_file.open("w", encoding="utf-8") as f:
        for ent in existing:
            f.write(json.dumps(ent, ensure_ascii=False) + "\n")

    return record


def get_client(raw_bce: str) -> Optional[Dict[str, Any]]:
    """Recherche un client par son numéro BCE dans le coffre local."""
    clean_bce = _normalize_bce(raw_bce)
    vault = get_vault_dir()
    entities_file = vault / "entities.jsonl"

    if not entities_file.exists():
        return None

    for line in entities_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                obj = json.loads(line)
                if obj.get("bce_number") == clean_bce:
                    return obj
            except Exception:
                continue

    return None


def list_clients(limit: int = 50) -> List[Dict[str, Any]]:
    """Liste les clients enregistrés dans le coffre local."""
    vault = get_vault_dir()
    entities_file = vault / "entities.jsonl"

    if not entities_file.exists():
        return []

    clients: List[Dict[str, Any]] = []
    for line in entities_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                clients.append(json.loads(line))
            except Exception:
                continue

    return clients[:limit]


def delete_client(raw_bce: str) -> bool:
    """
    Supprime un client du coffre local (Droit à l'oubli / RGPD).
    Retourne True si un client a été supprimé, False sinon.
    """
    clean_bce = _normalize_bce(raw_bce)
    vault = get_vault_dir()
    entities_file = vault / "entities.jsonl"

    if not entities_file.exists():
        return False

    found = False
    retained: List[Dict[str, Any]] = []

    for line in entities_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                obj = json.loads(line)
                if obj.get("bce_number") == clean_bce:
                    found = True
                else:
                    retained.append(obj)
            except Exception:
                continue

    if found:
        with entities_file.open("w", encoding="utf-8") as f:
            for ent in retained:
                f.write(json.dumps(ent, ensure_ascii=False) + "\n")

    return found


# =====================================================================
# Compartiment 2 : Instincts & Règles Métiers Apprises (instincts.jsonl)
# =====================================================================

def record_instinct(topic: str, rule: str, confidence: float = 1.0) -> Dict[str, Any]:
    """Enregistre un instinct ou une habitude métier apprise par l'agent."""
    vault = get_vault_dir()
    instincts_file = vault / "instincts.jsonl"

    instinct = {
        "topic": topic.strip().lower(),
        "rule": rule.strip(),
        "confidence": min(1.0, max(0.1, float(confidence))),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    with instincts_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(instinct, ensure_ascii=False) + "\n")

    return instinct


def get_instincts(topic: Optional[str] = None) -> List[Dict[str, Any]]:
    """Récupère la liste des instincts enregistrés, filtrés par sujet optionnel."""
    vault = get_vault_dir()
    instincts_file = vault / "instincts.jsonl"

    if not instincts_file.exists():
        return []

    results: List[Dict[str, Any]] = []
    search_topic = topic.strip().lower() if topic else None

    for line in instincts_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                obj = json.loads(line)
                if not search_topic or search_topic in obj.get("topic", ""):
                    results.append(obj)
            except Exception:
                continue

    return results
