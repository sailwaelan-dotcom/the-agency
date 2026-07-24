---
name: be-financial-modeling
description: "Utilisez quand le solopreneur belge doit modéliser un projet d'investissement, calculer une valorisation (DCF, multiples), analyser la sensibilité de ses hypothèses, ou stress-tester un business plan avec Monte Carlo. Produit des modèles financiers avec scénarios et graphiques de sensibilité."
version: 0.1.0
license: MIT
author: The Agency
metadata:
  tags: [business, finance, modeling, valuation, be]
  related_skills: [be-business-plan, be-market-research, be-funding-subsidies, fact-check-sourcing]
  domain: finance
  language: fr
  as_of: "2026-07"
---

# Modélisation financière — solopreneur belge

## Overview

Ce skill fournit les outils de **modélisation financière** pour les projets
d'investissement, valorisations et stress-tests. Inspiré des meilleures pratiques
(claude-cookbooks financial modeling) adapté au contexte belge : ISOC, IPP,
précompte mobilier, VVPR-bis, taux d'actualisation ajustés au marché belge.
Il produit des modèles DCF, analyses de sensibilité et simulations Monte Carlo
pour valider la robustesse d'un business plan ou d'un investissement.

## When to Use

- « Je dois valoriser mon entreprise / un projet d'investissement »
- « Quel est le DCF de mon business plan ? »
- « Comment mes hypothèses impactent-elles la rentabilité ? »
- « Je veux stress-tester mon plan avec Monte Carlo »
- « Un investisseur me demande une valorisation justifiée »

**Ne pas utiliser pour :**
- Business plan narratif → `be-business-plan`
- Étude de marché (inputs) → `be-market-research`
- Plan financier SRL (norme CSA) → `be-business-plan` (references/)

## Méthodologies de valorisation

### 1. DCF (Discounted Cash Flow)

**Quand** : valorisation d'une entreprise en création ou en croissance.

**Formule** : Valeur = Σ (FCF_t / (1 + WACC)^t) + Valeur terminale / (1 + WACC)^n

| Paramètre | Définition | Source BE |
|---|---|---|
| **FCF** (Free Cash Flow) | Cash flow disponible après investissements | Business plan prévisionnel |
| **WACC** (Weighted Average Cost of Capital) | Coût moyen pondéré du capital | Taux sans risque BE + prime de risque |
| **Valeur terminale** | Valeur de l'entreprise à l'infini | Croissance perpétuelle ou multiple de sortie |

**Taux d'actualisation BE** (as_of 2026-07 — vérifier) :
- Taux sans risque : OLO belge 10 ans (consultable sur banquenationale.be)
- Prime de risque marché : 5-7 % (marché belge)
- Prime de risque spécifique : +3-8 % selon le risque du projet
- **WACC typique PME belge** : 10-15 % (à ajuster selon le secteur)

### 2. Multiples (comparables)

**Quand** : valorisation rapide par comparaison avec des transactions similaires.

| Multiple | Formule | Source |
|---|---|---|
| **EV/CA** | Enterprise Value / Chiffre d'affaires | Transactions comparables, BNB |
| **EV/EBITDA** | Enterprise Value / EBITDA | Transactions comparables, BNB |
| **P/E** | Price / Earnings | Comptes annuels concurrents (BNB) |

**Fourchettes typiques** (à vérifier sur données réelles) :
- SaaS : 3-8× CA (selon croissance et rétention)
- Services B2B : 1-3× CA
- Commerce : 0,5-1,5× CA

### 3. Berkus (pré-revenus)

**Quand** : valorisation d'un projet avant les premiers revenus.

| Critère | Valorisation max |
|---|---|
| Idée (qualité, originalité) | jusqu'à 500 000 € |
| Prototype/MVP | jusqu'à 500 000 € |
| Équipe fondatrice | jusqu'à 500 000 € |
| Relations/clients early-stage | jusqu'à 500 000 € |
| Lancement/résultats initiaux | jusqu'à 500 000 € |
| **Total max** | **2,5 M€** |

## Analyse de sensibilité

**Quand** : comprendre l'impact de chaque hypothèse sur le résultat.

### Méthode tornado

1. Identifier les 5-10 hypothèses clés (prix, volume, coûts, délai paiement)
2. Pour chaque hypothèse, définir un range pessimiste/central/optimiste
3. Calculer l'impact de chaque variation sur le résultat (NPV, breakeven, cash)
4. Classer par impact décroissant → graphique tornado

**Exemple** :
| Hypothèse | Pessimiste | Central | Optimiste | Impact NPV |
|---|---|---|---|---|
| Prix moyen | −20 % | Base | +10 % | ±45 % |
| Volume clients | −30 % | Base | +20 % | ±35 % |
| Délai paiement | +30 jours | 45 jours | −15 jours | ±15 % |
| Coûts fixes | +15 % | Base | −10 % | ±12 % |

*Critère de complétion* : graphique tornado produit, hypothèses classées par impact.

## Simulation Monte Carlo

**Quand** : stress-tester un modèle avec des distributions de probabilité.

### Méthode

1. Définir une distribution pour chaque hypothèse clé (normale, triangulaire, uniforme)
2. Tirer N échantillons aléatoires (N = 1 000 à 10 000)
3. Calculer le résultat (NPV, cash, breakeven) pour chaque tirage
4. Analyser la distribution des résultats

**Distributions typiques** :
| Hypothèse | Distribution | Paramètres |
|---|---|---|
| Prix | Normale | μ = prix central, σ = 10 % |
| Volume | Triangulaire | min = pessimiste, mode = central, max = optimiste |
| Délai paiement | Uniforme | min = 30j, max = 90j |

**Résultat** :
- Probabilité que le projet soit rentable (NPV > 0)
- Valeur médiane du NPV
- Intervalles de confiance (5 %, 25 %, 75 %, 95 %)

*Critère de complétion* : distribution des NPV produite, probabilité de rentabilité calculée.

## Workflow

1. **Rassembler les inputs** : business plan, étude de marché, hypothèses de pricing.
   *Critère : toutes les données d'entrée sont sourcées (→ fact-check-sourcing).*

2. **Construire le modèle DCF** : FCF prévisionnels 3-5 ans + valeur terminale.
   *Critère : le modèle est reproductible (formules visibles, pas de boîte noire).*

3. **Analyser la sensibilité** : tornado sur les 5 hypothèses les plus impactantes.
   *Critère : le graphique tornado montre clairement quelles hypothèses dominent.*

4. **Simuler Monte Carlo** : 1 000+ itérations avec distributions définies.
   *Critère : la probabilité de rentabilité est calculée avec intervalles de confiance.*

5. **Documenter** : chaque hypothèse, source, et résultat est tracé.
   *Critère : un tiers peut reproduire le modèle à partir de la documentation.*

## Adaptation BE spécifique

| Élément | Spécificité belge |
|---|---|
| **ISOC** | Taux réduit PME sous conditions (premiers 100 000 €) — vérifier les conditions |
| **IPP** | Progressif 25-50 % + taxe communale — à modéliser selon le revenu |
| **Précompte mobilier** | 30 % sur dividendes (sauf VVPR-bis : 15 % après 3 ans) |
| **VVPR-bis** | Taux réduit 15 % sur dividendes si apport ≥ 20 % du capital, après 3 ans |
| **Plus-values** | Exonérées si gestion normale du patrimoine privé (sauf spéculation) |
| **TVA** | Non incluse dans la valorisation (flux à travers) |

## Common Pitfalls

1. **Modèle boîte noire.** Si les formules ne sont pas visibles et compréhensibles,
   le modèle n'est pas reproductible → rejeté par tout investisseur sérieux.
2. **Hypothèses non sourcées.** Chaque chiffre doit avoir une source (→ fact-check-sourcing).
   « J'ai estimé » sans justification = rejeté.
3. **Confondre valorisation et prix.** La valorisation est une estimation ; le prix est
   ce que quelqu'un est prêt à payer. Les deux peuvent diverger fortement.
4. **Négliger la fiscalité belge.** ISOC, précompte mobilier, VVPR-bis impactent
   directement la rentabilité → à modéliser systématiquement.
5. **Trop d'hypothèses.** 5-10 hypothèses clés suffisent. Au-delà, le modèle devient
   ingérable et les résultats peu fiables.
6. **Oublier le cash flow.** Un projet rentable (NPV > 0) peut mourir de faillite
   si le cash flow est négatif trop longtemps. Toujours modéliser la trésorerie.

## Verification Checklist

- [ ] Inputs sourcés (→ fact-check-sourcing)
- [ ] Modèle DCF reproductible (formules visibles)
- [ ] Tornado produit (5+ hypothèses)
- [ ] Monte Carlo exécuté (1 000+ itérations)
- [ ] Fiscalité belge modélisée (ISOC, IPP, précompte)
- [ ] Documentation complète (hypothèses + sources + résultats)

> ⚠️ **Disclaimer** : information générale (as_of 2026-07), pas un conseil financier
> ou fiscal personnalisé. Les modèles de valorisation sont des outils d'aide à la
> décision, pas des vérités absolues — faire valider par un expert-comptable ou un
> conseiller financier agréé en Belgique avant toute transaction.
