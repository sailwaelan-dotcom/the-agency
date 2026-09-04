---
name: be-devis-quotes
description: "Utilisez quand le solopreneur belge doit chiffrer et envoyer un devis : tarification (TJM, forfait, par phase), structure du document, mentions légales (BCE, TVA), numérotation, validité, acompte, relance d'un devis sans réponse, ou transformation d'un devis accepté en facture Peppol. Produit un devis conforme prêt à envoyer et un suivi des devis émis."
version: 1.0.0
license: MIT
author: The Agency
metadata:
  tags: [sales, devis, pricing, be]
  related_skills: [be-sales-outreach, be-invoicing-peppol, be-contracts-legal]
  domain: sales
  language: fr
  as_of: "2026-09"
---

# Devis et chiffrage — solopreneur belge

## Overview

Le devis est l'endroit où le solopreneur gagne ou perd sa rentabilité : mal
structuré, il ouvre la porte au scope creep ; sans acompte, il porte 100 % du
risque de impayé ; sans numérotation, la traçabilité jusqu'à la facture se perd.

Ce skill couvre la chaîne complète : cadrage du besoin, tarification, rédaction
d'un devis conforme aux mentions belges, numérotation et archivage, envoi,
relance, puis transformation du devis accepté en facture. Il produit un document
prêt à envoyer et un suivi des devis émis (statut, montant, relance).

## When to Use

- « Je dois envoyer un devis à un prospect, je mets quoi dedans ? »
- « Comment je tarife ma prestation — TJM, forfait, au projet ? »
- « Combien d'acompte je demande ? »
- « Le prospect ne répond pas à mon devis, je relance comment ? »
- « Mon client a validé le devis, je passe à la facture comment ? »

**Ne pas utiliser pour :**
- Prospecter / négocier en amont → `be-sales-outreach`
- Émettre la facture définitive (Peppol, UBL, mentions de facture) → `be-invoicing-peppol`
- Rédiger des CGV complètes ou un contrat de prestation → `be-contracts-legal`
- Décider du prix final : le skill prépare des fourchettes argumentées, le
  solopreneur tranche.

## Mentions d'un devis solide (as_of 2026-09 — à faire vérifier par un pro)

Un devis n'a pas de cadre légal aussi strict que la facture en Belgique, mais
une fois signé il vaut engagement contractuel — ses mentions protègent les
deux parties :

| Mention | Pourquoi |
|---|---|
| Nom / raison sociale, adresse, **n° BCE** (+ n° TVA si assujetti) du prestataire | Identification commerciale ; sans BCE, pas de facture propre ensuite |
| Coordonnées du client (+ n° BCE/TVA si B2B) | Nécessaire dès le devis pour le routage **Peppol** de la future facture |
| **Numéro de devis** en séquence (ex. `DEV-2026-014`) | Traçabilité devis → facture, zéro doublon |
| Date d'émission et **validité** (30 jours recommandé) | Après la validité, les prix sont à reconfirmer — pas de vieil engagement |
| Description des livrables **et des exclusions** | Le scope creep se paie en heures non prévues |
| Prix par ligne/phase, **HTVA**, taux de TVA applicable | Franchise TVA → mention « Franchise de TVA — art. 56bis CTVA » et pas de TVA facturée (*vérifier la mention en vigueur*) |
| **Acompte** et échéancier de solde (30-50 % à la commande est un ordre de grandeur courant) | Limite le risque d'impayé ; à ajuster selon la relation et le montant |
| Conditions de paiement et de révision (délai, pénalités de retard éventuelles) | Évite le « je paierai quand ça m'arrange » |
| Renvoi vers les CGV | Les CGV portent les clauses que le devis ne peut pas contenir → `be-contracts-legal` |

> ⚠️ Un devis signé engage généralement les deux parties. Toute clause sensible
> (pénalités, propriété intellectuelle, révisions illimitées) se fait vérifier
> par un juriste avant usage récurrent.

## Workflow

### 1. Cadrer le besoin

Avec le prospect : objectif métier, livrables attendus, délais, budget annoncé
(s'il le dit), ce qui est HORS périmètre.

*Critère de complétion* : le scope tient en 5-10 lignes écrites, avec une liste
d'exclusions explicite. Un devis sans exclusions est un devis refusé.

### 2. Tarifier par phases

Trois modes de tarification, à combiner :

- **TJM** (taux journalier moyen) : pour le conseil / l'itératif dont le périmètre
  bouge. Le TJM se cale sur le marché du secteur et l'expérience — pas sur « ce
  que le client peut payer ce mois-ci ».
- **Forfait** : pour un livrable défini. Le forfait se prix sur la base d'une
  estimation en jours × TJM + marge de risque (15-25 % sur l'inconnu).
- **Par phase** : découper en 2-4 phases facturables séparément (cadrage →
  réalisation → ajustements). Le client peut arrêter à chaque jalon, toi tu
  n'avances pas de trésorerie.

Ajouter les frais refacturables (licences, déplacements) en lignes séparées,
jamais noyés dans le prix.

*Critère de complétion* : chaque phase a un prix, une durée estimée et une
phrase qui dit ce qu'elle couvre. Le total HTVA est cohérent avec la somme des
phases.

### 3. Rédiger le devis

Utiliser le tableau des mentions ci-dessus comme checklist de rédaction : une
ligne par livrable/phase, les exclusions en section visible, la validité datée,
l'acompte en gras, les conditions de paiement. Ton : celui de la marque du
solopreneur (→ `brand-voice-solopreneur` si une charte existe), sans jargon
non défini.

*Critère de complétion* : les 9 mentions du tableau sont présentes ou
explicitement non applicables avec la raison.

### 4. Numéroter et tracer

Séquence unique par année (`DEV-2026-014`), registre simple (numéro, client,
montant HTVA, date d'envoi, statut : brouillon / envoyé / signé / refusé /
expiré) dans l'outil du solopreneur — tableur suffit au début.

*Critère de complétion* : le devis est enregistré avec son statut « envoyé » et
sa date. Un devis non tracé est un devis qui se rééditera en doublon.

### 5. Envoyer et relancer

Envoyer avec un message court qui rappelle le livrable, le prix total, la
validité et propose un échange. Planifier les relances **à l'émission**, pas de
tête : J+7 (email courtois), J+14 (email + proposition d'appel), après J+21 →
passer au téléphone ou clore. La relance fait partie du chiffrage : un devis
sans réponse suivi, c'est du temps vendu à zéro.

*Critère de complétion* : deux créneaux de relance datés existent avant que la
première heure de production ne démarre.

### 6. Conclure — devis accepté → facture

Devis signé (ou accord écrit) : facturer l'acompte immédiatement via
`be-invoicing-peppol` (en B2B, la facture part par Peppol — le n° BCE/TVA du
client collecté à l'étape 3 sert ici), noter la référence du devis dans la
facture, mettre le statut du devis à « signé » et démarrer la phase 1.
Devis refusé : noter la raison (prix, timing, choix concurrent) dans le
registre — c'est la donnée qui affine la prochaine tarification.

*Critère de complétion* : chaque devis signé a une facture d'acompte émise ;
chaque devis refusé a une raison notée.

## Common Pitfalls

1. **Vendre des jours, promettre des résultats.** Le devis décrit des livrables,
   pas des heures invisibles. Sans livrables définis, chaque malentendu devient
   gratuit pour le client.
2. **Un prix global unique, sans phases.** Impossible de négocier sans tout
   défaire ; impossible d'arrêter proprement. Toujours 2-4 phases.
3. **Pas de validité.** Le client revient six mois plus tard aux prix d'hier.
   30 jours datés, puis re-devis.
4. **Zéro acompte.** Le solopreneur finance le client. Acompte systématique
   (ordre de grandeur : 30-50 %) sauf relation éprouvée.
5. **Oublier de collecter le n° BCE/TVA du client B2B au stade du devis.** La
   facture Peppol en dépend ; la réclamer après signature rallonge le paiement.
6. **Numérotation à la main, au coup par coup.** Doublons, trous, contrôles
   fiscaux pénibles. Une séquence par année, tenue dès le premier devis.
7. **Chiffrer en séance sous pression.** Le prix annoncé en réunion ancre la
   négociation. « Je vous envoie le devis sous 48 h » est une réponse complète.
8. **Confondre devis et contrat.** Le devis signé engage, mais il ne remplace
   pas des CGV (propriété intellectuelle, responsabilité, révisions). Faire
   rédiger les CGV une fois, les renvoyer sur chaque devis → `be-contracts-legal`.

## Verification Checklist

- [ ] Scope écrit avec exclusions explicites
- [ ] Tarification par phases, total HTVA cohérent, frais refacturables séparés
- [ ] Les 9 mentions du tableau présentes (ou justifiées non applicables)
- [ ] Numéro de devis en séquence, registre à jour, statut « envoyé » daté
- [ ] Validité datée (30 jours) et acompte défini (30-50 % sauf exception motivée)
- [ ] Deux relances planifiées avant démarrage de la production
- [ ] N° BCE/TVA du client B2B collecté (routage Peppol de la future facture)
- [ ] Renvoi vers les CGV présent

> ⚠️ **Disclaimer** : information générale (as_of 2026-09), pas un conseil
> juridique ou fiscal personnalisé. Un devis signé est un document engageant :
> faites valider vos CGV et vos clauses sensibles par un juriste, et vos
> mentions TVA par un comptable agréé en Belgique.
