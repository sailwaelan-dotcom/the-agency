---
name: be-accounting-basics
description: "Utilisez quand le solopreneur belge pose une question TVA (régime normal/franchise/forfait, déclarations, délais), impôt (IPP vs ISOC), précompte professionnel, cotisations sociales INASTI, ou veut comprendre ses obligations comptables de base. Produits : réponse chiffrée avec as_of + renvoi officiel, calendrier des échéances."
version: 0.1.0
license: MIT
author: The Agency
metadata:
  tags: [finance, accounting, tax, tva, be]
  related_skills: [be-invoicing-peppol, be-bookkeeping-ops]
  domain: finance
  language: fr
  as_of: "2026-09"
---

# Comptabilité de base — solopreneur belge

## Overview

Un solopreneur belge (indépendant personne physique ou SRL) jongle avec quatre
obligations récurrentes : la **TVA** (déclarations périodiques), les **cotisations
sociales** (INASTI, provisionnelles trimestrielles), l'**impôt** (IPP pour la personne
physique, ISOC + précompte mobilier sur dividendes pour la SRL) et le **précompte
professionnel** (versé par la SRL sur la rémunération du dirigeant).

Ce skill répond aux questions de routine (« quand est ma prochaine déclaration TVA ? »,
« franchise ou régime normal ? », « combien provisionner pour l'impôt ? ») et produit
un calendrier d'échéances personnalisé. Il ne remplace pas un comptable : il prépare
les bonnes questions et évite les oublis coûteux.

## When to Use

- « Franchise TVA ou régime normal, je choisis quoi ? »
- « C'est quoi mes échéances ce trimestre ? »
- « Combien je mets de côté pour l'impôt / les cotisations ? »
- « IPP ou ISOC, je paie quoi avec ma SRL ? »
- « Le précompte professionnel, ça marche comment pour un dirigeant d'entreprise ? »

**Ne pas utiliser pour :**
- Émettre une facture conforme → `be-invoicing-peppol`
- Organiser les pièces et préparer le dossier comptable mensuel → `be-bookkeeping-ops`
- Choisir SRL vs personne physique à la création → `be-company-setup`

## Concepts clés (as_of 2026-07 — vérifier les montants en vigueur)

### TVA

| Régime | Pour qui | Déclarations | Particularités |
|---|---|---|---|
| **Franchise** | CA annuel ≤ seuil légal (≈ 25 000 €, *vérifier le seuil en vigueur*) | Aucune déclaration périodique (une liste annuelle clients reste possible) | Pas de TVA facturée, pas de TVA récupérable. Mention « Franchise de TVA — art. 56bis CTVA » sur chaque facture |
| **Régime normal** | Au-delà du seuil, ou par choix | Mensuelle **ou** trimestrielle (si CA < seuil trimestriel, *vérifier*) | TVA collectée − TVA déductible = solde à payer/récupérer |
| **Forfait** | Certains secteurs sans TVA déductible suffisante | Trimestrielle | Calcul forfaitaire du solde — cas de plus en plus rare |

- Délais (as_of 2026-09, SPF Finances) : dépôt + paiement au plus tard le **20 du mois suivant**
  pour les mensuels (reporté au jour ouvrable suivant si le 20 tombe un samedi, un dimanche
  ou un jour férié légal) et le **25 du mois suivant le trimestre** pour les trimestriels,
  **sans report**. Plus d'acomptes pour les trimestriels : la TVA due se paie à l'échéance.
- La **liste annuelle des clients assujettis** et le **listing intracommunautaire**
  restent dus selon votre situation, même en franchise pour certains cas.

### Cotisations sociales (indépendant)

- **Provisionnelles trimestrielles** à la caisse d'assurances sociales, calculées sur
  les revenus d'il y a 3 ans, régularisées après taxation définitive.
- Taux de base ≈ **20,5 %** du revenu net imposable (*vérifier le taux en vigueur*),
  avec minimums pour débutants et plafonds.
- Statuts : activité principale, complémentaire, étudiant-indépendant, pensionné actif —
  chacun a ses seuils d'exonération. Le choix du statut change tout le calcul.
- **Outillage MCP (`agency-be-mcp`)** : Utilisez `calc_inasti_provision(annual_net_income=...)` pour calculer immédiatement les provisions trimestrielles exactes, les frais de caisse estimés et vérifier si les seuils planchers ou plafonds s'appliquent.

### Impôt

- **Personne physique (indépendant)** : IPP progressif sur le bénéfice, versements
  anticipés trimestriels fortement recommandés (majoration sinon).
- **SRL** : ISOC sur le bénéfice de la société (taux réduit PME sous conditions,
  *vérifier les conditions d'octroi*), puis précompte mobilier sur dividendes
  (taux standard 30 %, régimes réduits VVPR-bis / liquidation sous conditions).
- **Précompte professionnel** : retenu par la SRL sur la rémunération mensuelle du
  dirigeant, déclaré et versé mensuellement ou trimestriellement.

## Questions à poser
Posées **en une seule salve** avant de produire l'artefact — options fermées quand possible, jamais de donnée inventée ; l'inconnu qui reste est marqué « à confirmer » :
- Votre forme juridique : personne physique (IPP) ou SRL (ISOC) ?
- Votre régime TVA : franchise, normal (mensuel ou trimestriel), ou forfait ?
- Votre statut INASTI : activité principale, complémentaire, étudiant-indépendant, pensionné actif ?
- Votre chiffre d'affaires estimé ? (pour surveiller le seuil de franchise)
- Votre année de début d'activité ? (les cotisations se calculent sur la 3e année précédente)
- Pour une SRL : quelle rémunération de dirigeant envisagée ? (précompte pro, VVPR-bis)

## Workflow

### 1. Identifier la situation

Demander (ou déduire du contexte) : forme juridique (PP/SRL), régime TVA, statut
social, chiffre d'affaires estimé, année de démarrage.

*Critère de complétion* : les 5 paramètres sont notés ; les inconnus sont marqués
« à confirmer avec le comptable ».

### 2. Construire le calendrier d'échéances

Produire un tableau mois par mois pour les 12 prochains mois :

| Mois | Échéance | Action | Montant estimé |
|---|---|---|---|
| … | Déclaration TVA T+1 | Préparer via comptable/logiciel | selon CA |
| … | Cotisation sociale trimestre | Payer à la caisse | provisionnel |
| … | Versement anticipé IPP/ISOC | Recommandé | X % du bénéfice estimé |

*Critère de complétion* : chaque échéance applicable a une date limite et un
responsable (toi / comptable / logiciel automatique).

### 3. Calculer les provisions

Règles de pouce à présenter comme **ordres de grandeur**, pas comme conseil :
- Mettre de côté **30-50 % du net facturé** (IPP + cotisations) pour un indépendant PP
  selon le niveau de revenu ; affiner après la première année réelle.
- Pour une SRL : provisionner l'ISOC sur le bénéfice + garder la trésorerie du
  précompte professionnel mensuel séparée.

*Critère de complétion* : un pourcentage de provision est choisi et justifié par le
niveau de revenu estimé, avec la mention « à recalibrer avec le comptable après
année 1 ».

### 4. Signaler les pièges du moment

Vérifier systématiquement : passage de seuil franchise (risque de bascule rétroactive),
échéance TVA trimestrielle du 25 (sans report), régularisation cotisations sur revenus réels, oubli listing
annuel clients.

## Références belges

- **SPF Finances** (finances.belgium.be) : régimes TVA, délais, taux, Intervat.
- **INASTI** (rsvz-inasti.fgov.be) : cotisations sociales indépendants, calculateur.
- **Caisse d'assurances sociales** du solopreneur : interlocuteur concret des paiements.
- **Biztax / MyMinfin** : déclarations IPP/ISOC en ligne.
- Toutes les données datées : **as_of 2026-07** (échéances TVA : **as_of 2026-09**). Vérifier chaque montant/seuil/taux
  sur la source officielle avant décision.

## Common Pitfalls

1. **Dépasser le seuil franchise sans réagir.** Le dépassement peut rendre la TVA due
   rétroactivement. Suivre le CA mensuellement et anticiper le basculement.
2. **Payer la TVA trimestrielle le 20 ou le lundi suivant.** L'échéance est le 25 du mois
   qui suit le trimestre, sans report : des intérêts de retard courent dès le 26.
3. **Mélanger compte perso et pro.** Rend la déclaration et le contrôle pénibles ;
   compte pro dédié dès le jour 1 (obligatoire pour SRL).
4. **Négliger les versements anticipés.** La majoration IPP/ISOC coûte plusieurs % du
   bénéfice ; les VA trimestriels les neutralisent.
5. **Croire que « franchise » = zéro paperasse.** Factures avec mention légale, liste
   annuelle clients éventuelle, et tenue d'un journal des recettes restent exigées.
6. **Calculer ses cotisations sur le revenu de l'année en cours.** Elles se basent sur
   N-3 avec régularisation : prévoir la régularisation dans la trésorerie.

## Verification Checklist

- [ ] Régime TVA confirmé et cohérent avec le CA
- [ ] Calendrier 12 mois produit avec dates limites réelles
- [ ] Pourcentage de provision impôt+cotisations défini et mis en pratique (compte épargne dédié)
- [ ] Compte bancaire pro séparé
- [ ] Chaque chiffre du skill vérifié sur source officielle le jour d'utilisation

> ⚠️ **Disclaimer** : information générale (as_of 2026-09 pour les échéances TVA, 2026-07 pour le reste), pas un conseil fiscal ou
> comptable personnalisé. Faites valider votre situation (régime TVA, statut social,
> versements anticipés) par un comptable ou expert-comptable agréé en Belgique —
> notamment avant tout choix de régime ou estimation de provision.
