---
name: be-admin-deadlines
description: "Utilisez quand le solopreneur belge veut un calendrier fiscal annuel complet (TVA, INASTI, IPP/ISOC, BNB, listings), vérifier ses prochaines échéances, ou configurer des rappels automatiques. Produit un calendrier personnalisé selon le régime et la forme juridique."
version: 0.1.0
license: MIT
author: The Agency
metadata:
  tags: [admin, finance, tax, calendar, be]
  related_skills: [be-accounting-basics, be-bookkeeping-ops, be-company-setup]
  domain: admin
  language: fr
  as_of: "2026-07"
---

# Calendrier fiscal annuel — solopreneur belge

## Overview

Ce skill produit le **calendrier fiscal complet** d'un solopreneur belge, adapté à
son régime (PP/SRL, TVA normal/franchise, IPP/ISOC). Chaque échéance est datée,
avec le rappel J-14/J-3 recommandé et l'action concrète à faire. Il complète
`be-accounting-basics` (théorie) et `be-bookkeeping-ops` (rituel mensuel) en
fournissant la **vue annuelle** qui évite les oublis coûteux.

## When to Use

- « C'est quoi mes échéances fiscales cette année ? »
- « Quand est-ce que je dois déclarer ma TVA ? »
- « J'ai raté une échéance, c'est quoi les pénalités ? »
- « Je veux configurer des rappels dans mon agenda pour toutes mes échéances »

**Ne pas utiliser pour :**
- Théorie TVA/cotisations (régimes, taux) → `be-accounting-basics`
- Rituel mensuel de tenue comptable → `be-bookkeeping-ops`
- Questions sur la création d'entreprise → `be-company-setup`

## Calendrier complet (as_of 2026-07)

### Échéances mensuelles

| Jour | Échéance | Qui est concerné | Action |
|---|---|---|---|
| **20 du mois M+1** | Déclaration TVA mensuelle | Régime normal, CA > seuil trimestriel | Déposer via logiciel/comptable + payer le solde |
| **15 du mois M** | Précompte professionnel | SRL avec employés/dirigeant salarié | Déclarer et verser le précompte du mois précédent |

### Échéances trimestrielles

| Trimestre | Échéance | Qui est concerné | Action |
|---|---|---|---|
| **T1 (avr-juin)** → 20 juillet | Déclaration TVA trimestrielle | Régime normal, CA < seuil trimestriel | Déposer + payer |
| **T2 (juil-sept)** → 20 octobre | Déclaration TVA trimestrielle | Idem | Déposer + payer |
| **T3 (oct-déc)** → 20 janvier | Déclaration TVA trimestrielle | Idem | Déposer + payer |
| **T4 (jan-mar)** → 20 avril | Déclaration TVA trimestrielle | Idem | Déposer + payer |
| **1er trimestre** → 31 mars | Cotisation sociale INASTI | Tous les indépendants | Payer à la caisse d'assurances sociales |
| **2e trimestre** → 30 juin | Cotisation sociale INASTI | Idem | Payer |
| **3e trimestre** → 30 septembre | Cotisation sociale INASTI | Idem | Payer |
| **4e trimestre** → 31 décembre | Cotisation sociale INASTI | Idem | Payer |
| **10 avril, 10 juillet, 10 octobre, 20 décembre** | Versements anticipés IPP/ISOC | PP (IPP) et SRL (ISOC) | Payer via virement (éviter majoration) |

### Échéances annuelles

| Date | Échéance | Qui est concerné | Action |
|---|---|---|---|
| **31 mars** | Listing clients assujettis TVA | Régime normal (clients belges assujettis) | Déposer via Intervat |
| **30 avril** | Déclaration TVA annuelle (régime forfaitaire) | Régime forfaitaire | Déposer |
| **30 juin** | Comptes annuels (SRL) | SRL | Déposer à la BNB via le guichet électronique |
| **30 juin** | Déclaration IPP/ISOC (via comptable) | Tous | Fournir les pièces au comptable pour préparer la déclaration |
| **1er trimestre** | Acompte de décembre TVA | Régime trimestriel | Payer l'acompte provisionnel (calculé par l'administration) |
| **Variable** | Déclaration IPP/ISOC définitive | Tous | Déposer avant la date limite du SPF Finances (variable selon le mode) |
| **Variable** | Renouvellement assurances | Tous | Vérifier les échéances et renouveler |
| **Variable** | Renouvellement caisse sociale | Tous | Vérifier l'affiliation et les cotisations |

### Échéances ponctuelles (après création)

| Échéance | Délai | Action |
|---|---|---|
| Activation TVA | Immédiatement après inscription BCE | Vérifier que le numéro est actif dans le registre |
| Affiliation caisse sociale | Avant le début d'activité | Vérifier l'attestation d'affiliation |
| UBO register (SRL) | Dans le mois après constitution | Déclarer les bénéficiaires effectifs |
| Compte bancaire pro | Avant la 1re facture | Ouvrir un compte séparé |

## Configuration des rappels (agenda)

Pour chaque échéance, créer **2 rappels récurrents** :
- **J-14** : rappel de préparation (rassembler les pièces, vérifier les montants)
- **J-3** : rappel d'exécution (déposer, payer, envoyer)

Exemple de structure dans l'agenda :
```
[TVA] Déclaration trimestrielle T1 — 20 avril
  Rappel J-14 : 6 avril — préparer déclaration
  Rappel J-3 : 17 avril — déposer et payer
[INASTI] Cotisation sociale T1 — 31 mars
  Rappel J-14 : 17 mars — vérifier montant
  Rappel J-3 : 28 mars — payer
```

## Pénalités de retard (ordres de grandeur, as_of 2026-07)

| Échéance | Pénalité | Source |
|---|---|---|
| TVA (déclaration tardive) | Amende fixe + majoration progressive | SPF Finances |
| TVA (paiement tardif) | Intérêts de retard (taux semestriel) | SPF Finances |
| INASTI (cotisation tardive) | Majoration de 3 % à 7 % selon le retard | INASTI |
| IPP/ISOC (versements anticipés manquants) | Majoration de 2,25 % à 6,75 % selon le trimestre | SPF Finances |
| Comptes annuels SRL (dépôt tardif) | Amende progressive (BNB) | BNB |

**Vérifier les montants exacts** sur les sites officiels — les taux changent.

## Common Pitfalls

1. **Oublier l'acompte de décembre TVA.** L'administration le calcule automatiquement
   mais ne vous prévient pas toujours à temps. Mettre un rappel dès novembre.
2. **Confondre date limite et date de paiement.** La date limite est le jour où le
   virement doit être reçu (pas émis). Payer 2-3 jours avant.
3. **Négliger les versements anticipés.** La majoration IPP/ISOC pour versements
   manquants coûte cher — les faire systématiquement, même si le montant est estimé.
4. **Régime trimestriel sans acompte de décembre.** L'acompte de décembre est obligatoire
   pour le régime trimestriel TVA — ne pas l'oublier.
5. **UBO register oublié.** La SRL doit déclarer ses bénéficiaires effectifs dans le
   mois après la constitution — sanction en cas de retard.
6. **Confondre échéance comptable et échéance fiscale.** Le comptable prépare la
   déclaration, mais c'est VOUS qui êtes responsable du dépôt et du paiement.

## Verification Checklist

- [ ] Toutes les échéances applicables dans l'agenda avec rappels J-14/J-3
- [ ] Régime TVA déterminé (normal/frimestriel/forfait)
- [ ] Forme juridique déterminée (PP/SRL) → échéances adaptées
- [ ] Versements anticipés IPP/ISOC programmés (4×/an)
- [ ] Acompte de décembre TVA rappelé (si régime trimestriel)
- [ ] Comptes annuels SRL rappelés (30 juin)
- [ ] UBO register rappelé (si SRL récente)

> ⚠️ **Disclaimer** : information générale (as_of 2026-07), pas un conseil fiscal
> personnalisé. Les dates, taux et pénalités évoluent — vérifier sur les sites
> officiels (SPF Finances, INASTI, BNB) et faire valider par un comptable ou
> expert-comptable agréé en Belgique.
