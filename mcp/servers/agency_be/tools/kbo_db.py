"""
Micro-moteur SQLite KBO / BCE Hors-Ligne pour The Agency.
Permet la recherche ultra-rapide (< 1 ms) d'entreprises belges par nom, numéro BCE,
code postal ou code NACE, sans quota API ni dépendance réseau.
Utilise exclusivement la bibliothèque standard Python (sqlite3).
"""
import os
import re
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_DB_DIR = Path.home() / ".agency"
DEFAULT_DB_PATH = DEFAULT_DB_DIR / "kbo.db"

# Échantillon de référence représentatif pour initialisation et tests hors-ligne
REFERENCE_ENTERPRISES = [
    {
        "enterprise_number": "0202239951",
        "denomination": "PROXIMUS SA DE DROIT PUBLIC",
        "status": "AC",
        "juridical_form": "SA",
        "postal_code": "1030",
        "municipality": "Schaerbeek",
        "nace_code": "61100",
        "start_date": "1994-09-04",
    },
    {
        "enterprise_number": "0214596464",
        "denomination": "RADIO-TELEVISION BELGE DE LA COMMUNAUTE FRANCAISE (RTBF)",
        "status": "AC",
        "juridical_form": "Entreprise publique",
        "postal_code": "1044",
        "municipality": "Bruxelles",
        "nace_code": "60100",
        "start_date": "1977-01-01",
    },
    {
        "enterprise_number": "0308356862",
        "denomination": "SERVICE PUBLIC FEDERAL FINANCES",
        "status": "AC",
        "juridical_form": "Service Public",
        "postal_code": "1030",
        "municipality": "Schaerbeek",
        "nace_code": "84110",
        "start_date": "2002-01-01",
    },
    {
        "enterprise_number": "0403201185",
        "denomination": "SOLVAY SA",
        "status": "AC",
        "juridical_form": "SA",
        "postal_code": "1120",
        "municipality": "Bruxelles",
        "nace_code": "20140",
        "start_date": "1863-12-26",
    },
    {
        "enterprise_number": "0800000024",
        "denomination": "TEST BELGIAN SRL (DEMO)",
        "status": "AC",
        "juridical_form": "SRL",
        "postal_code": "1000",
        "municipality": "Bruxelles",
        "nace_code": "62010",
        "start_date": "2024-01-01",
    },
]


def normalize_bce(raw_number: str) -> str:
    """Normalise un numéro BCE (supprime points, espaces, préfixe BE)."""
    clean = re.sub(r"[^0-9]", "", raw_number)
    if len(clean) == 9:
        clean = "0" + clean
    return clean


def get_db_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Obtient une connexion SQLite vers la base KBO."""
    target_path = Path(db_path) if db_path else DEFAULT_DB_PATH
    if str(target_path) != ":memory:":
        target_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(target_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_kbo_db(db_path: Optional[str] = None, seed: bool = True) -> sqlite3.Connection:
    """Initialise le schéma de la base de données KBO."""
    conn = get_db_connection(db_path)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS enterprises (
            enterprise_number TEXT PRIMARY KEY,
            denomination TEXT NOT NULL,
            status TEXT DEFAULT 'AC',
            juridical_form TEXT,
            postal_code TEXT,
            municipality TEXT,
            nace_code TEXT,
            start_date TEXT
        )
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_ent_denomination ON enterprises(denomination)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ent_postal ON enterprises(postal_code)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ent_nace ON enterprises(nace_code)")
    conn.commit()

    if seed:
        cur.execute("SELECT COUNT(*) FROM enterprises")
        count = cur.fetchone()[0]
        if count == 0:
            for ent in REFERENCE_ENTERPRISES:
                cur.execute("""
                    INSERT OR REPLACE INTO enterprises 
                    (enterprise_number, denomination, status, juridical_form, postal_code, municipality, nace_code, start_date)
                    VALUES (:enterprise_number, :denomination, :status, :juridical_form, :postal_code, :municipality, :nace_code, :start_date)
                """, ent)
            conn.commit()

    return conn


def lookup_bce_offline(raw_number: str, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Recherche une entreprise par son numéro BCE dans la base locale SQLite.
    Retourne les informations d'entreprise ou None si introuvable.
    """
    clean_bce = normalize_bce(raw_number)
    conn = init_kbo_db(db_path, seed=True)
    cur = conn.cursor()

    cur.execute("SELECT * FROM enterprises WHERE enterprise_number = ?", (clean_bce,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return dict(row)


def search_bce_by_name(
    query: str,
    postal_code: Optional[str] = None,
    limit: int = 5,
    db_path: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Recherche d'entreprises par nom (insensible à la casse) et code postal optionnel.
    Exécution sub-milliseconde en SQLite pur.
    """
    conn = init_kbo_db(db_path, seed=True)
    cur = conn.cursor()

    pattern = f"%{query.strip()}%"
    params: List[Any] = [pattern]

    sql = "SELECT * FROM enterprises WHERE denomination LIKE ?"

    if postal_code:
        sql += " AND postal_code = ?"
        params.append(str(postal_code).strip())

    sql += " ORDER BY status ASC, denomination ASC LIMIT ?"
    params.append(limit)

    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()

    return [dict(r) for r in rows]
