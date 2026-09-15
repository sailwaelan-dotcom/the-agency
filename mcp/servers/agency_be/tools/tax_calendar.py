"""
Générateur de calendrier fiscal et social belge pour solopreneurs.
Couvre les échéances SPF Finances (TVA, Versements Anticipés) et INASTI.

Échéances TVA périodiques (as_of 2026-09 — SPF Finances, « La nouvelle chaîne TVA » §2 et §10.1,
calendrier TVA) :
- trimestriel : dépôt + paiement au plus tard le 25 du mois qui suit le trimestre, sans report
  si le 25 tombe un samedi, un dimanche ou un jour férié légal ;
- mensuel : dépôt + paiement au plus tard le 20 du mois suivant, reporté au jour ouvrable
  suivant si le 20 tombe un samedi, un dimanche ou un jour férié légal.
"""
from datetime import date, timedelta
from typing import Any, Dict, List, Set

REGIMES_TVA = ("trimestriel", "mensuel")
MOIS = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre")
PROCEDURE_TVA = "Dépôt déclaration Intervat + paiement sur compte SPF Finances avec communication structurée"


def _format_event(
    event_id: str,
    event_type: str,
    title: str,
    deadline: date,
    procedure: str,
    details: str = "",
) -> Dict[str, Any]:
    return {
        "id": event_id,
        "type": event_type,
        "title": title,
        "deadline": deadline.isoformat(),
        "alert_j14": (deadline - timedelta(days=14)).isoformat(),
        "alert_j3": (deadline - timedelta(days=3)).isoformat(),
        "procedure": procedure,
        "details": details,
    }


def _paques(annee: int) -> date:
    """Dimanche de Pâques (calendrier grégorien, algorithme de Meeus/Jones/Butcher)."""
    a = annee % 19
    b, c = divmod(annee, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    ll = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * ll) // 451
    mois, jour = divmod(h + ll - 7 * m + 114, 31)
    return date(annee, mois, jour + 1)


def _jours_feries_legaux(annee: int) -> Set[date]:
    """Les 10 jours fériés légaux belges : 1er janvier, lundi de Pâques, 1er mai, Ascension,
    lundi de Pentecôte, 21 juillet, 15 août, 1er novembre, 11 novembre, 25 décembre."""
    paques = _paques(annee)
    return {
        date(annee, 1, 1), paques + timedelta(days=1), date(annee, 5, 1),
        paques + timedelta(days=39), paques + timedelta(days=50), date(annee, 7, 21),
        date(annee, 8, 15), date(annee, 11, 1), date(annee, 11, 11), date(annee, 12, 25),
    }


def _jour_ouvrable_suivant(jour: date) -> date:
    """Le jour lui-même s'il est ouvrable, sinon le premier jour ouvrable qui suit."""
    while jour.weekday() >= 5 or jour in _jours_feries_legaux(jour.year):
        jour += timedelta(days=1)
    return jour


def _echeances_tva(year: int, regime: str) -> List[Dict[str, Any]]:
    """Échéances des déclarations TVA périodiques de l'année (règles : docstring du module)."""
    if regime == "trimestriel":
        echeances = [
            ("q1", date(year, 4, 25), f"TVA Trimestre 1 {year}"),
            ("q2", date(year, 7, 25), f"TVA Trimestre 2 {year}"),
            ("q3", date(year, 10, 25), f"TVA Trimestre 3 {year}"),
            ("q4", date(year + 1, 1, 25), f"TVA Trimestre 4 {year}"),
        ]
        details = ("Aucun report si le 25 tombe un samedi, un dimanche ou un jour férié légal : "
                   "anticiper le dépôt et le paiement.")
    elif regime == "mensuel":
        echeances = []
        for mois in range(1, 13):
            annee_echeance, mois_echeance = (year + 1, 1) if mois == 12 else (year, mois + 1)
            echeances.append((
                f"m{mois:02d}",
                _jour_ouvrable_suivant(date(annee_echeance, mois_echeance, 20)),
                f"TVA {MOIS[mois - 1].capitalize()} {year}",
            ))
        details = ("Le 20 du mois suivant, reporté au jour ouvrable suivant s'il tombe un samedi, "
                   "un dimanche ou un jour férié légal (date déjà ajustée).")
    else:
        raise ValueError(f"Régime TVA inconnu : {regime!r} (attendu : {' ou '.join(REGIMES_TVA)})")
    return [
        _format_event(
            event_id=f"tva_{year}_{code}",
            event_type="tva",
            title=title,
            deadline=deadline,
            procedure=PROCEDURE_TVA,
            details=details,
        )
        for code, deadline, title in echeances
    ]


def get_be_tax_calendar(year: int = 2026, regime: str = "trimestriel") -> List[Dict[str, Any]]:
    """
    Retourne la liste ordonnée des échéances fiscales et sociales pour une année donnée en Belgique.

    Types d'échéances inclus :
    - Déclarations TVA périodiques (Intervat) : 4 trimestrielles ou 12 mensuelles selon `regime`
    - Versements anticipés d'impôt (VA1 à VA4 - SPF Finances)
    - Cotisations sociales trimestrielles (INASTI / Caisse d'assurances sociales)

    Lève ValueError si `regime` n'est ni « trimestriel » ni « mensuel ».
    """
    # 1. Déclarations TVA périodiques
    events: List[Dict[str, Any]] = _echeances_tva(year, regime)

    # 2. Versements anticipés d'impôt (VA1-VA4)
    # Les VA permettent d'éviter la majoration d'impôt (Art. 157-168 CIR 92).
    va_dates = [
        ("1", f"{year}-04-10", f"Versement Anticipé VA1 {year}"),
        ("2", f"{year}-07-10", f"Versement Anticipé VA2 {year}"),
        ("3", f"{year}-10-10", f"Versement Anticipé VA3 {year}"),
        ("4", f"{year}-12-20", f"Versement Anticipé VA4 {year}"),
    ]
    for va_num, d_str, title in va_dates:
        d = date.fromisoformat(d_str)
        events.append(
            _format_event(
                event_id=f"va_{year}_{va_num}",
                event_type="versement_anticipe",
                title=title,
                deadline=d,
                procedure="Paiement via virement bancaire SPF Finances avec communication structurée VA (MyMinfin)",
                details="Évite la majoration d'impôt pour solopreneurs et indépendants.",
            )
        )

    # 3. Cotisations sociales trimestrielles INASTI
    inasti_quarters = [
        ("q1", f"{year}-03-31", f"Cotisations Sociales INASTI Q1 {year}"),
        ("q2", f"{year}-06-30", f"Cotisations Sociales INASTI Q2 {year}"),
        ("q3", f"{year}-09-30", f"Cotisations Sociales INASTI Q3 {year}"),
        ("q4", f"{year}-12-31", f"Cotisations Sociales INASTI Q4 {year}"),
    ]
    for q_code, d_str, title in inasti_quarters:
        d = date.fromisoformat(d_str)
        events.append(
            _format_event(
                event_id=f"inasti_{year}_{q_code}",
                event_type="inasti",
                title=title,
                deadline=d,
                procedure="Paiement à la caisse d'assurances sociales (Liantis, Partena, Xerius, UCM...)",
                details="Les fonds doivent être crédités sur le compte de la caisse au plus tard le dernier jour du trimestre.",
            )
        )

    # Tri chronologique par date d'échéance
    events.sort(key=lambda x: x["deadline"])
    return events
