"""
Catalogue et lecture des ressources réglementaires belges (MCP Resources).
Fournit aux agents IA un accès direct aux textes légaux, barèmes et grilles fiscales.
"""
import json
from typing import Any, Dict, List

RESOURCES_CATALOG: List[Dict[str, Any]] = [
    {
        "uri": "belgian-tax://2026/rates",
        "name": "Taux TVA et régimes fiscaux belges (2026)",
        "description": (
            "Grille officielle des taux de TVA en Belgique (21%, 12%, 6%, 0%), "
            "seuils de la franchise pour petites entreprises (Art. 56bis CTVA), "
            "règles de facturation intracommunautaire (autoliquidation) et dérogations."
        ),
        "mimeType": "application/json",
    },
    {
        "uri": "inasti://2026/brackets",
        "name": "Barèmes de cotisations sociales INASTI (2026)",
        "description": (
            "Seuils planchers, tranches de cotisation (20,5% et 14,16%) et plafonds maximaux "
            "pour les indépendants à titre principal, conjoints aidants et débutants."
        ),
        "mimeType": "application/json",
    },
    {
        "uri": "cir92://deductibility/rules",
        "name": "Règles de déductibilité des frais professionnels (CIR 92)",
        "description": (
            "Pourcentages légaux de déductibilité fiscale en Belgique : "
            "frais de restaurant (69%), frais de réception (50%), cadeaux d'affaires (50%), "
            "règles d'amortissement et frais de bureau à domicile."
        ),
        "mimeType": "application/json",
    },
]

TAX_RATES_DATA = {
    "year": 2026,
    "as_of": "2026-01-01",
    "rates": {
        "standard": 0.21,
        "intermediate": 0.12,
        "reduced": 0.06,
        "zero": 0.00,
    },
    "rate_descriptions": {
        "0.21": "Taux normal standard applicable à la majorité des biens et prestations de services.",
        "0.12": "Taux intermédiaire : restauration (nourriture sans boissons), certains travaux immobiliers.",
        "0.06": "Taux réduit : produits alimentaires de base, livres, médicaments, rénovation d'habitations privées de plus de 10 ans.",
        "0.00": "Taux zéro : presse quotidienne et périodique, certaines opérations maritimes/aériennes.",
    },
    "franchise_56bis": {
        "threshold": 25000.0,
        "legal_basis": "Article 56bis du Code de la TVA",
        "mandatory_invoice_notice": "Franchise de taxe, petites entreprises — Article 56bis du Code de la TVA",
        "rules": [
            "Pas de TVA facturée aux clients.",
            "Aucune déduction de la TVA payée sur les achats et investissements.",
            "Obligation de déposer le listing annuel des clients assujettis belges avant le 31 mars.",
        ],
    },
    "cross_border_b2b": {
        "legal_basis": "Article 196 Directive 2006/112/CE & Art. 51 §2 1° CTVA",
        "mandatory_invoice_notice": "Autoliquidation — Reverse charge (Article 196 Directive 2006/112/CE)",
        "rules": [
            "Facturation HTVA à un client assujetti établi dans un autre État membre de l'UE.",
            "Vérification préalable obligatoire du numéro de TVA sur VIES.",
            "Dépôt d'un relevé intracommunautaire (listing intracommunautaire périodique).",
        ],
    },
}

INASTI_BRACKETS_DATA = {
    "year": 2026,
    "as_of": "2026-01-01",
    "minimum_annual_income": 16861.46,
    "first_bracket_ceiling": 77015.17,
    "maximum_annual_income": 107300.00,
    "rate_bracket_1": 0.205,
    "rate_bracket_2": 0.1416,
    "average_management_fee_rate": 0.035,
    "starter_concession": (
        "Les indépendants débutants (3 premières années) bénéficient d'une cotisation minimale "
        "réduite sous conditions de revenus modestes."
    ),
    "regularization_rule": (
        "Les cotisations payées trimestriellement sont des provisions basées sur l'année N-3. "
        "La régularisation définitive intervient 2 à 3 ans plus tard sur base de l'avertissement-extrait de rôle."
    ),
}

CIR92_RULES_DATA = {
    "year": 2026,
    "as_of": "2026-01-01",
    "legal_code": "Code des Impôts sur les Revenus 1992 (CIR 92)",
    "restaurant_expenses": {
        "deductibility_rate": 0.69,
        "legal_basis": "Article 53, 8° CIR 92",
        "condition": "La note de restaurant doit comporter une souche TVA avec mention des convives et du lien professionnel direct.",
    },
    "reception_expenses": {
        "deductibility_rate": 0.50,
        "legal_basis": "Article 53, 8° CIR 92",
        "description": "Frais de réception et d'accueil de relations d'affaires.",
    },
    "business_gifts": {
        "deductibility_rate": 0.50,
        "condition": "Valeur unitaire inférieure à 50 € HTVA. Au-delà, considéré comme avantage de toute nature ou libéralité non déductible.",
    },
    "home_office": {
        "deductibility_rate": "quote-part réelle (m2 pro / m2 total)",
        "condition": "Pièce exclusivement affectée à l'exercice de l'activité professionnelle indépendante.",
    },
}


def get_server_resources() -> List[Dict[str, Any]]:
    """Retourne la liste des métadonnées de ressources exposées."""
    return RESOURCES_CATALOG


def handle_read_resource(uri: str) -> Dict[str, Any]:
    """Lit et sérialise la ressource correspondant à l'URI demandée."""
    if uri == "belgian-tax://2026/rates":
        return {
            "uri": uri,
            "mimeType": "application/json",
            "text": json.dumps(TAX_RATES_DATA, ensure_ascii=False, indent=2),
        }
    if uri == "inasti://2026/brackets":
        return {
            "uri": uri,
            "mimeType": "application/json",
            "text": json.dumps(INASTI_BRACKETS_DATA, ensure_ascii=False, indent=2),
        }
    if uri == "cir92://deductibility/rules":
        return {
            "uri": uri,
            "mimeType": "application/json",
            "text": json.dumps(CIR92_RULES_DATA, ensure_ascii=False, indent=2),
        }

    raise ValueError(f"Ressource inconnue : {uri}")
