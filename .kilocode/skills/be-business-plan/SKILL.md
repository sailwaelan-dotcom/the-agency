---
name: be-business-plan
description: "Utilisez quand le solopreneur belge doit rédiger un business plan (banque, subside, notaire pour SRL), construire son plan financier prévisionnel (obligatoire au CSA pour SRL), évaluer son breakeven, ou préparer un dossier de financement. Produit un plan structuré prêt à faire valider."
version: 0.1.0
license: MIT
author: The Agency
metadata:
  tags: [business, finance, rd, strategy, be]
  related_skills: [be-market-research, be-funding-subsidies, be-company-setup, be-accounting-basics]
  domain: rd
  language: fr
  as_of: "2026-07"
---

# Business plan belge (banque / notaire / subside)

## Overview

En Belgique, le business plan sert à trois guichets différents : la **banque** (crédit),
le **notaire** (plan financier SRL, exigé par le CSA — le document le plus normé),
et les **organismes de subside/accompagnement** (VLAIO, SPW, Innoviris, microStart…).
Ce skill produit un plan structuré qui satisfait les trois, avec le focus réglementaire
belge : hypothèses chiffrées à 2-3 ans, scénario pessimiste, breakeven, et — pour SRL —
la preuve que l'apport suffit aux 2 premières années.

## When to Use

- « Je dois faire un business plan pour la banque / le notaire / un subside »
- « C'est quoi un plan financier pour une SRL ? »
- « Combien d'apport je dois prévoir pour ma SRL ? »
- « Mon breakeven, je le calcule comment ? »

**Ne pas utiliser pour :**
- L'étude de marché en amont → `be-market-research`
- Le détail des guichets de subside → `be-funding-subsidies`
- La création juridique → `be-company-setup`

## Structure du plan (8 blocs)

1. **Résumé exécutif** — 1 page, écrit en dernier. Projet, marché, avantage, besoin de financement, usage des fonds.
2. **Porteur de projet** — parcours, compétences clés, ce qui te rend crédible sur CE marché.
3. **Produit/service** — problème, solution, différenciation, stade (idée/MVP/ventes).
4. **Étude de marché** — issue de `be-market-research` : taille, segments, concurrence, pricing observé. **Un plan sans données de marché sourcées est refusé.**
5. **Stratégie commerciale** — canaux d'acquisition réalistes pour un solo, cycle de vente, objectifs chiffrés par trimestre.
6. **Moyens** — outils, fournisseurs, local éventuel, temps alloué.
7. **Plan financier** — le cœur normatif (voir ci-dessous).
8. **Annexes** — CV, lettres d'intention, devis, preuves de traction.

## Le plan financier (norme CSA pour SRL)

Le notaire exige pour la constitution d'une SRL un plan financier couvrant **au minimum 2 ans**, comprenant :

- **Compte de résultats prévisionnel** : CA par produit/segment, charges détaillées
  (cotisations INASTI, loyer, outils, marketing, comptable, assurances)
- **Plan d'investissement** : matériel, développement, stock
- **Plan de financement** : apport (numéraire/nature), crédit, subsides visés
- **Plan de trésorerie mensuel** année 1 (le document qui tue les mauvais projets) :
  encaissements réels (délais clients 30-60j) vs décaissements (TVA trimestrielle,
  cotisations, fournisseurs)
- **Hypothèses écrites** : chaque chiffre doit être justifiable (« 10 clients × 500 €/mois
  dès le mois 4 » avec la preuve pipeline)

### Règles de crédibilité

- **Trois scénarios** : pessimiste (CA −40 %), central, optimiste. La banque lit le pessimiste.
- **Breakeven calculé** : charges fixes annuelles ÷ marge brute unitaire = volume à vendre.
  Convertir en « clients/mois » : si le chiffre dépasse ton carnet d'adresses ×10, le modèle est faux.
- **Apport SRL suffisant** : le CSA exige que les fonds propres couvrent les besoins
  prévisibles sur 2 ans ; un apport symbolique avec un plan déficitaire = responsabilité
  des fondateurs en cas de faillite précoce.
- **Apport en nature** (matériel, code, stock) : rapport d'un **réviseur d'entreprises**
  obligatoire — anticiper le coût et le délai (plusieurs semaines).

### Ordres de grandeur à provisionner (as_of 2026-07 — vérifier)

- Cotisations sociales indépendant : ≈ 20,5 % du net, minimums dès la 1re année
- Impôt : provisionner 30-50 % du bénéfice selon tranche (IPP) ou ISOC + précompte mobilier (SRL)
- Frais de création SRL : notaire + publication + guichet (devis notaire à demander)
- Comptable : forfait mensuel selon volume — demander 2-3 offres

## Workflow

1. **Cadrer le guichet** — banque, notaire, subside ? Le même socle, trois habillages.
   *Critère : le destinataire et son critère de décision sont écrits.*
2. **Assembler marché + pricing** — sorties de `be-market-research`.
   *Critère : chaque affirmation marché a une source citée.*
3. **Construire le prévisionnel 24-36 mois** — mensuel année 1, trimestriel ensuite.
   *Critère : le plan de trésorerie ne passe jamais sous zéro dans le scénario central,
   ou le besoin de financement est chiffré exactement.*
4. **Stresser** — scénario pessimiste + breakeven + sensibilité (prix −10 %, délai paiement +30j).
   *Critère : le projet survit au pessimiste, ou le plan dit honnêtement ce qui doit être vrai.*
5. **Rédiger le résumé + annexes** — *critère : un lecteur pressé comprend projet,
   marché, demande et usage des fonds en 1 page.*
6. **Faire relire** — comptable pour les chiffres, guichet d'accompagnement régional
   (souvent gratuit) pour la forme. *Critère : une relecture externe documentée avant envoi.*

## Références belges

- **CSA (Code des sociétés et des associations)** : contenu légal du plan financier SRL
- **Notaire** : modèles de plan financier acceptés, exigences apport en nature
- **Guichets d'accompagnement régionaux** : relecture gratuite (hub.brussels, Awex,
  VLAIO partners, UCM, UWE…) — vérifier celui de ta région
- **SPF Économie / BNB** : statistiques sectorielles pour étayer le marché
- Données datées : **as_of 2026-07** — vérifier les exigences en vigueur.

## Common Pitfalls

1. **Prévisionnel copié d'un template** sans lien avec ton pipeline réel. La banque
   détecte les courbes lisses ; chaque chiffre doit tracer vers une preuve.
2. **Oublier la TVA dans la trésorerie.** Tu encaisses TVAC, tu reverses trimestriellement :
   le solde TVA dort sur le compte et n'est PAS du cash disponible.
3. **Apport SRL symbolique + plan gourmand.** Si la société fait faillite dans les 3 ans
   faute de fonds propres suffisants, les fondateurs risquent d'y laisser leur responsabilité.
4. **Pas de scénario pessimiste.** Un plan qui ne survit qu'au scénario parfait est un refus garanti.
5. **Sous-estimer les délais de paiement B2B** (30-60 jours). Le CA n'est pas de la trésorerie.
6. **Rédiger le résumé en premier.** Il se construit en dernier, une fois les chiffres figés.

## Verification Checklist

- [ ] Destinataire et critère de décision identifiés
- [ ] Données de marché sourcées (cf. be-market-research)
- [ ] Prévisionnel 24+ mois avec trésorerie mensuelle année 1
- [ ] 3 scénarios + breakeven en clients/mois
- [ ] Hypothèses écrites et justifiées une par une
- [ ] SRL : apport couvre les besoins 2 ans ; réviseur prévu si apport en nature
- [ ] Relecture externe (comptable / guichet régional) avant envoi

> ⚠️ **Disclaimer** : information générale (as_of 2026-07), pas un conseil financier,
> fiscal ou juridique personnalisé. Le plan financier d'une SRL engage la responsabilité
> des fondateurs : faites-le valider par un expert-comptable et votre notaire avant tout dépôt.
