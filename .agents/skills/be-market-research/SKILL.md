---
name: be-market-research
description: "Utilisez quand le solopreneur belge doit valider une idée (étude de marché), dimensionner son marché (TAM/SAM/SOM), analyser la concurrence locale, ou interviewer des clients potentiels avant de construire. Produit des données sourcées prêtes pour le business plan."
version: 0.1.0
license: MIT
author: The Agency
metadata:
  tags: [business, rd, strategy, market, be]
  related_skills: [be-business-plan, be-funding-subsidies]
  domain: rd
  language: fr
  as_of: "2026-07"
---

# Étude de marché belge (solopreneur)

## Overview

Avant tout business plan, il faut des données réelles : combien de clients potentiels
en Belgique, que paient-ils aujourd'hui, qui sert déjà ce marché, et est-ce que le
problème fait assez mal pour payer. Ce skill combine le **dimensionnement top-down**
(TAM/SAM/SOM à partir de sources publiques belges) et la **validation bottom-up**
(interviews clients, méthode Mom Test). Il produit un dossier de marché sourcé,
directement injectable dans `be-business-plan`.

## When to Use

- « Mon idée tient la route ? Il y a un marché en Belgique ? »
- « Je dois chiffrer mon marché pour la banque / le notaire / un subside »
- « Qui sont mes concurrents en Belgique et que facturent-ils ? »
- « Comment je parle à des clients potentiels sans qu'ils me mentent poliment ? »

**Ne pas utiliser pour :**
- Rédiger le business plan complet → `be-business-plan`
- Trouver des subsides → `be-funding-subsidies`
- Veille continue sur les réseaux → `social-listening-be`

## Sources publiques belges (lecture seule)

| Source | Ce qu'on y trouve |
|---|---|
| **Statbel** (statbel.fgov.be) | Démographie, ménages, revenus, emploi par secteur/région |
| **SPF Économie** | Statistiques d'entreprises par code NACE, créations/défaillances |
| **BCE / KBO Open Data** (kbopub.economie.fgov.be) | Nombre d'entreprises actives par secteur et province |
| **BNB — Centrale des bilans** | Comptes annuels des sociétés concurrentes (CA, effectifs) |
| **Organismes sectoriels** | Chiffres de filière (ex: INAMI pour la santé, Febelfin, Agoria) |
| **Eurostat** | Comparaisons BE vs EU, données harmonisées |

Règle : **toute donnée citée porte source + année**. Une estimation sans source est
marquée « estimation — à valider » et n'entre jamais dans un dossier officiel telle quelle.

## Dimensionnement TAM / SAM / SOM

1. **TAM** (marché total) : population × taux d'équipement/besoin × dépense moyenne.
   Exemple de méthode : Statbel donne le nombre de ménages belges ; un rapport
   sectoriel donne le % qui achète la catégorie ; le prix moyen boucle le calcul.
2. **SAM** (marché adressable) : filtrer par géographie (région/province), segment
   (B2B/B2C, taille), et canal (en ligne, présentiel).
3. **SOM** (part obtenable) : ce qu'un solo peut réalistement servir en 3 ans —
   capacité (heures vendables, débit de production) × taux de pénétration prudent
   (0,5-2 % du SAM est déjà ambitieux pour un inconnu).

*Critère de complétion* : les trois chiffres tiennent en un tableau avec leurs
hypothèses écrites à côté. Le SOM est exprimé en **clients/an**, pas en € seulement.

## Analyse concurrentielle

Grille minimale par concurrent (3-8 acteurs) :

| Concurrent | Offre | Prix public | Cible | Forces | Faiblesses exploitables |
|---|---|---|---|---|---|

- Prix : pages tarifaires publiques, devis anonymisés, avis clients mentionnant le prix.
- Comptes annuels (BNB) pour les sociétés : tendance de croissance, rentabilité.
- Ce qu'**aucun** concurrent ne fait : c'est ton angle de différenciation — le noter
  explicitement, il nourrit le positionnement et le business plan.

## Validation terrain : interviews (Mom Test)

Règles d'or pour 10-20 entretiens avant de construire :
1. Parler du **passé vécu**, jamais du futur hypothétique (« la dernière fois que
   vous avez eu ce problème, qu'avez-vous fait ? » — pas « est-ce que vous paieriez
   pour… ? »).
2. Chercher des **faits** (combien dépensé, temps perdu, solutions bricolées), pas des
   compliments.
3. Signaux forts : le client a déjà payé/bricolé une solution, demande le prix,
   propose un essai. Signaux faibles : « super idée ! », « tiens-moi au courant ».
4. Noter verbatim les mots exacts utilisés pour décrire le problème — ils deviennent
   le copywriting de `content-engine-be`.

*Critère de complétion* : ≥ 10 entretiens documentés, chacun avec : segment, problème
vécu, coût actuel du problème, signal fort/faible.

## Workflow

1. **Définir le segment précis** (qui paie, qui utilise, où en Belgique).
   *Critère : le segment tient en une phrase falsifiable.*
2. **Collecter top-down** : 3-5 sources publiques, extraire les chiffres clés avec liens.
   *Critère : TAM/SAM/SOM calculés avec hypothèses visibles.*
3. **Cartographier les concurrents** : grille remplie, prix réels notés.
   *Critère : au moins 3 concurrents, au moins 1 faiblesse exploitable par concurrent.*
4. **Interviewer** : 10-20 conversations Mom Test.
   *Critère : synthèse des signaux — combien de signaux forts sur combien d'entretiens.*
5. **Trancher** : GO (signaux forts ≥ 30-40 % des entretiens + SOM ≥ objectif année 1),
   PIVOT (problème réel mais segment/solution à ajuster), STOP (problème tiède, marché
   trop petit). *Critère : décision écrite et justifiée en 5 lignes.*

## Common Pitfalls

1. **Confondre TAM et SOM.** « Le marché mondial vaut des milliards » ne dit rien sur
   ce qu'un solo belge peut capter. Seul le SOM en clients/an compte pour l'année 1.
2. **Interviewer en demandant la permission.** « Tu achèterais ? » → toujours oui,
   jamais suivi d'acte. Le Mom Test existe précisément pour ça.
3. **Chercher des chiffres qui confirment.** Biaiser l'étude tue le business plan qui
   la suit : noter aussi les données qui contredisent l'idée.
4. **Ignorer les alternatives non-concurrentes.** Le vrai concurrent est souvent
   « Excel + WhatsApp + ne rien faire », pas une autre startup.
5. **Recruter ses interviews dans son cercle.** Famille et amis mentent par affection ;
   viser des inconnus du segment (groupes métiers, salons, LinkedIn).
6. **S'arrêter aux chiffres.** Sans entretiens terrain, l'étude reste théorique :
   la banque et toi-même avez besoin des deux jambes (top-down + bottom-up).

## Verification Checklist

- [ ] Segment défini en une phrase falsifiable
- [ ] TAM/SAM/SOM chiffrés avec sources + années citées
- [ ] ≥ 3 concurrents avec prix réels et faiblesses
- [ ] ≥ 10 entretiens Mom Test documentés avec signaux
- [ ] Décision GO/PIVOT/STOP écrite et justifiée
- [ ] Dossier exportable tel quel dans le business plan

> ⚠️ **Disclaimer** : méthodologie générale (as_of 2026-07). Les données publiques
> évoluent — vérifier chaque chiffre sur la source officielle avant de l'inscrire dans
> un document engageant (business plan, dossier de subside).
