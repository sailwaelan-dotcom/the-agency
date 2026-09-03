---
name: agency-doc-keeper
description: "Utilisez quand le repo The Agency a changé — ajout, modification ou suppression d'un skill, changement de scripts ou de tests, ou avant une release. Produit une documentation resynchronisée : INDEX.md et catalog.json régénérés, compteurs README à jour, CHANGELOG complété, as_of revus, gates au vert."
version: 1.0.0
license: MIT
author: The Agency
metadata:
  tags: [meta, documentation, maintenance]
  related_skills: [skill-forge, fact-check-sourcing]
  domain: meta
  language: fr
  as_of: "2026-08"
---

# Agency Doc Keeper — maintenance documentaire du repo

## Overview

Ce skill maintient la **cohérence documentaire** du dépôt The Agency après chaque
changement de contenu : catalogue (`INDEX.md`, `catalog.json`), compteurs du
README (nombre de skills, liens, tests), `CHANGELOG.md`, et fraîcheur réglementaire
des `as_of`. Il produit un repo dont la documentation reflète exactement l'état
réel des skills — vérifiable par des gates automatiques, pas par relecture.

Le principe directeur : **la doc est du code**. Elle se régénère, se vérifie par
des scripts, et ne s'édite jamais à la main quand un générateur existe.

## When to Use

- « Je viens d'ajouter / modifier / supprimer un skill »
- « Les scripts ou les tests ont changé, la doc doit suivre »
- « On prépare une release, vérifie que tout est synchro »
- « Les compteurs du README ont l'air faux »
- « Certains `as_of` datent, fais le point de fraîcheur »
- **Ne pas utiliser pour :** la création d'un skill (c'est `skill-forge`), ni la
  vérification factuelle de données externes (c'est `fact-check-sourcing`).

## Inputs & Sorties

- **Entrées** : un repo modifié (skills, scripts ou tests) avec un état git propre
  ou des changements en cours identifiés.
- **Sorties** : `INDEX.md` + `catalog.json` régénérés, compteurs README
  resynchronisés, `CHANGELOG.md` complété, rapport de fraîcheur des `as_of`,
  quatre gates en exit 0.

## Workflow

### 1. Lancer les gates de structure

Avant toute mise à jour documentaire, s'assurer que le contenu lui-même est sain :

```bash
python scripts/validate_skills.py
python scripts/security_scan.py
python scripts/check_related_links.py
python tests/test_vagueN_tdd.py   # le test TDD de la vague en cours, s'il existe
```

*Critère de complétion : les quatre commandes sortent en exit 0. Si l'une échoue,
corriger le contenu d'abord — jamais documenter un état cassé.*

### 2. Régénérer le catalogue

Le catalogue est **généré**, jamais édité à la main :

```bash
python scripts/build_index.py
```

Cela régénère `INDEX.md` (catalogue lisible des skills, groupés par domaine) et
`catalog.json` (export machine-readable : noms, descriptions, tags, domaines,
`as_of`). Les deux fichiers doivent être régénérés ensemble — l'un sans l'autre
est un état incohérent.

*Critère de complétion : `INDEX.md` et `catalog.json` reflètent exactement les
dossiers présents dans `.agents/skills/` (hors `_template`).*

### 3. Resynchroniser les compteurs du README

Mettre à jour dans `README.md` les chiffres dérivés du contenu réel :
- nombre de skills (« N skills ») ;
- statut de validation (« N/N skills valides ») ;
- nombre de liens `related_skills` (« N liens ») ;
- compteurs de tests (nombre de fichiers/cas de test).

Puis vérifier la synchro au lieu de la croire :

```bash
python scripts/check_doc_sync.py
```

Ce script recompte depuis la source de vérité (dossiers skills, sortie du
validateur, tests) et compare aux chiffres affichés dans la documentation
(README, tests/ACTIVATION.md). Exit 0 = synchro ; exit 1 = liste des écarts.

*Critère de complétion : `python scripts/check_doc_sync.py` sort en exit 0.*

### 4. Mettre à jour CHANGELOG.md

Format [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/), en français :
section `## [Non publié]` en tête, entrées classées (`Ajouté`, `Modifié`,
`Corrigé`, `Supprimé`), une ligne par changement visible du contributeur. À une
release, transformer `Non publié` en `## [X.Y.Z] - AAAA-MM-JJ`.

*Critère de complétion : chaque changement de la session a une entrée, datée le
jour de la release le cas échéant.*

### 5. Vérifier la fraîcheur réglementaire

Les `as_of` vieillissent ; un skill fiscal avec un `as_of` de plus de 6 mois est
suspect. Mesurer avant de corriger :

```bash
python scripts/freshness_report.py --fail-after-months 6
```

Le rapport liste les skills dont l'`as_of` dépasse le seuil (exit 1 si au moins un
dépasse). Pour chaque skill signalé : **revoir les sources officielles** du domaine
(SPF Finances, INASTI, VLAIO, Awex…), vérifier que chaque chiffre est toujours en
vigueur, et **alors seulement** bumper l'`as_of` au mois de la revue. Utiliser
`fact-check-sourcing` pour le croisement des sources.

*Critère de complétion : chaque `as_of` bumpé correspond à une revue réelle
tracée (source consultée + date), et le rapport repasse sous le seuil.*

### 6. Checklist finale avant commit

Rejouer tous les gates une dernière fois sur l'état final, puis laisser le commit
atomique à l'utilisateur (un lot cohérent : skill(s) + doc synchronisée).

*Critère de complétion : gates en exit 0 sur l'état final, documentation et
contenu modifiés dans le même lot.*

## Common Pitfalls

1. **Chiffres qui divergent entre README, ACTIVATION.md et la réalité.** C'est le
   symptôme classique d'une mise à jour manuelle oubliée. Toujours terminer par
   `check_doc_sync.py` — il recompte depuis la source de vérité.
2. **Éditer INDEX.md à la main.** Le fichier est régénéré par `build_index.py` :
   toute édition manuelle est écrasée à la prochaine génération. Corriger la
   source (le SKILL.md), pas le catalogue.
3. **Bumper un `as_of` sans revue réelle.** Un `as_of` frais sur un chiffre mort
   est pire qu'un `as_of` ancien honnête : il ment avec confiance. Pas de bump
   sans source officielle consultée à la date du bump.
4. **Régénérer INDEX.md mais oublier catalog.json** (ou l'inverse). Les deux sont
   produits par la même commande ; ne jamais en committer un seul.
5. **Documenter un état cassé.** Mettre à jour les compteurs pendant que le
   validateur échoue fige l'erreur dans la doc. Gates d'abord, doc ensuite.
6. **Oublier le CHANGELOG.** « Je le ferai à la release » ne survit jamais.
   L'entrée s'écrit au moment du changement, dans `Non publié`.
7. **Compter `_template` comme un skill.** Les compteurs excluent les dossiers
   commençant par `_` — vérifier que les scripts et la doc appliquent la même règle.

## Verification Checklist

- [ ] `python scripts/validate_skills.py` → exit 0 (N/N skills valides)
- [ ] `python scripts/security_scan.py` → exit 0
- [ ] `python scripts/check_related_links.py` → exit 0
- [ ] Le test TDD de la vague concernée → exit 0
- [ ] `INDEX.md` et `catalog.json` régénérés ensemble via `build_index.py`
- [ ] Compteurs README (skills, validés, liens, tests) à jour et confirmés par `check_doc_sync.py` → exit 0
- [ ] `CHANGELOG.md` : chaque changement a son entrée Keep a Changelog en français
- [ ] `freshness_report.py --fail-after-months 6` → exit 0, ou `as_of` bumpés après revue réelle des sources
- [ ] Aucun fichier généré édité à la main
