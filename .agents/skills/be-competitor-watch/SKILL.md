---
name: be-competitor-watch
description: "Utilisez quand le solopreneur belge veut cartographier ses concurrents directs (3-8 acteurs), surveiller leurs mouvements (prix, offres, recrutement, contenu), ou préparer un dossier de différenciation. Produit une grille concurrentielle vivante alimentée par des méthodes 100% légales."
version: 0.1.0
license: MIT
author: The Agency
metadata:
  tags: [business, rd, strategy, intel, be]
  related_skills: [be-market-research, social-listening-be, content-engine-be]
  domain: rd
  language: fr
  as_of: "2026-07"
---

# Veille concurrentielle structurée — solopreneur belge

## Overview

Ce skill va au-delà de `social-listening-be` (surveillance large) : il produit une
**grille concurrentielle vivante** de 3-8 concurrents directs, alimentée par des
méthodes 100% légales (pages publiques, comptes annuels, avis clients, annonces
d'emploi). La grille est un outil de décision stratégique : quoi différencier, où
attaquer, quand réagir. Elle nourrit directement `be-business-plan` (positionnement),
`be-market-research` (analyse de marché) et `content-engine-be` (sujets de contenu).

## When to Use

- « Qui sont mes 3-5 concurrents directs en Belgique ? »
- « Qu'est-ce que mes concurrents facturent ? »
- « Comment me différencier de [concurrent X] ? »
- « Mon concurrent vient de lancer [produit], je fais quoi ? »
- « Je prépare un business plan — il me faut l'analyse concurrentielle »

**Ne pas utiliser pour :**
- Surveillance large du secteur (veille réputation, tendances) → `social-listening-be`
- Étude de marché complète (TAM/SAM/SOM) → `be-market-research`
- Contenu régulier → `content-engine-be`

## Méthodes 100% légales (rappel SECURITY.md §4)

| Source | Ce qu'on y trouve | Comment |
|---|---|---|
| **Pages publiques** (site web, pricing) | Offre, prix, positionnement, cible | Lecture manuelle, copie dans la grille |
| **LinkedIn entreprise** | Effectifs, croissance, recrutement, contenu | Page publique, lecture manuelle |
| **Comptes annuels BNB** | CA, résultat, effectifs, tendance sur 3 ans | Recherche publique par numéro BCE |
| **Avis clients** (Google, Trustpilot, sectoriels) | Forces/faiblesses perçues, verbatims | Lecture manuelle, extraction des thèmes |
| **Annonces d'emploi** | Stratégie (recrute = croît, quel poste = quel axe) | Lecture manuelle sur LinkedIn/Indeed |
| **Google Alerts** | Mentions web (communiqués, presse) | Alimente `social-listening-be` |

**Interdit** : scraping automatisé, contournement de restrictions, collecte de données
personnelles. Voir `social-listening-be` pour le détail des méthodes autorisées.

## Grille concurrentielle (modèle)

Remplir pour **3 à 8 concurrents** directs (pas les acteurs lointains) :

| Critère | Concurrent 1 | Concurrent 2 | Concurrent 3 |
|---|---|---|---|
| **Nom** | | | |
| **Site web** | | | |
| **Numéro BCE** | | | |
| **Offre principale** | | | |
| **Cible** | | | |
| **Prix public** (ou fourchette) | | | |
| **Effectifs** (LinkedIn) | | | |
| **CA dernier exercice** (BNB) | | | |
| **Tendance CA** (3 ans) | | | |
| **Forces perçues** (avis clients) | | | |
| **Faiblesses exploitables** | | | |
| **Contenu** (LinkedIn, blog) | | | |
| **Recrutement en cours** | | | |
| **Dernier mouvement notable** | | | |

### Ce qu'on cherche dans la grille

- **Faiblesse exploitable** : ce que le concurrent fait mal ou ne fait pas → ton angle d'attaque
- **Tendance** : croissance = concurrent sérieux, déclin = opportunité
- **Prix** : fourchette réelle (pas toujours publiée — devis anonymes, avis clients)
- **Effectifs** : entreprise solo ou équipe ? Impact sur la capacité et le positionnement
- **Contenu** : quel canal utilise-t-il ? Quel ton ? Où est le vide ?

## Sources publiques belges

| Source | URL | Ce qu'on y trouve |
|---|---|---|
| **BCE / KBO** | kbopub.economie.fgov.be | Numéro BCE, date création, code NACE, situation |
| **BNB — Centrale des bilans** | recherchefirme.nbb.be | Comptes annuels (CA, résultat, effectifs) |
| **Google** | google.com | Site web, avis, communiqués |
| **LinkedIn** | linkedin.com | Effectifs, recrutement, contenu |
| **Avis Google** | google.com/maps | Notes, verbatims clients |
| **Trustpilot / sectoriels** | trustpilot.com | Avis détaillés |

## Workflow

1. **Identifier les 3-8 concurrents directs** : ceux qui servent le même segment, dans
   la même zone géographique, avec une offre similaire. *Critère : la liste est courte
   (< 10) et chaque concurrent est un vrai concurrent (un client hésite entre vous).*

2. **Remplir la grille** : une session de 2-3h pour les données initiales.
   *Critère : chaque cellule remplie ou marquée « non trouvable » — pas de cases vides
   non expliquées.*

3. **Identifier les angles** : pour chaque concurrent, noter au moins 1 faiblesse
   exploitable. *Critère : 3+ angles de différenciation identifiés au total.*

4. **Surveiller** (rituel mensuel, 30 min) : vérifier les mouvements récents (nouveau
   produit, recrutement, changement de prix). *Critère : la colonne « dernier mouvement
   notable » est mise à jour.*

5. **Alimenter** : chaque insight de la grille nourrit un autre outil :
   - Faiblesse exploitable → `be-business-plan` (positionnement)
   - Verbatims clients → `content-engine-be` (sujets de contenu)
   - Prix observé → `be-business-plan` (pricing)
   - Mouvement notable → `social-listening-be` (veille)

## Common Pitfalls

1. **Trop de concurrents.** 8 maximum — au-delà, la grille devient ingérable et la
   surveillance impossible. Choisir les plus proches.
2. **Confondre concurrent direct et indirect.** Un logiciel généraliste n'est pas un
   concurrent direct d'un outil spécialisé. Garder la grille focalisée.
3. **Ne jamais mettre à jour.** La grille est un outil vivant — sans rituel mensuel,
   elle devient obsolète en 3 mois.
4. **Scraper pour remplir la grille.** Toutes les données sont publiques et accessibles
   manuellement. Le scraping est interdit et inutile ici.
5. **Copier le concurrent.** La grille sert à se différencier, pas à imiter. Chaque
   faiblesse identifiée = une opportunité de positionnement distinct.
6. **Ignorer les avis clients.** Les verbatims dans les avis Google/Trustpilot sont
   la meilleure source de différenciation — les clients disent ce qu'ils veulent.

## Verification Checklist

- [ ] 3-8 concurrents directs identifiés (même segment, même zone)
- [ ] Grille remplie (chaque cellule ou « non trouvable » documenté)
- [ ] 3+ angles de différenciation identifiés
- [ ] Rituel mensuel de mise à jour (30 min) dans l'agenda
- [ ] Insights alimentent business-plan, content-engine et social-listening

> ⚠️ **Disclaimer** : information générale (as_of 2026-07). Les données publiques
> (comptes annuels, avis) évoluent — vérifier chaque chiffre sur la source officielle
> avant de l'inscrire dans un document engageant (business plan, dossier de subside).
