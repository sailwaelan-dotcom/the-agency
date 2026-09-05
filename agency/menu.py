"""
Menu Interactif TUI Zéro-Code pour The Agency.
Permet aux solopreneurs belges d'exécuter toutes les fonctionnalités
dans un assistant guidé simple, sans ligne de commande complexe.
"""
from pathlib import Path

from agency.bootstrap import setup_environment

setup_environment()

from agency.vault import list_clients
from agency_be.tools.bce import validate_bce_number
from agency_be.tools.inasti import calc_inasti_provision
from agency_be.tools.kbo_db import lookup_bce_offline
from agency_be.tools.peppol import lookup_peppol_participant
from agency_be.tools.tax_calendar import get_be_tax_calendar
from agency_be.tools.ubl_generator import generate_peppol_ubl_xml
from agency_be.tools.vies import check_vat_vies


def prompt_float(message: str, default: float) -> float:
    """Demande un nombre décimal à l'utilisateur de manière sécurisée et tolérante."""
    while True:
        raw = input(f"{message} [{default:,.2f}] : ").strip()
        if not raw:
            return default
        cleaned = raw.replace(" ", "").replace(",", ".")
        try:
            val = float(cleaned)
            if val >= 0:
                return val
            print("  ⚠️ Veuillez saisir un montant positif ou nul.")
        except ValueError:
            print("  ⚠️ Montant invalide. Veuillez saisir un nombre (ex: 45000 ou 1500.50).")


def banner():
    print("""
==================================================================
🇧🇪 THE AGENCY — Assistant Solopreneur Belgique
Boîte à outils d'agents & conformité administrative déterministe
==================================================================
""")


def menu_check_client():
    print("\n--- 🔍 VÉRIFICATION D'UN CLIENT OU PROSPECT ---")
    raw = input("Entrez le numéro d'entreprise BCE ou TVA (ex: 0202.239.951) : ").strip()
    if not raw:
        return

    # 1. BCE Modulo 97
    res = validate_bce_number(raw)
    if not res.get("is_valid"):
        print(f"\n❌ Numéro invalide : {res.get('error')}")
        return

    clean_bce = res["normalized"]
    print(f"\n✓ Numéro BCE valide : {res['formatted']}")

    # 2. KBO Offline
    ent = lookup_bce_offline(clean_bce)
    if ent:
        print(f"  • Raison sociale  : {ent.get('denomination')}")
        print(f"  • Localisation    : {ent.get('postal_code')} {ent.get('municipality')}")
        print(f"  • Code NACE-BEL   : {ent.get('nace_code')}")

    # 3. VIES TVA
    print("  • Vérification TVA UE (VIES)...", end=" ", flush=True)
    vies = check_vat_vies(clean_bce)
    if vies.get("is_valid"):
        print(f"✓ Assujetti ({vies.get('name', '')})")
    else:
        print("ℹ Non trouvé au VIES ou indisponible")

    # 4. Peppol B2B
    print("  • Vérification Peppol B2B...", end=" ", flush=True)
    peppol = lookup_peppol_participant(clean_bce)
    if peppol.get("is_registered"):
        print("✓ Enregistré (Facturation électronique UBL possible)")
    else:
        print("✗ Non enregistré dans l'annuaire Peppol")

    print(f"\nLien vers la fiche KBO officielle : {res.get('kbo_url')}\n")


def menu_inasti():
    print("\n--- 💰 SIMULATION DES COTISATIONS SOCIALES INASTI ---")
    income = prompt_float("Revenu net imposable annuel estimé en €", 40000.0)

    st_str = input("Êtes-vous indépendant débutant (< 3 ans) ? (o/n) [n] : ").strip().lower()
    is_starter = (st_str == "o" or st_str == "oui")

    res = calc_inasti_provision(annual_net_income=income, is_starter=is_starter)
    print(f"\n★ RÉSULTAT DE LA SIMULATION (as_of {res['year']} — Barèmes INASTI) :")
    print(f"  • Revenu net annuel pris en compte : {res['annual_net_income']:,.2f} €")
    print(f"  • Cotisation de base trimestrielle : {res['quarterly_base_contribution']:,.2f} €")
    print(f"  • Frais de gestion de caisse       : {res['quarterly_management_fee']:,.2f} €")
    print(f"  ───────────────────────────────────────────────")
    print(f"  ★ TOTAL TRIMESTRIEL À PAYER        : {res['total_quarterly_due']:,.2f} €")
    print(f"  ★ CHARGE ANNUELLE ESTIMÉE          : {res['annual_estimated_total']:,.2f} €")
    print(f"  ───────────────────────────────────────────────")
    print(f"  ℹ️ Information indicative générale (as_of {res['year']}).")
    print("     Ne constitue pas un conseil comptable personnalisé.")
    print("     Vérifiez toujours vos cotisations définitives auprès de votre")
    print("     caisse d'assurances sociales ou de votre expert-comptable ITAA.\n")


def menu_deadlines():
    print("\n--- 📅 ÉCHÉANCIER FISCAL & SOCIAL BELGE (as_of 2026) ---")
    events = get_be_tax_calendar()
    for dead in events:
        print(f"[{dead['deadline']}] {dead['title']}")
        print(f"   Action  : {dead['procedure']}")
        print(f"   Alertes : J-14 ({dead['alert_j14']}) | J-3 ({dead['alert_j3']})\n")
    print("ℹ️ Dates indicatives officielles (as_of 2026). Vérifiez toujours sur MyMinfin / Intervat.\n")


def menu_ubl():
    print("\n--- 🧾 GÉNÉRATEUR DE FACTURE PEPPOL BIS 3.0 UBL 2.1 ---")
    seller_bce = input("Votre numéro BCE (émetteur) [0202239951] : ").strip() or "0202239951"
    buyer_bce = input("Numéro BCE du client (acheteur) [0403201185] : ").strip() or "0403201185"
    amount = prompt_float("Montant HTVA de la prestation en €", 1500.00)

    invoice_data = {
        "invoice_number": "INV-2026-001",
        "issue_date": "2026-04-01",
        "due_date": "2026-05-01",
        "supplier": {
            "bce_number": seller_bce,
            "name": "Mon Entreprise Solopreneur",
            "street": "Avenue Louise 100",
            "postal_code": "1000",
            "city": "Bruxelles",
            "iban": "[IBAN_FOURNISSEUR]",
        },
        "customer": {
            "bce_number": buyer_bce,
            "name": "Client Entreprise SRL",
            "street": "Rue de la Loi 1",
            "postal_code": "1000",
            "city": "Bruxelles",
        },
        "lines": [
            {
                "id": "1",
                "name": "Prestation de conseil stratégique",
                "description": "Accompagnement et livrables",
                "quantity": 1.0,
                "unit_price": amount,
                "vat_rate": 0.21,
            }
        ],
    }

    res = generate_peppol_ubl_xml(invoice_data)
    # Écriture dans le répertoire de travail courant de l'utilisateur (jamais dans _MEIPASS temporaire)
    out_file = Path.cwd() / f"facture_{res['invoice_number']}.xml"
    out_file.write_text(res["xml"], encoding="utf-8")
    print(f"\n✓ Facture XML Peppol générée avec succès : {out_file}")
    print(f"  • Total HTVA : {res['total_htva']:.2f} €")
    print(f"  • TVA (21 %) : {res['total_tva']:.2f} €")
    print(f"  • Total TTC  : {res['total_ttc']:.2f} €")
    print(f"\nℹ️ Facture conforme norme EN 16931 / Peppol BIS Billing 3.0 (as_of 2026).")
    print(f"   Format obligatoire pour les transactions B2B en Belgique.\n")


def menu_vault():
    print("\n--- 🔐 COFFRE-FORT LOCAL RGPD (Clients enregistrés) ---")
    clients = list_clients()
    if not clients:
        print("Aucun client enregistré pour l'instant dans ~/.agency/vault/\n")
        return
    for c in clients:
        print(f"• [{c['bce_number']}] {c['name']} (Délai : {c['payment_terms_days']} jours, TVA : {c['vat_regime']})")
    print()


def menu_configure():
    print("\n--- ⚙️ CONFIGURATION DES HARNESSES IA ---")
    from install import run_full_installation
    run_full_installation(interactive=True)


def menu_create_shortcut():
    print("\n--- 📌 CRÉATION DE RACCOURCI SUR LE BUREAU ---")
    from install import create_desktop_shortcut
    ok, path_or_msg = create_desktop_shortcut()
    if ok:
        print(f"✓ Raccourci créé sur votre Bureau : {path_or_msg}\n")
    else:
        print(f"✗ Impossible de créer le raccourci : {path_or_msg}\n")


def launch_interactive_menu():
    """Boucle principale du menu interactif."""
    while True:
        banner()
        print("Que souhaitez-vous faire ?\n")
        print("  [1] 🔍 Vérifier un client ou prospect (BCE, TVA, Peppol)")
        print("  [2] 💰 Simuler mes cotisations trimestrielles INASTI")
        print("  [3] 📅 Consulter mes prochaines échéances fiscales")
        print("  [4] 🧾 Générer une facture électronique Peppol BIS 3.0 UBL")
        print("  [5] 🔐 Consulter mon coffre-fort local RGPD")
        print("  [6] ⚙️  Configurer mes applications IA (Claude Desktop, Cursor...)")
        print("  [7] 📌 Créer un raccourci The Agency sur mon Bureau")
        print("  [0] 🚪 Quitter\n")

        try:
            choice = input("Votre choix (0-7) : ").strip()
            if choice == "0":
                print("\nAu revoir et bon succès dans votre activité solopreneur ! 🇧🇪\n")
                break
            elif choice == "1":
                menu_check_client()
            elif choice == "2":
                menu_inasti()
            elif choice == "3":
                menu_deadlines()
            elif choice == "4":
                menu_ubl()
            elif choice == "5":
                menu_vault()
            elif choice == "6":
                menu_configure()
            elif choice == "7":
                menu_create_shortcut()
            else:
                print("\nOption invalide, veuillez choisir un chiffre entre 0 et 7.\n")

            input("\nAppuyez sur [Entrée] pour revenir au menu...")
        except (KeyboardInterrupt, EOFError):
            print("\n\nInterruption reçue. Au revoir !\n")
            break
