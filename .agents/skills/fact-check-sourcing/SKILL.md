---
name: fact-check-sourcing
description: "GATE ACTIF — s'applique AUTOMATIQUEMENT après chaque web search, web extract, ou recherche de données. Vérifie la fiabilité des sources, croise les chiffres avec les sources officielles belges, produit un score de confiance (A/B/C/D), et bloque les informations non vérifiées avant utilisation. NE PAS utiliser uniquement à la demande — ce skill est un gate permanent."
version: 2.0.0
license: MIT
author: The Agency
metadata:
  tags: [business, rd, research, sourcing, gate, be]
  related_skills: [be-market-research, be-business-plan, be-funding-subsidies, content-engine-be, be-financial-modeling]
  domain: rd
  language: fr
  as_of: "2026-07"
---

# Fact-checking actif — gate de vérification permanent

## Overview

Ce skill n'est **pas une référence passive** — c'est un **gate actif** qui s'applique
**automatiquement après chaque web search, web extract, ou recherche de données**.
Son rôle : vérifier la fiabilité des sources, croiser les chiffres avec les sources
officielles belges, produire un score de confiance, et **bloquer les informations
non vérifiées** avant qu'elles ne soient utilisées dans un document, une réponse,
ou une décision.

**Règle absolue** : aucune donnée chiffrée issue d'une recherche web ne doit être
utilisée sans passer par ce gate.

## When to Use (AUTOMATIQUE — pas à la demande)

Ce gate s'active **systématiquement** quand :
- L'agent effectue une `web_search` ou `web_extract`
- L'agent cite un chiffre, une statistique, ou une affirmation réglementaire
- L'agent rédige un document contenant des données sourcées (business plan, dossier, contenu)
- L'agent répond à une question factuelle sur la Belgique (TVA, cotisations, subsides…)

**Ne pas utiliser pour :**
- Données déjà vérifiées dans le repo (skills internes avec `as_of`)
- Opinions ou recommandations générales (pas de chiffres à vérifier)
- Données personnelles de l'utilisateur (pas de fact-check sur ses propres données)

## Le gate : 4 étapes en 30 secondes

Après CHAQUE recherche web, l'agent applique ces 4 étapes **avant d'utiliser les données** :

### Étape 1 — Identifier la source (5 sec)

Pour chaque résultat de recherche, classifier la source :

| Niveau | Type | Exemples | Action |
|---|---|---|---|
| **A — Officielle** | Site gouvernemental, institution publique | SPF Finances, INASTI, Statbel, BNB, BCE, VLAIO, Awex, APD | ✅ Utilisable directement |
| **B — Institutionnelle** | Organisme reconnu, fédération professionnelle | Febelfin, Agoria, UCM, VOKA, chambres de commerce | ✅ Utilisable avec mention |
| **C — Journalistique** | Presse spécialisée, média reconnu | L'Écho, Trends-Tendances, De Tijd, Made In | ⚠️ Croiser avec source A/B |
| **D — Non vérifiable** | Blog, forum, réseau social, site commercial | Reddit, LinkedIn, blogs personnels, sites marketing | ❌ Ne PAS utiliser seul |

**Règle** : toute donnée de niveau C ou D doit être **croisée avec une source A ou B**
avant utilisation. Si pas de croisement disponible → marquer « non vérifié » et ne
pas l'utiliser dans un document officiel.

### Étape 2 — Vérifier la fraîcheur (5 sec)

| Situation | Action |
|---|---|
| Source avec date < 1 an | ✅ Utilisable |
| Source avec date 1-3 ans | ⚠️ Vérifier si les données ont changé |
| Source sans date | ❌ Ne PAS utiliser |
| Source avec date > 3 ans | ❌ Ne PAS utiliser (sauf données historiques) |

**Spécificités BE** : les taux TVA, cotisations INASTI, seuils de subsides changent
annuellement. Toujours vérifier la date de dernière mise à jour de la source.

### Étape 3 — Croiser avec les sources officielles BE (15 sec)

Pour toute donnée chiffrée sur la Belgique, **toujours vérifier** sur la source
officielle correspondante :

| Domaine | Source officielle à consulter |
|---|---|
| TVA, impôts, IPP/ISOC | finances.belgium.be |
| Cotisations sociales INASTI | rsvz-inasti.fgov.be |
| Statistiques entreprises | statistiques.fgov.be |
| Données macroéconomiques | nbr.be (Banque Nationale) |
| Statistiques démographiques | statbel.fgov.be |
| Subsides régionaux | vlaio.be / awex.be / hub.brussels / innoviris.brussels |
| Protection données | autoriteprotectiondonnees.be |
| Registre entreprises | kbopub.economie.fgov.be |
| Code des sociétés | ejustice.just.fgov.be |

**Méthode rapide** : extraire le chiffre clé de la recherche web, puis le vérifier
sur la source officielle avec une 2e `web_search` ou `web_extract` ciblée.

### Étape 4 — Produire le score de confiance (5 sec)

Pour chaque donnée issue d'une recherche web :

```
SCORE : [A/B/C/D] | Source : [nom] | Date : [YYYY-MM] | Croisé : [oui/non] | as_of : [YYYY-MM]
```

**Règles d'utilisation** :
- **A** : utilisable directement dans tout document
- **B** : utilisable avec mention de la source
- **C** : utilisable seulement si croisée avec source A/B
- **D** : NE PAS UTILISER — chercher une meilleure source

## Intégration dans le workflow de l'agent

### Pattern : après chaque web_search

```
1. web_search("taux TVA Belgique 2026")
2. [GATE] Classifier les résultats (étape 1)
3. [GATE] Vérifier la fraîcheur (étape 2)
4. [GATE] Si résultat C/D → web_search sur source officielle (étape 3)
5. [GATE] Produire le score (étape 4)
6. Utiliser les données dans la réponse/document
```

### Pattern : avant de citer un chiffre

```
1. Identifier le chiffre à citer
2. [GATE] Quelle est la source ? (étape 1)
3. [GATE] La source est-elle fraîche ? (étape 2)
4. [GATE] Si pas de source A/B → rechercher sur source officielle (étape 3)
5. [GATE] Produire le score (étape 4)
6. Citer avec : "Selon [source] (consulté le [date]), [chiffre] (as_of [YYYY-MM])"
```

### Pattern : dans un document (business plan, dossier)

Chaque chiffre cité doit porter :
```
[TVA standard : 21 % | Source : SPF Finances | Date consultation : 15/01/2026 | as_of : 2026-01 | Score : A]
```

## Sources officielles belges (référence rapide)

| Domaine | URL | Fiabilité |
|---|---|---|
| **TVA** | finances.belgium.be | A |
| **Cotisations sociales** | rsvz-inasti.fgov.be | A |
| **Statistiques entreprises** | statistiques.fgov.be | A |
| **Banque Nationale** | nbr.be | A |
| **Statbel** | statbel.fgov.be | A |
| **BCE/KBO** | kbopub.economie.fgov.be | A |
| **VLAIO** | vlaio.be | A |
| **Awex** | awex.be | A |
| **hub.brussels** | hub.brussels | A |
| **Innoviris** | innoviris.brussels | A |
| **APD/GBA** | autoriteprotectiondonnees.be | A |
| **CSA** | ejustice.just.fgov.be | A |
| **Febelfin** | febelfin.be | B |
| **Agoria** | agoria.be | B |
| **UCM** | ucm.be | B |
| **VOKA** | voka.be | B |

## Common Pitfalls

1. **Utiliser le premier résultat Google sans vérifier.** Le premier résultat est
   souvent un blog ou un site commercial (niveau D). Toujours classifier la source.
2. **Croire qu'une donnée "récente" est forcément correcte.** Un article de blog de
   2026 peut citer des chiffres de 2022. Vérifier la date des DONNÉES, pas de l'article.
3. **Ne pas croiser les sources C/D.** Un article de presse (niveau C) peut contenir
   des erreurs. Toujours vérifier sur une source A/B.
4. **Oublier le `as_of`.** Un chiffre sans date de vérification est un chiffre mort.
5. **Confondre "publié sur un site officiel" et "donnée officielle".** Un blog hébergé
   sur un site gouvernemental n'est pas une source officielle. Vérifier le contexte.
6. **Ignorer les spécificités belges.** Un taux de TVA français ne s'applique pas en
   Belgique. Toujours vérifier sur les sources belges.

## Verification Checklist (pour l'agent)

Après chaque recherche web, l'agent doit pouvoir répondre :
- [ ] Chaque résultat est classifié (A/B/C/D)
- [ ] Les données C/D sont croisées avec source A/B
- [ ] Chaque chiffre a un `as_of` et une source
- [ ] Les données datées sont vérifiées (< 1 an)
- [ ] Le score de confiance est produit
- [ ] Les données non vérifiées sont marquées comme telles

> ⚠️ **Disclaimer** : ce gate est une méthodologie de vérification, pas une garantie
> d'exactitude. Les sources officielles évoluent — vérifier chaque chiffre sur la
> source le jour de l'utilisation. Pour des documents engageants (business plan,
> dossier de subside), faire valider par un expert-comptable ou un avocat agréé
> en Belgique.
