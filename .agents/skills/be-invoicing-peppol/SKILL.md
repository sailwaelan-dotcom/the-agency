---
name: be-invoicing-peppol
description: "Utilisez quand le solopreneur doit émettre une facture B2B en Belgique (Peppol obligatoire depuis janvier 2026), choisir un logiciel/Access Point, vérifier les mentions légales d'une facture, ou comprendre la différence entre facture PDF et facture électronique structurée."
version: 0.1.0
license: MIT
author: The Agency
metadata:
  tags: [finance, accounting, invoicing, peppol, be]
  related_skills: [be-accounting-basics, be-bookkeeping-ops]
  domain: finance
  language: fr
  as_of: "2026-07"
---

# Facturation B2B belge & Peppol

## Overview

Depuis le **1er janvier 2026**, la facturation électronique structurée via le réseau
**Peppol** est obligatoire pour les transactions B2B domestiques entre assujettis TVA
établis en Belgique. Une simple facture PDF envoyée par email **ne suffit plus** entre
entreprises belges : il faut un fichier structuré (format **Peppol BIS 3.0**, basé sur
UBL 2.1) transmis via un **Access Point** Peppol.

Ce skill guide l'émission d'une facture conforme : vérifier si le client est joignable
sur Peppol, choisir l'outil d'envoi, contrôler les mentions légales TVA, et archiver
correctement. Il couvre le cas standard du solopreneur (SRL ou indépendant personne
physique, régime normal ou franchise) — pas la facturation intracommunautaire détaillée
ni l'e-reporting (annoncé pour 2028, hors périmètre ici).

## When to Use

- « Je dois envoyer une facture à un client belge (entreprise) »
- « Peppol c'est quoi / suis-je concerné ? »
- « Mon client me demande ma facture au format électronique / UBL / Peppol »
- « Quel logiciel pour facturer en Belgique ? »
- « Je viens de créer ma SRL, comment je facture ma première mission ? »

**Ne pas utiliser pour :**
- La déclaration TVA périodique → `be-accounting-basics`
- L'organisation mensuelle des pièces comptables → `be-bookkeeping-ops`
- La vente à des particuliers (B2C) : Peppol non obligatoire, mais les mentions légales
  ci-dessous restent valables pour la facture papier/PDF.

## Inputs & Sorties

**Entrées nécessaires** (demander à l'utilisateur si manquantes) :
- Votre numéro d'entreprise BCE (`BE0123.456.789` comme placeholder) et statut TVA
  (régime normal, franchise, ou forfait)
- Le numéro d'entreprise/TVA du client (mentionné sur son bon de commande ou son site)
- Nature de la prestation (bien/service), montant HTVA, taux TVA applicable
- Votre outil actuel de facturation (logiciel, Excel, Word…)

**Sortie** :
- Une checklist de conformité remplie pour la facture concernée
- Une recommandation d'outil/Access Point adaptée au profil (volume, budget, comptable)
- Le cas échéant, un squelette de facture avec toutes les mentions légales belges

## Workflow

### 1. Déterminer si Peppol s'applique

- Client = entreprise **belge** assujettie TVA → **Peppol obligatoire** (sauf client au
  régime de franchise/forfait, ou vous-même en franchise : vérifier le cas).
- Client = particulier ou entreprise **étrangère** → Peppol non obligatoire (une facture
  PDF conforme reste légale ; le format électronique est une option).
- *Critère de complétion* : la réponse « obligatoire / non obligatoire / à vérifier »
  est tranchée et justifiée en une phrase.

### 2. Vérifier la présence du client sur Peppol

- Rechercher le client dans l'annuaire public Peppol avec son numéro BCE ou TVA
  (ex: directory.peppol.eu — outil de recherche officiel du réseau).
- Identifiant Peppol belge standard : `0208:` + numéro BCE (ex: `0208:0123456789`).
- **Outillage MCP (`agency-be-mcp`)** : Si le serveur MCP est activé dans votre harness, exécutez l'outil `lookup_peppol_participant(bce_number="...")` pour sonder automatiquement l'annuaire OpenPeppol en direct, et `validate_bce_number(bce_number="...")` pour valider mathématiquement le numéro BCE (Modulo 97).
- Si absent de l'annuaire : le client n'est pas (encore) inscrit → facture PDF conforme
  par email + lui signaler que l'inscription Peppol est obligatoire pour lui aussi.
- *Critère de complétion* : identifiant Peppol du client noté, ou absence documentée.

### 3. Choisir l'outil d'émission

Catégories (liste non exhaustive, pas de recommandation commerciale) :

| Profil | Option type | Remarque |
|---|---|---|
| 0-10 factures/mois | Logiciel de facturation belge avec Peppol intégré | Souvent ~5-20 €/mois, envoi/réception inclus |
| Comptable existant | Le logiciel du comptable (beaucoup sont déjà Access Point-ready) | Demander avant d'en choisir un autre |
| Développeur/intégration | Access Point agréé + API | Pour volumes ou intégration produit |
| Gratuit/minimal | Certains outils proposent un tier gratuit limité | Vérifier que l'envoi Peppol est inclus, pas seulement le PDF |

- La liste officielle des Access Points agréés est publiée par l'autorité Peppol belge
  (SPF BOSA). La plupart des logiciels comptables/facturation belges la gèrent pour vous.
- *Critère de complétion* : un outil choisi ET la réception Peppol activée (l'obligation
  porte aussi sur la **réception** des factures fournisseurs).

### 4. Contrôler les mentions légales de la facture

Toute facture belge (Peppol ou PDF) doit contenir :

- [ ] Numéro **séquentiel ininterrompu** (par journal de ventes)
- [ ] Date d'émission (+ date de livraison/prestation si différente)
- [ ] Vos nom/dénomination, adresse, numéro BCE précédé de « TVA BE » (ex: `TVA BE 0123.456.789`)
- [ ] Nom, adresse et numéro TVA du client
- [ ] Description, quantité, prix unitaire HTVA par ligne
- [ ] Taux TVA par ligne (21 % taux normal ; 6 % et 12 % pour catégories réduites —
      **vérifier le taux applicable** à votre activité sur le site du SPF Finances)
- [ ] Total HTVA, montant TVA par taux, total TVAC
- [ ] Date et conditions de paiement (délai légal B2B par défaut : 30 jours)
- [ ] Mention spéciale le cas échéant : « Autoliquidation » (sous-traitance
      construction), « Franchise de TVA — art. 56bis CTVA », « Exonéré — art. 44 CTVA »
- [ ] Si vous utilisez une caisse enregistreuse ou êtes soumis à des règles sectorielles,
      les mentions complémentaires associées

- *Critère de complétion* : chaque case cochée sur la facture réelle, pas sur l'idée.

### 5. Envoyer et archiver

- Envoi via l'outil choisi (le fichier UBL est généré automatiquement par le logiciel).
- Archivage légal : **7 ans** (factures émises et reçues), dans un format garantissant
  l'intégrité et la lisibilité — le fichier UBL reçu/envoyé, pas une capture d'écran.
- *Critère de complétion* : facture émise (statut « envoyée » dans l'outil) + copie UBL
  archivée dans votre dossier comptable de l'année.

## Mentions légales (résumé)

Voir [references/mentions-legales-facture.md](references/mentions-legales-facture.md) pour la checklist complète avec fondement légal.

## Références belges

- **SPF Finances** (finances.belgium.be) : obligations e-invoicing 2026, mentions légales
  de facturation, taux TVA par catégorie. *Vérifier les taux et règles en vigueur au
  jour de l'émission.*
- **SPF BOSA / autorité Peppol belge** : liste des Access Points agréés, inscription
  des entreprises belges au réseau.
- **Banque-Carrefour des Entreprises (BCE)** : recherche publique du numéro d'entreprise
  d'un client (kbopub.economie.fgov.be).
- **Annuaire Peppol** (directory.peppol.eu) : vérification de l'identifiant d'un client.
- Toutes les données datées de ce skill : **as_of 2026-07**.

## Common Pitfalls

1. **Confondre facture PDF et facture électronique.** Un PDF par email n'est PAS une
   facture électronique au sens légal 2026 pour le B2B belge. Il faut un flux structuré
   UBL via Peppol. Corriger en choisissant un outil Peppol-native (étape 3).
2. **Oublier la réception.** L'obligation est symétrique : vous devez aussi **recevoir**
   les factures fournisseurs via Peppol. Activer la réception dans votre outil, sinon
   vos fournisseurs ne peuvent pas vous facturer légalement.
3. **Numérotation non séquentielle.** Recommencer la numérotation chaque mois, ou
   supprimer une facture brouillon du lot, casse l'exigence de séquence ininterrompue.
   Utiliser des notes de crédit pour annuler, jamais la suppression.
4. **Mauvais taux TVA.** Appliquer 21 % « par défaut » sur une activité à taux réduit
   (ou l'inverse) fausse la facture et la déclaration. Vérifier le taux par catégorie
   sur le site du SPF Finances avant la première facture d'un nouveau type de prestation.
5. **Attendre d'avoir « le bon logiciel » pour facturer.** Le chiffre d'affaires n'attend
   pas : facturer avec un outil simple mais conforme dès la première mission, migrer
   ensuite si besoin (les données historiques restent dans l'ancien outil, archivées).
6. **Facturer sans numéro TVA actif.** S'assurer que votre numéro est activé auprès du
   guichet TVA avant la première facture (l'activation peut prendre quelques jours après
   l'inscription BCE).

## Verification Checklist

- [ ] Statut Peppol du client déterminé (annuaire consulté ou absence documentée)
- [ ] Outil d'émission/réception Peppol choisi et réception activée
- [ ] Facture contient toutes les mentions légales (numéro séquentiel, TVA BE, taux, totals)
- [ ] Mention spéciale présente si franchise/autoliquidation/exonération
- [ ] Copie UBL archivée pour 7 ans
- [ ] Taux TVA vérifié sur source officielle le jour de l'émission

> ⚠️ **Disclaimer** : information générale (as_of 2026-07), pas un conseil fiscal ou
> comptable personnalisé. Les règles d'e-invoicing et les taux TVA évoluent — vérifiez
> sur finances.belgium.be et faites valider votre configuration par un comptable ou
> expert-comptable agréé en Belgique avant votre première facture.
