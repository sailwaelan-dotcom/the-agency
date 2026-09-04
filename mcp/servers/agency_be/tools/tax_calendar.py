"""
Générateur de calendrier fiscal et social belge pour solopreneurs.
Couvre les échéances SPF Finances (TVA, Versements Anticipés) et INASTI.
"""
from datetime import date, timedelta
from typing import Any, Dict, List


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


def get_be_tax_calendar(year: int = 2026, regime: str = "trimestriel") -> List[Dict[str, Any]]:
    """
    Retourne la liste ordonnée des échéances fiscales et sociales pour une année donnée en Belgique.

    Types d'échéances inclus :
    - Déclarations TVA trimestrielles (Intervat)
    - Versements anticipés d'impôt (VA1 à VA4 - SPF Finances)
    - Cotisations sociales trimestrielles (INASTI / Caisse d'assurances sociales)
    """
    events: List[Dict[str, Any]] = []

    # 1. Déclarations TVA trimestrielles (dépôt + paiement le 20 du mois suivant le trimestre)
    tva_quarters = [
        ("q1", f"{year}-04-20", f"TVA Trimestre 1 {year}"),
        ("q2", f"{year}-07-20", f"TVA Trimestre 2 {year}"),
        ("q3", f"{year}-10-20", f"TVA Trimestre 3 {year}"),
        ("q4", f"{year + 1}-01-20", f"TVA Trimestre 4 {year}"),
    ]
    for q_code, d_str, title in tva_quarters:
        d = date.fromisoformat(d_str)
        events.append(
            _format_event(
                event_id=f"tva_{year}_{q_code}",
                event_type="tva",
                title=title,
                deadline=d,
                procedure="Dépôt déclaration Intervat + paiement sur compte SPF Finances avec communication structurée",
                details="Pénalité de retard et intérêts légaux en cas de non-respect du 20.",
            )
        )

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
