---
name: be-bookkeeping-ops
description: "Utilisez quand le solopreneur belge doit organiser sa comptabilité courante : rituel mensuel de collecte des pièces, rapprochement bancaire, suivi des factures impayées et relances clients, préparation du dossier pour le comptable, ou archivage légal (7 ans)."
version: 0.1.0
license: MIT
author: The Agency
metadata:
  tags: [finance, accounting, bookkeeping, ops, be]
  related_skills: [be-accounting-basics, be-invoicing-peppol]
  domain: finance
  language: fr
  as_of: "2026-07"
---

# Tenue comptable opérationnelle — solopreneur belge

## Overview

Ce skill couvre le **travail récurrent** entre deux rendez-vous comptables : collecter
les pièces, rapprocher la banque, relancer les impayés, préparer un dossier propre. Il
produit un **rituel mensuel de 60-90 minutes** qui évite la panique de fin d'année et
les honoraires de « déblayage ». Pas de théorie TVA ici (voir `be-accounting-basics`) —
uniquement l'hygiène opérationnelle : pièces, banque, cash, délais.

## When to Use

- « C'est la fin du mois, qu'est-ce que je dois faire côté compta ? »
- « Mon comptable me réclame mes pièces, je lui envoie quoi et comment ? »
- « Un client n'a pas payé, je relance comment ? »
- « Je veux arrêter de passer mes week-ends à trier des tickets »
- « Comment j'archive mes factures légalement ? »

**Ne pas utiliser pour :**
- Régimes TVA, cotisations, impôts (théorie) → `be-accounting-basics`
- Émettre une facture conforme → `be-invoicing-peppol`
- Choix de structure → `be-company-setup`

## Inputs & Sorties

**Entrées** : outil de facturation utilisé, banque(s), volume mensuel de factures,
comptable (oui/non + son logiciel), mode actuel de stockage des pièces.

**Sorties** :
- Rituel mensuel calé à date fixe avec checklist
- Arborescence d'archivage normalisée (7 ans)
- Tableau de suivi des impayés + séquence de relances
- Dossier mensuel prêt-à-envoyer au comptable

## Workflow

### 1. Le rituel mensuel (date fixe, ex. le 3 du mois)

1. **Exporter les factures émises** du mois écoulé (UBL/PDF) depuis l'outil Peppol —
   *critère : le nombre de factures correspond au journal des ventes de l'outil.*
2. **Collecter les factures d'achat** : boîte mail dédiée (ex. `factures@…`), portails
   fournisseurs, Peppol entrant — *critère : chaque débit bancaire « fournisseur » a
   une pièce associée ou une note d'explication.*
3. **Rapprochement bancaire** : exporter le relevé CSV du mois, pointer chaque ligne
   vers une facture ou une catégorie (perso, TVA, cotisations, virement compte pro) —
   *critère : zéro ligne « ? » non expliquée.*
4. **Suivi des impayés** : mettre à jour le tableau, déclencher les relances dues (§4).
5. **Envoyer le dossier mensuel** au comptable (ou classer si autogestion) —
   *critère : dossier horodaté transmis, accusé du comptable.*

### 2. Arborescence d'archivage (conservation 7 ans)

```
compta/
  2026/
    01-janvier/
      ventes/            # factures émises (UBL + PDF lisible)
      achats/            # factures fournisseurs reçues
      banque/            # relevés CSV + PDF
      notes/             # justificatifs sans facture (petits frais, km)
    02-fevrier/
      …
  declarations/          # TVA, listings, IPP/ISOC par année
  contrats/              # clients, bail, assurances
```

- Noms de fichiers normalisés : `2026-01-15_fournisseur_montant.pdf`.
- **UBL conservé** pour les factures Peppol (c'est l'original légal, pas le PDF).
- Copie hors du poste de travail (cloud chiffré ou disque externe) : le disque qui
  lâche n'est pas une excuse recevable.

### 3. Dossier mensuel pour le comptable

Envoyer en **un seul paquet daté** : factures ventes + achats + relevé bancaire +
notes de frais + tableau impayés. Poser les questions **par écrit** dans le même envoi
(« cette dépense mixte, je la déduis comment ? ») — chaque aller-retour éclaté coûte
des honoraires. *Critère : le comptable n'a rien à réclamer.*

### 4. Impayés : suivi et relances

Tableau minimal : client | n° facture | montant | échéance | statut | dernière relance.

| Jour | Action |
|---|---|
| Échéance +1 | Rappel courtois par email (ton neutre, facture en pièce jointe) |
| +7 | Relance ferme : rappel des intérêts de retard légaux B2B et clause d'indemnité si prévue aux conditions |
| +15 | Mise en demeure recommandée (modèle à faire valider) |
| +30+ | Options : médiation, avocat, recouvrement, ou provision pour créance douteuse |

- En B2B, les **intérêts de retard** sont dus de plein droit dès le lendemain de
  l'échéance (loi sur les retards de paiement — *vérifier le taux semestriel en
  vigueur*), sans mise en demeure préalable.
- *Critère : aucun impayé > 15 jours sans action datée.*

### 5. Petits frais et dépenses mixtes

- Frais sans facture (parking, petit matériel) : note de frais mensuelle datée +
  preuve de paiement bancaire.
- Dépenses mixtes (gsm, voiture, internet, bureau à domicile) : noter le **pourcentage
  professionnel revendiqué** et sa justification — le comptable tranche, pas toi.
- Titres-repas / écochèques : règles spécifiques, à cadrer avec le comptable dès la
  première utilisation.

## Références belges

- **SPF Finances** : obligations de conservation (7 ans), livres et documents exigibles,
  taux d'intérêts de retard B2B.
- **Loi du 2 août 2002** relative aux retards de paiement dans les transactions commerciales.
- **Codex des sociétés / droit comptable** : obligations renforcées pour SRL
  (comptabilité double, dépôt des comptes annuels à la BNB).
- **BNB — Centrale des bilans** : dépôt des comptes annuels (SRL).
- Données datées : **as_of 2026-07** — vérifier les délais et taux en vigueur.

## Common Pitfalls

1. **Le tiroir à tickets annuel.** Sans rituel mensuel, la clôture devient un cauchemar
   facturé au prix fort par le comptable. Le rituel à date fixe est LA solution.
2. **Jeter l'UBL.** Pour une facture Peppol, l'UBL est l'original légal ; un PDF régénéré
   ne le remplace pas en cas de contrôle.
3. **Lignes bancaires fantômes.** Un virement « perso » non marqué finit en question de
   contrôle. Tout pointer, chaque mois.
4. **Relances molles et irrégulières.** Un impayé sans suivi structuré devient une
   créance irrécouvrable ; la loi B2B donne des armes (intérêts de plein droit) — les
   utiliser, par écrit, à dates fixes.
5. **Mélanger les années.** Chaque dossier annuel doit être clos (ventes complètes,
   achats complets, relevés) avant d'archiver ; une pièce de décembre classée en
   janvier décale la TVA.
6. **Autogestion SRL sans comptable.** La SRL impose comptabilité double + comptes
   annuels : l'autogestion totale y est un faux-économie pour la plupart des profils.

## Verification Checklist

- [ ] Rituel mensuel à date fixe dans l'agenda (récurrent)
- [ ] Arborescence d'archivage créée et sauvegardée hors poste
- [ ] Dernier mois : ventes, achats, banque, notes — tous pointés, zéro « ? »
- [ ] Tableau impayés à jour, relances dues envoyées
- [ ] Dossier mensuel transmis au comptable avec questions écrites
- [ ] Originaux UBL conservés pour toutes les factures Peppol

> ⚠️ **Disclaimer** : information générale (as_of 2026-07), pas un conseil comptable
> personnalisé. Les modalités de conservation, de déduction et de relance doivent être
> validées avec votre comptable ou expert-comptable agréé en Belgique.
