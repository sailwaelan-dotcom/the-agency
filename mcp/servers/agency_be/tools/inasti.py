"""
Simulateur de cotisations sociales indépendant INASTI (Belgique).

Barème 2026, indépendant à titre principal (as_of 2026-01 — UCM, « Calcul et barème des
cotisations sociales dues en 2026 », note d'info janvier 2026 ; Partena Professional,
« Barème des cotisations trimestrielles indépendants pour 2026 ») :
- revenu minimum 17 374,08 € (cotisation minimale 890,42 €/trimestre hors frais) ;
- 20,5 % jusqu'à 75 024,54 €, 14,16 % de 75 024,54 € à 110 562,42 €, rien au-delà ;
- primostarter (4 premiers trimestres d'une première activité principale, sous conditions) :
  revenu minimum réduit à 8 972,07 € (Partena, barème 2026).
"""
from typing import Any, Dict

SUPPORTED_YEAR = 2026
MIN_ANNUAL_INCOME = 17374.08                # Revenu minimum, activité principale
PRIMOSTARTER_MIN_ANNUAL_INCOME = 8972.07    # Revenu minimum réduit du primostarter
FIRST_BRACKET_CEILING = 75024.54            # Fin de la tranche à 20,5 %
MAX_ANNUAL_INCOME = 110562.42               # Plafond : aucune cotisation au-delà
RATE_BRACKET_1 = 0.205                      # 20,5 %
RATE_BRACKET_2 = 0.1416                     # 14,16 %
# Frais de gestion propres à chaque caisse (2026 : UCM 4,05 %, Partena 4,20 %).
DEFAULT_MANAGEMENT_FEE = 0.035


def calc_inasti_provision(
    annual_net_income: float,
    is_starter: bool = False,
    year: int = SUPPORTED_YEAR,
    management_fee_rate: float = DEFAULT_MANAGEMENT_FEE,
) -> Dict[str, Any]:
    """
    Calcule la cotisation sociale trimestrielle d'un indépendant à titre principal
    en Belgique, sur le revenu net imposable annuel (barème : docstring du module).

    `is_starter` vise le primostarter (4 premiers trimestres) : son revenu minimum est réduit.
    Les autres débutants (jusqu'à la fin de la 3e année civile complète) paient le barème normal.
    Lève ValueError pour une autre année que 2026 : seul ce barème est codé.
    """
    if year != SUPPORTED_YEAR:
        raise ValueError(f"Barème INASTI disponible uniquement pour {SUPPORTED_YEAR} (reçu : {year})")

    income = float(annual_net_income)
    floor = PRIMOSTARTER_MIN_ANNUAL_INCOME if is_starter else MIN_ANNUAL_INCOME
    is_min = income <= floor
    is_max = income > MAX_ANNUAL_INCOME

    assessed = min(max(income, floor), MAX_ANNUAL_INCOME)
    base_annual = min(assessed, FIRST_BRACKET_CEILING) * RATE_BRACKET_1
    if assessed > FIRST_BRACKET_CEILING:
        base_annual += (assessed - FIRST_BRACKET_CEILING) * RATE_BRACKET_2

    quarterly_base = round(base_annual / 4.0, 2)
    quarterly_fee = round(quarterly_base * management_fee_rate, 2)
    total_quarterly = round(quarterly_base + quarterly_fee, 2)
    total_annual = round(total_quarterly * 4, 2)

    return {
        "annual_net_income": income,
        "is_starter": is_starter,
        "year": year,
        "is_minimum_applied": is_min,
        "is_ceiling_applied": is_max,
        "quarterly_base_contribution": quarterly_base,
        "management_fee_rate": management_fee_rate,
        "quarterly_management_fee": quarterly_fee,
        "total_quarterly_due": total_quarterly,
        "annual_estimated_total": total_annual,
        "as_of": "2026-01-01",
        "disclaimer": (
            "Estimation indicative basée sur le barème INASTI 2026. Les frais de gestion varient "
            "selon la caisse. Les cotisations payées sont des provisions, régularisées plus tard "
            "sur base des revenus définitifs communiqués par le SPF Finances."
        ),
    }
