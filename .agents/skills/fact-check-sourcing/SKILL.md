---
name: fact-check-sourcing
description: "Utilisez quand le solopreneur belge doit vérifier l'exactitude d'un chiffre, d'une affirmation ou d'une référence dans un document (business plan, dossier de subside, contenu marketing) : sourcing, vérification de dates, validation de montants, format de citation. Produit un rapport de fiabilité des sources."
version: 0.1.0
license: MIT
author: The Agency
metadata:
  tags: [business, rd, research, sourcing, be]
  related_skills: [be-market-research, be-business-plan, be-funding-subsidies, content-engine-be]
  domain: rd
  language: fr
  as_of: "2026-07"
---

# Fact-checking, sourcing & citation — solopreneur belge

## Overview

Ce skill est le **garde-fou de la crédibilité** du repo The Agency. Il fournit une
méthodologie rigoureuse pour vérifier chaque affirmation chiffrée, chaque référence
réglementaire, chaque montant cité dans un document business. Il produit un **rapport
de fiabilité** qui identifie les sources vérifiées, les affirmations non sourcées, et
les données potentiellement obsolètes. Obligatoire avant tout envoi de business plan,
dossier de subside, ou contenu marketing qui cite des chiffres.

## When to Use

- « Ce chiffre TVA/cotisation/subside est-il encore à jour ? »
- « J'ai cité une source dans mon business plan, est-elle fiable ? »
- « Mon dossier de subside contient des affirmations — je dois les sourcer »
- « Mon contenu marketing cite des statistiques — sont-elles vérifiables ? »
- « Je dois produire une bibliographie pour un document officiel »

**Ne pas utiliser pour :**
- L'étude de marché elle-même → `be-market-research`
- La veille concurrentielle → `be-competitor-watch`
- La production de contenu → `content-engine-be`

## Hiérarchie des sources (du plus au moins fiable)

| Niveau | Type de source | Exemples | Fiabilité |
|---|---|---|---|
| **1 — Primaire** | Texte de loi, règlement, arrêté royal | Code des sociétés (CSA), Code de la TVA (CTVA), RGPD (UE 2016/679) | Maximale |
| **2 — Officielle** | Site gouvernemental, statistiques publiques | SPF Finances, INASTI, Statbel, BNB, BCE, VLAIO, Awex | Très haute |
| **3 — Institutionnelle** | Rapport d'organisme reconnu | Febelfin, Agoria, UCM, VOKA, chambres de commerce | Haute |
| **4 — Académique** | Article peer-reviewed, thèse, livre de référence | Universités belges, éditions juridiques Larcier/Bruylant | Haute |
| **5 — Journalistique** | Article de presse spécialisé | L'Écho, Trends-Tendances, De Tijd, Made In | Moyenne |
| **6 — Sectorielle** | Blog, newsletter, podcast d'expert | Blogs de comptables, newsletters sectorielles | Moyenne |
| **7 — Anecdotique** | Témoignage, avis client, forum | Trustpilot, Reddit, LinkedIn | Faible |

**Règle** : toute affirmation chiffrée dans un document officiel doit être sourcée au
niveau 1-4. Les niveaux 5-7 sont acceptables pour du contenu marketing mais pas pour
un business plan ou un dossier de subside.

## Méthodologie de fact-checking (5 étapes)

### 1. Extraire les affirmations

Lister chaque affirmation chiffrée ou réglementaire du document :
- Montants (TVA, cotisations, subsides, prix)
- Dates (échéances, entrée en vigueur, délais)
- Pourcentages (taux, seuils, parts de marché)
- Références légales (articles, arrêtés, règlements)

*Critère de complétion* : chaque affirmation est identifiée et numérotée.

### 2. Identifier la source

Pour chaque affirmation, noter :
- La source citée dans le document (URL, nom, date)
- Le niveau de fiabilité (1-7)
- La date de la source (quand a-t-elle été publiée/mise à jour ?)

*Critère de complétion* : chaque affirmation a une source identifiée avec son niveau.

### 3. Vérifier l'exactitude

Pour chaque affirmation, vérifier :
- **Le montant/chiffre** est-il correct sur la source citée ?
- **La date** est-elle la plus récente disponible ?
- **Le contexte** est-il respecté (ex: taux réduit vs taux normal) ?
- **La référence légale** est-elle complète et correcte (article, alinéa, paragraphe) ?

**Sources de vérification officielles belges** :

| Domaine | Source officielle | URL |
|---|---|---|
| TVA | SPF Finances | finances.belgium.be |
| Cotisations sociales | INASTI | rsvz-inasti.fgov.be |
| Statistiques entreprises | SPF Économie | statistiques.fgov.be |
| Données macro | Banque Nationale de Belgique | nbr.be |
| Statistiques démographiques | Statbel | statbel.fgov.be |
| Subsides régionaux | VLAIO / Awex / hub.brussels / Innoviris | vlaio.be / awex.be / hub.brussels / innoviris.brussels |
| Protection données | APD/GBA | autoriteprotectiondonnees.be |
| Code des sociétés | CSA | ejustice.just.fgov.be |
| Registre entreprises | BCE/KBO | kbopub.economie.fgov.be |

*Critère de complétion* : chaque affirmation vérifiée = source consultée + résultat
(confirmé / infirmé / obsolète / non vérifiable).

### 4. Dater et marquer

Chaque chiffre cité doit porter :
- `as_of: YYYY-MM` — date de la dernière vérification
- « Vérifier le taux en vigueur » — si le chiffre peut évoluer
- Source complète : nom + URL + date de consultation

*Critère de complétion* : chaque chiffre du document a un `as_of` et une source.

### 5. Produire le rapport de fiabilité

Format du rapport :

```
RAPPORT DE FIABILITÉ — [Nom du document]
Date : YYYY-MM-DD
Vérifié par : [Nom/Agent]

RÉSUMÉ :
- Affirmations vérifiées : X/Y
- Sources niveau 1-4 : X/Y
- Données obsolètes : X
- Non vérifiables : X

DÉTAIL :
# | Affirmation | Source | Niveau | Statut | Action
1 | TVA 21 % | SPF Finances | 2 | ✅ Confirmed | —
2 | Subside 15 000 € | Awex | 2 | ⚠️ Obsolète | Vérifier montant actuel
3 | Marché 50 M€ | Estimation | 7 | ❌ Non sourcé | Trouver source niveau 1-4

ACTIONS REQUISES :
- [ ] Vérifier le montant du subside Awex (ligne 2)
- [ ] Sourcer le chiffre de marché (ligne 3)
```

## Format de citation

### Dans le texte
```
Selon le SPF Finances (finances.belgium.be, consulté le 15/01/2026), le taux de TVA
standard en Belgique est de 21 %.
```

### En bibliographie
```
SPF Finances. "Taux de TVA". finances.belgium.be. Consulté le 15/01/2026.
https://finances.belgium.be/fr/entreprises/tva/taux
```

### Pour les données datées
```
Statbel. "Population par commune". statbel.fgov.be. Données au 01/01/2026.
https://statbel.fgov.be/fr/themes/population
```

## Auto-fact-check (checklist avant envoi)

Avant d'envoyer tout document contenant des chiffres :
- [ ] Toute affirmation chiffrée a une source niveau 1-4
- [ ] Toute source a un `as_of` (date de vérification)
- [ ] Les montants ont été vérifiés sur la source officielle
- [ ] Les dates d'entrée en vigueur sont confirmées
- [ ] Les références légales sont complètes (article + alinéa)
- [ ] Le rapport de fiabilité est produit

## Common Pitfalls

1. **Citer un chiffre sans source.** « Le marché vaut 50 M€ » sans source = affirmation
   non vérifiable = rejeté par toute institution sérieuse.
2. **Utiliser une source obsolète.** Un taux de TVA de 2019 ne vaut rien en 2026.
   Toujours vérifier la date de dernière mise à jour de la source.
3. **Confondre taux normal et réduit.** 21 % est le taux normal, 6 % et 12 % sont
   réduits — le contexte de l'affirmation doit préciser lequel s'applique.
4. **Citer un blog comme source officielle.** Un blog de comptable est niveau 6, pas
   niveau 2. Pour un business plan, remonter à la source primaire.
5. **Oublier le `as_of`.** Un chiffre sans date est un chiffre mort — il ne peut pas
   être vérifié ni mis à jour.
6. **Copier-coller des statistiques sans les vérifier.** La source originale peut
   avoir été corrigée ou mise à jour depuis la citation initiale.

## Verification Checklist

- [ ] Méthodologie 5 étapes appliquée
- [ ] Hiérarchie des sources respectée (niveau 1-4 pour documents officiels)
- [ ] Rapport de fiabilité produit
- [ ] `as_of` présent sur chaque chiffre
- [ ] Sources vérifiées sur les sites officiels belges
- [ ] Format de citation cohérent

> ⚠️ **Disclaimer** : information générale (as_of 2026-07), pas un conseil juridique
> ou comptable personnalisé. Les sources officielles évoluent — vérifier chaque
> chiffre sur la source le jour de l'utilisation. Pour des documents engageants
> (business plan, dossier de subside), faire valider par un expert-comptable ou
> un avocat agréé en Belgique.
