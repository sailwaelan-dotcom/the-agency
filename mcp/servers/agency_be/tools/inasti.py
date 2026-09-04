"""
Simulateur de cotisations sociales indépendant INASTI (Belgique).
Réglementation et seuils officiels as_of 2026-01-01.
"""
from typing import Any, Dict

MIN_ANNUAL_INCOME = 16861.46       # Seuil plancher cotisation minimale (~864.15 €/trimestre hors frais)
FIRST_BRACKET_CEILING = 77015.17   # Seuil première tranche à 20,5%
MAX_ANNUAL_INCOME = 107300.00      # Plafond maximal au-delà duquel aucune cotisation n'est due
RATE_BRACKET_1 = 0.205             # 20,5%
RATE_BRACKET_2 = 0.1416            # 14,16%
DEFAULT_MANAGEMENT_FEE = 0.035     # Frais de gestion de caisse (3,5% en moyenne)


def calc_inasti_provision(
    annual_net_income: float,
    is_starter: bool = False,
    year: int = 2026,
    management_fee_rate: float = DEFAULT_MANAGEMENT_FEE,
) -> Dict[str, Any]:
    """
    Calcule la cotisation sociale trimestrielle provisionnelle pour un travailleur
    indépendant à titre principal en Belgique.

    Barème légal :
    - Moins de 16 861,46 € : cotisation minimale forfaitaire
    - De 16 861,46 € à 77 015,17 € : 20,5 %
    - De 77 015,17 € à 107 300,00 € : 14,16 %
    - Au-delà de 107 300,00 € : plafonné
    + Frais de gestion de la caisse d'assurances sociales (~3,05% à 4,25%).
    """
    income = float(annual_net_income)
    is_min = False
    is_max = False

    if income <= MIN_ANNUAL_INCOME:
        is_min = True
        base_annual = MIN_ANNUAL_INCOME * RATE_BRACKET_1
    elif income > MAX_ANNUAL_INCOME:
        is_max = True
        base_annual = (FIRST_BRACKET_CEILING * RATE_BRACKET_1) + (
            (MAX_ANNUAL_INCOME - FIRST_BRACKET_CEILING) * RATE_BRACKET_2
        )
    else:
        if income <= FIRST_BRACKET_CEILING:
            base_annual = income * RATE_BRACKET_1
        else:
            base_annual = (FIRST_BRACKET_CEILING * RATE_BRACKET_1) + (
                (income - FIRST_BRACKET_CEILING) * RATE_BRACKET_2
            )

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
            "Estimation légale indicative basée sur les barèmes INASTI. "
            "Les cotisations payées sont des provisions régularisées 2 à 3 ans plus tard "
            "sur base de l'avertissement-extrait de rôle fiscal définitif."
        ),
    }
