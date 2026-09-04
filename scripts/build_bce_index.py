"""
Script d'indexation KBO / BCE Open Data pour The Agency.
Permet d'initialiser ou de mettre à jour la base SQLite locale (~/.agency/kbo.db)
à partir des exports Open Data officiels du SPF Economie (enterprise.csv, address.csv, activity.csv).
Zéro dépendance tierce (sqlite3, csv, urllib, zipfile).
"""
import argparse
import csv
import io
import os
import re
import sqlite3
import sys
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from mcp.servers.agency_be.tools.kbo_db import DEFAULT_DB_PATH, init_kbo_db, normalize_bce


def parse_args():
    parser = argparse.ArgumentParser(description="Constructeur d'index SQLite KBO / BCE Open Data.")
    parser.add_argument(
        "--db",
        default=str(DEFAULT_DB_PATH),
        help=f"Chemin cible de la base SQLite (défaut : {DEFAULT_DB_PATH})",
    )
    parser.add_argument(
        "--seed-only",
        action="store_true",
        help="Initialise uniquement la base avec les entreprises de référence sans télécharger de dump lourd.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    db_path = Path(args.db)
    print(f"Initialisation de la base KBO SQLite sur : {db_path}")

    conn = init_kbo_db(str(db_path), seed=True)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM enterprises")
    count = cur.fetchone()[0]
    conn.close()

    print(f"Base KBO prête : {count} entreprise(s) enregistrée(s).")
    print("Prête pour utilisation déterministe hors-ligne avec search_bce_by_name.")


if __name__ == "__main__":
    main()
