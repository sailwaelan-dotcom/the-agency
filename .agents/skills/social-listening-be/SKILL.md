---
name: social-listening-be
description: "Utilisez quand le solopreneur belge veut surveiller sa réputation en ligne, suivre des concurrents, ou repérer des sujets de contenu via les réseaux sociaux — en méthodes 100% légales : APIs officielles, alertes, RSS, exports manuels. Jamais de scraping, contournement de CAPTCHA, ou collecte non autorisée."
version: 0.1.0
license: MIT
author: The Agency
metadata:
  tags: [content, intel, be]
  related_skills: [content-engine-be, be-market-research, be-rgpd-compliance]
  domain: content
  language: fr
  as_of: "2026-07"
---

# Veille réseaux sociaux — méthodes légales uniquement (Belgique)

## Overview

Ce skill est un **playbook de veille légale**, pas un outil de scraping. Il répond à :
« comment je sais ce qu'on dit de moi / de mes concurrents / de mon secteur en ligne ? »
en utilisant **exclusivement** des méthodes autorisées : APIs officielles des
plateformes, alertes gratuites, flux RSS publics, exports manuels de tes propres
comptes, et lecture manuelle de pages publiques.

> ⚠️ **Règle absolue** : ce skill ne fournit et n'exécute **aucun** code de scraping,
> aucune technique de contournement (CAPTCHA, proxies, faux comptes), aucune collecte
> de données personnelles non publiques. Toute donnée collectée sur des personnes
> relève du RGPD → voir `be-rgpd-compliance`.

## When to Use

- « Je veux savoir quand on parle de moi / de mon entreprise en ligne »
- « Comment suivre ce que font mes concurrents sur LinkedIn ? »
- « Je cherche des sujets de contenu qui agitent mon secteur »
- « Un client m'a mentionné, je veux être alerté des prochaines fois »

**Ne pas utiliser pour :**
- Extraire des listes de prospects ou des bases d'emails → **interdit** (RGPD + ToS)
- Automatiser des interactions (likes, follows, DMs) → **interdit** (ToS)
- Contourner une restriction technique d'une plateforme → **interdit** (loi + ToS)
- Contenu marketing régulier → `content-engine-be`

## ⛔ Ce qui est strictement interdit (rappel SECURITY.md §4)

| Interdit | Pourquoi |
|---|---|
| Scraping automatisé (bots, crawlers, headless browsers) | Violation des Conditions d'Utilisation de toutes les plateformes ; risque légal (loi belge sur la criminalité informatique, art. 550bis Code pénal) |
| Contournement de CAPTCHA / rate limits / blocages | Contournement de mesure technique de protection — infraction pénale |
| Proxys / rotation d'IP pour masquer l'origine | Indicateur de collecte non autorisée |
| Scraping authentifié (avec session/login) | Violation ToS + accès à données non publiques |
| Faux comptes pour accéder à du contenu restreint | Fraude + violation ToS |
| Collecte de données personnelles sans base légale | Violation RGPD — amende APD possible |
| Stockage de données personnelles collectées dans ce repo | Violation SECURITY.md §2 (zéro donnée réelle) |

## ✅ Ce qui est autorisé et recommandé

### 1. Alertes gratuites (zéro technique)

| Outil | Ce qu'il fait | Coût |
|---|---|---|
| **Google Alerts** (google.com/alerts) | Email quand un mot-clé apparaît sur le web indexé | Gratuit |
| **LinkedIn notifications** | Alertes natives quand on te mentionne ou te suit | Gratuit |
| **Talkwalker Alerts** | Alternative à Google Alerts, couvre blogs/forums | Gratuit |

Mise en place : créer des alertes sur ton nom, ta dénomination, tes concurrents
directs, et 2-3 termes sectoriels clés. *Critère : alertes actives et premier email
reçu.*

### 2. APIs officielles des plateformes

- **LinkedIn API** : lecture de ton propre profil et statistiques (via ton compte,
  avec token OAuth officiel). Utile pour suivre l'engagement sur TES posts.
- **X/Twitter API** : tiers gratuits limités ; recherche de tweets publics dans la
  limite des quotas officiels.
- **Meta Business Suite** : statistiques de tes pages Facebook/Instagram professionnelles.

Règle : utiliser uniquement ton **propre** compte, ton **propre** token, dans les
limites officielles. Jamais de token d'un tiers, jamais de contournement de quota.

### 3. Flux RSS publics

- Blogs sectoriels belges (ajouter le flux RSS à un lecteur : Feedly, Inoreader…)
- Sites d'actualité économique belge (L'Écho, Trends-Tendances, Made In…)
- Blogs concurrents qui en publient un

*Critère : 5-10 flux RSS actifs dans un lecteur, consultés 2×/semaine.*

### 4. Lecture manuelle de pages publiques

- Profils LinkedIn publics de concurrents (ce qu'ils publient, leur cadence, leurs sujets)
- Pages publiques Facebook/Instagram du secteur
- Groupes LinkedIn/Facebook de ton métier en Belgique (observation, pas extraction)

**Manuel** signifie : toi, un navigateur, des notes. Pas d'outil qui automatise la
visite ou l'extraction.

### 5. Exports manuels de tes propres données

- LinkedIn → Paramètres → Obtenir une copie de vos données (export officiel)
- Meta → Télécharger vos informations
- Ces exports concernent TES données, générés par la plateforme à ta demande — légal.

## Workflow : la veille hebdo d'un solopreneur (30 min)

| Jour | Action | Durée |
|---|---|---|
| Lundi | Lire les alertes Google/Talkwalker reçues la semaine passée ; noter les mentions pertinentes | 10 min |
| Mercredi | Consulter les flux RSS sectoriels ; marquer 2-3 sujets réutilisables en contenu | 10 min |
| Vendredi | Tour des profils concurrents (manuel) : qu'ont-ils publié ? Quel engagement ? | 10 min |

**Sortie** : un tableau de veille simple (date | source | sujet | action à prendre :
répondre, créer du contenu, ignorer) — alimente directement `content-engine-be`.

## RGPD et veille (rappel essentiel)

- Observer des **pages publiques d'entreprises** : pas de RGPD applicable (pas de
  données personnelles).
- Relever le nom d'une **personne** qui te mentionne publiquement : traitement de
  données personnelles → base légale requise (intérêt légitime de gestion de
  réputation, documenté) → voir `be-rgpd-compliance`.
- **Ne jamais** constituer de fichier de prospects à partir de profils sociaux
  extraits — c'est de la collecte non autorisée, sanctionnable par l'APD.

## Common Pitfalls

1. **Confondre « public » et « libre de droits ».** Une page publique reste protégée
   par les ToS de la plateforme et par le RGPD pour les données personnelles.
2. **Utiliser un « petit scraper juste pour moi ».** La taille ne change rien à la
   légalité : le scraping automatisé viole les ToS, point.
3. **Surveiller sans but.** La veille sans action (répondre, adapter, créer) est du
   temps perdu — chaque item de veille doit déboucher sur une décision.
4. **Négliger les alertes gratuites.** Google Alerts couvre 80 % du besoin d'un
   solopreneur, sans technique et sans risque.
5. **Observer sans jamais interagir.** Répondre à une mention (merci, précision,
   correction) vaut plus que 100 items de veille passive.

## Verification Checklist

- [ ] Google Alerts actives (nom, dénomination, concurrents, secteur)
- [ ] 5-10 flux RSS dans un lecteur, consultés régulièrement
- [ ] Rituel hebdo de veille bloqué dans l'agenda (30 min)
- [ ] Tableau de veille tenu (date | source | sujet | action)
- [ ] Aucune méthode interdite utilisée (scraping, proxies, faux comptes)
- [ ] Traitement de données personnelles documenté si applicable (→ be-rgpd-compliance)

> ⚠️ **Disclaimer** : information générale (as_of 2026-07). La légalité des méthodes
> de collecte en ligne évolue (jurisprudence, ToS des plateformes). Pour toute collecte
> systématique ou tout doute, consultez un avocat spécialisé en droit des nouvelles
> technologies ou en protection des données en Belgique.
