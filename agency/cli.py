"""
Interface en Ligne de Commande (CLI) Solopreneur pour The Agency.
Permet d'exécuter directement les diagnostics et calculs belges
sans dépendance externe ni besoin d'un LLM ou d'un harness.
Exécution : python -m agency <commande>
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from agency.bootstrap import setup_environment

REPO_ROOT, APP_DIR = setup_environment()

from agency_be.tools.bce import validate_bce_number
from agency_be.tools.inasti import calc_inasti_provision
from agency_be.tools.tax_calendar import get_be_tax_calendar
from agency_be.tools.kbo_db import lookup_bce_offline, search_bce_by_name
from agency_be.tools.peppol import lookup_peppol_participant
from agency_be.tools.vies import check_vat_vies
from agency_be.tools.ubl_generator import generate_peppol_ubl_xml
from agency.vault import get_client, list_clients, save_client, delete_client, record_instinct, get_instincts


def cmd_bce(args):
    """Audit Modulo 97 et vérification KBO."""
    res = validate_bce_number(args.number)
    print("\n🇧🇪 Audit BCE / TVA Belge :")
    print(f"  • Numéro analysé : {args.number}")
    print(f"  • Numéro formaté : {res.get('formatted', 'N/A')}")
    print(f"  • Modulo 97      : {'✓ VALIDE' if res.get('is_valid') else '✗ INVALIDE'}")
    if not res.get("is_valid"):
        print(f"  • Erreur         : {res.get('error')}")
        sys.exit(1)

    # Consultation de la base KBO locale
    clean_bce = res.get("normalized", "")
    ent = lookup_bce_offline(clean_bce)
    if ent:
        print(f"  • Dénomination   : {ent.get('denomination')}")
        print(f"  • Forme juridique: {ent.get('juridical_form')}")
        print(f"  • Commune        : {ent.get('postal_code')} {ent.get('municipality')}")
        print(f"  • Code NACE-BEL  : {ent.get('nace_code')}")
    else:
        print("  • Données KBO    : Entreprise non indexée dans l'échantillon local.")

    print(f"  • Fiche KBO SPF  : {res.get('kbo_url')}\n")


def cmd_inasti(args):
    """Simulation de cotisations sociales trimestrielles INASTI."""
    res = calc_inasti_provision(
        annual_net_income=args.income,
        is_starter=args.starter,
        year=args.year,
    )
    print(f"\n🇧🇪 Cotisations Trimestrielles INASTI (Année {args.year}) :")
    print(f"  • Revenu net imposable annuel : {res['annual_net_income']:,.2f} €")
    print(f"  • Statut                      : {'Débutant (starter)' if res['is_starter'] else 'Normal'}")
    print(f"  • Cotisation de base          : {res['quarterly_base_contribution']:,.2f} € / trimestre")
    print(f"  • Frais de gestion caisse     : {res['quarterly_management_fee']:,.2f} €")
    print(f"  ───────────────────────────────────────────────")
    print(f"  ★ TOTAL TRIMESTRIEL DÛ        : {res['total_quarterly_due']:,.2f} €")
    print(f"  ★ TOTAL ANNUEL ESTIMÉ         : {res['annual_estimated_total']:,.2f} €\n")


def cmd_deadlines(args):
    """Affichage des échéances fiscales belges avec alertes."""
    events = get_be_tax_calendar(year=args.year, regime=args.regime)
    print(f"\n🇧🇪 Calendrier Fiscal & Social Belge {args.year} (Régime {args.regime}) :")
    for dead in events:
        print(f"\n  [{dead['deadline']}] {dead['title']}")
        print(f"    Type      : {dead['type']}")
        print(f"    Procédure : {dead['procedure']}")
        print(f"    Rappels   : J-14 ({dead['alert_j14']}) | J-3 ({dead['alert_j3']})")
    print()


def cmd_check_client(args):
    """Audit 3-en-1 : Modulo 97, VIES TVA UE, et Peppol Directory."""
    bce = args.bce
    print(f"\n🔍 Audit Global Client Belge : {bce}")

    # 1. BCE
    bce_res = validate_bce_number(bce)
    print(f"  [1/3] BCE Modulo 97  : {'✓ Conforme' if bce_res.get('is_valid') else '✗ Non-conforme'}")
    if not bce_res.get("is_valid"):
        print(f"        Arrêt : {bce_res.get('error')}\n")
        sys.exit(1)

    # 2. VIES
    clean_bce = bce_res.get("normalized", "")
    vies_res = check_vat_vies(clean_bce)
    vies_ok = vies_res.get("is_valid", False)
    print(f"  [2/3] VIES TVA UE    : {'✓ Valide (' + vies_res.get('name', '') + ')' if vies_ok else 'ℹ Non trouvé ou VIES indisponible'}")

    # 3. Peppol
    peppol_res = lookup_peppol_participant(clean_bce)
    peppol_ok = peppol_res.get("is_registered", False)
    print(f"  [3/3] Peppol B2B     : {'✓ Enregistré pour factures UBL' if peppol_ok else '✗ Non enregistré (recommandé inviter le client)'}")

    print("\n  ★ Diagnostic Solopreneur :")
    if peppol_ok:
        print("    -> Prêt pour émission de facture Peppol BIS 3.0 UBL 2.1 immédiate.")
    else:
        print("    -> Facture Peppol non routable automatiquement : envoi PDF avec avertissement requis.")
    print()


def cmd_vault(args):
    """Gestion du coffre-fort local RGPD."""
    subaction = args.vault_action

    if subaction == "list":
        clients = list_clients()
        print(f"\n🔐 Fiches Clients dans le Coffre ({len(clients)}) :")
        for c in clients:
            print(f"  • [{c['bce_number']}] {c['name']} (Délai : {c['payment_terms_days']}j, Peppol: {c['peppol_supported']})")
        print()

    elif subaction == "get":
        c = get_client(args.bce)
        if c:
            print(f"\n🔐 Client {c['bce_number']} :")
            for k, v in c.items():
                print(f"  • {k:<18} : {v}")
            print()
        else:
            print(f"\nClient '{args.bce}' non trouvé dans le coffre local.\n")

    elif subaction == "delete":
        ok = delete_client(args.bce)
        if ok:
            print(f"\nClient {args.bce} supprimé du coffre (droit à l'oubli appliqué).\n")
        else:
            print(f"\nClient {args.bce} introuvable.\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agency",
        description="The Agency — Boîte à outils CLI pour solopreneurs belges (zéro dépendance).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # bce
    p_bce = subparsers.add_parser("bce", help="Valider un numéro BCE avec Modulo 97 et consultation KBO.")
    p_bce.add_argument("number", help="Numéro BCE / TVA (ex: 0202.239.951)")

    # inasti
    p_inasti = subparsers.add_parser("inasti", help="Simuler les cotisations sociales trimestrielles.")
    p_inasti.add_argument("--income", type=float, required=True, help="Revenu net imposable annuel en euros")
    p_inasti.add_argument("--starter", action="store_true", help="Si indépendant débutant (< 3 ans)")
    p_inasti.add_argument("--year", type=int, default=2026, help="Année fiscale (défaut: 2026)")

    # deadlines
    p_deadlines = subparsers.add_parser("deadlines", help="Afficher les échéances fiscales belges.")
    p_deadlines.add_argument("--year", type=int, default=2026, help="Année fiscale")
    p_deadlines.add_argument("--regime", choices=["trimestriel", "mensuel"], default="trimestriel")

    # check-client
    p_check = subparsers.add_parser("check-client", help="Audit 3-en-1 d'un client (BCE + VIES + Peppol).")
    p_check.add_argument("bce", help="Numéro BCE du client")

    # vault
    p_vault = subparsers.add_parser("vault", help="Gestion du coffre-fort local RGPD.")
    v_sub = p_vault.add_subparsers(dest="vault_action", required=True)
    v_sub.add_parser("list", help="Lister les clients enregistrés")
    p_vg = v_sub.add_parser("get", help="Afficher un client par son numéro BCE")
    p_vg.add_argument("bce", help="Numéro BCE")
    p_vd = v_sub.add_parser("delete", help="Supprimer un client (droit à l'oubli)")
    p_vd.add_argument("bce", help="Numéro BCE")

    return parser


def main():
    if len(sys.argv) == 1:
        from agency.menu import launch_interactive_menu
        launch_interactive_menu()
        return

    # Route dédiée au serveur MCP stdio : c'est elle que la config MCP de l'exe
    # gelé référence (command=TheAgency.exe, args=["mcp"], voir install.py).
    if sys.argv[1] == "mcp":
        from agency_be.server import run_stdio_server
        run_stdio_server()
        return

    parser = build_parser()
    args = parser.parse_args()

    if args.command == "bce":
        cmd_bce(args)
    elif args.command == "inasti":
        cmd_inasti(args)
    elif args.command == "deadlines":
        cmd_deadlines(args)
    elif args.command == "check-client":
        cmd_check_client(args)
    elif args.command == "vault":
        cmd_vault(args)


if __name__ == "__main__":
    main()
