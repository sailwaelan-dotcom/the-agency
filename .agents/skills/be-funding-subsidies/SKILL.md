---
name: be-funding-subsidies
description: "Utilisez quand le solopreneur belge cherche un financement non-dilutif (subside, prime, prêt d'honneur, microcrédit), veut savoir à quel guichet s'adresser selon sa région (VLAIO, SPW/Awex, Innoviris/hub.brussels), ou prépare un dossier de subside. Produit une cartographie des guichets pertinents + checklist d'éligibilité."
version: 0.1.0
license: MIT
author: The Agency
metadata:
  tags: [business, finance, rd, funding, be]
  related_skills: [be-business-plan, be-market-research, be-company-setup]
  domain: rd
  language: fr
  as_of: "2026-07"
---

# Subsides & financements non-dilutifs en Belgique

## Overview

La Belgique est un labyrinthe de guichets publics — **les aides sont régionales** avant
tout : VLAIO (Flandre), SPW/Awex (Wallonie), hub.brussels/Innoviris (Bruxelles).
S'ajoutent les acteurs fédéraux et privés (microStart, Réseau Entreprendre, BeAngels,
prêts d'honneur). Ce skill produit une **cartographie des guichets pertinents** pour
ton profil + une checklist d'éligibilité réaliste. Règle absolue : **aucun montant ni
barème figé ici** — ils changent chaque année ; le skill pointe vers les sources
officielles à vérifier au jour du dépôt.

## When to Use

- « Y a-t-il des subsides pour mon projet en Belgique ? »
- « Je suis en Wallonie/Bruxelles/Flandre, à quel guichet je m'adresse ? »
- « Microcrédit, prêt d'honneur, subside — c'est quoi la différence ? »
- « Je prépare un dossier VLAIO / Awex / hub.brussels »

**Ne pas utiliser pour :**
- Le business plan qui accompagne le dossier → `be-business-plan`
- L'étude de marché requise par la plupart des dossiers → `be-market-research`
- Le financement bancaire classique ou la levée de fonds dilutive (hors périmètre)

## Cartographie des guichets (par région)

### Flandre
- **VLAIO** (vlaio.be) : subventions innovation, conseils, chèques-entreprise,
  aides à la transformation digitale. Guichet central des entreprises flamandes.
- **PMV** : financements complémentaires (prêts, garanties, participations).

### Wallonie
- **SPW Économie / Awex** (awex.be, spw.wallonie.be) : primes à la création,
  aides à l'investissement, chèques-entreprises, accompagnement export.
- **Sowalfin** : prêts et garanties pour PME wallonnes, dont premiers financements.

### Bruxelles
- **hub.brussels** : guichet unique bruxellois — accompagnement gratuit, information
  sur toutes les primes régionales.
- **Innoviris** (innoviris.brussels) : subventions R&D et innovation pour projets
  bruxellois (appels à projets thématiques).
- **finance&invest.brussels** : prêts et participations.

### Fédéral & transversal
- **SPF Économie / SPF Finances** : incitants fiscaux (pas des subsides directs mais
  impact réel : déduction pour investissement, dispense partielle de précompte
  pour chercheurs, statut de jeune entreprise innovante).
- **Tremplin Indépendants** (via ONEM) : démarrer en conservant temporairement ses
  allocations de chômage — vérifier les conditions actuelles auprès du syndicat/ONEM.

### Privé & hybride
- **microStart** : microcrédit + accompagnement pour indépendants sans accès bancaire.
- **Réseau Entreprendre** : prêt d'honneur (sans garantie personnelle bancaire) +
  mentorat, remboursable mais non-dilutif.
- **BeAngels / réseaux de business angels** : dilutif — hors périmètre de ce skill,
  mais à connaître pour la suite.
- **Plan Airbag et équivalents régionaux** : accompagnement à la reprise après échec.

## Types d'aide — ce que chacun implique

| Type | Remboursable ? | Dilutif ? | Effort dossier | Quand pertinent |
|---|---|---|---|---|
| Subside / prime | Non (sous conditions) | Non | Élevé (dossier + suivi) | Projet avec impact régional/innovation |
| Prêt d'honneur | Oui | Non | Moyen | Compléter un apport insuffisant |
| Microcrédit | Oui | Non | Moyen | Exclusion bancaire, petits montants |
| Garantie publique | — (garantit un crédit bancaire) | Non | Faible | Banque frileuse, profil correct |
| Incitant fiscal | Non | Non | Faible (via comptable) | Automatique si conditions remplies |
| Tremplin chômage | Non | Non | Faible | Démarrage depuis le chômage |

## Workflow

1. **Localiser le siège d'exploitation** — la région du siège détermine le guichet
   principal, pas la région d'habitation. *Critère : guichet régional unique identifié.*
2. **Qualifier le projet** : création vs développement, innovation ou non, secteur,
   montant recherché, calendrier. *Critère : fiche projet d'une page prête (réutiliser
   la sortie de `be-business-plan`).*
3. **Shortlister 2-3 guichets** avec le tableau ci-dessus + sites officiels.
   *Critère : pour chaque guichet retenu — nom du programme, éligibilité vérifiée sur
   le site officiel, prochaine date de dépôt (beaucoup fonctionnent par appels).*
4. **Vérifier l'éligibilité AVANT de rédiger** : certains programmes exigent
   l'inscription AVANT la création, d'autres une ancienneté minimale, d'autres un
   cofinancement propre. Rater ce critère = dossier refusé d'office.
   *Critère : checklist d'éligibilité du programme cochée point par point.*
5. **Monter le dossier** : business plan + plan financier + lettre de motivation
   calibrée sur les critères du programme (impact régional, emploi, innovation).
   Faire relire par l'accompagnateur gratuit du guichet (hub.brussels, 1819,
   maisons de l'entreprise) avant dépôt. *Critère : accusé de dépôt + date de réponse
   notée dans l'agenda.*
6. **Après l'octroi** : respecter les obligations (reporting, justification des
   dépenses, maintien de l'activité X années) — un subside non justifié se rembourse.

## Références belges

- **vlaio.be** · **awex.be** · **hub.brussels** · **innoviris.brussels** ·
  **sowalfin.be** · **pmv.eu** · **microstart.be** · **reseau-entreprendre.be**
- **1819.brussels / 1890.be / guichets d'entreprises** : orientation gratuite initiale
- Données datées : **as_of 2026-07**. Chaque montant, barème, taux et date d'appel
  DOIT être vérifié sur le site officiel du guichet au jour du dépôt.

## Common Pitfalls

1. **Déposer avant d'être créé (ou l'inverse).** La plupart des aides ont une fenêtre
   d'éligibilité stricte (avant création, dans les X mois après, ancienneté min.).
   Vérifier ce critère en premier, avant toute rédaction.
2. **Croire qu'un subside remplace l'apport.** Presque tous exigent un cofinancement
   propre (souvent 25-50 %). Le subside complète, ne fonde pas.
3. **Rédiger le dossier seul.** Les accompagnateurs gratuits des guichets connaissent
   les critères réels de sélection — une relecture par eux multiplie les chances.
4. **Compter le subside dans la trésorerie année 1.** Les délais d'instruction +
   paiement par tranches post-dépenses : le cash arrive tard, souvent après 6-18 mois.
5. **Oublier les obligations post-octroi.** Reporting annuel, maintien d'activité,
   justification : le non-respect déclenche le remboursement.
6. **Postuler partout à la fois.** Certains programmes sont incompatibles entre eux
   (double financement public interdit sur les mêmes dépenses). Déclarer les autres
   demandes dans chaque dossier.

## Verification Checklist

- [ ] Guichet régional principal identifié (selon siège d'exploitation)
- [ ] Fiche projet 1 page réutilisable prête
- [ ] 2-3 programmes shortlistés avec éligibilité vérifiée sur site officiel
- [ ] Fenêtre d'éligibilité confirmée (avant/après création, ancienneté)
- [ ] Cofinancement propre disponible et documenté
- [ ] Dossier relu par un accompagnateur du guichet avant dépôt
- [ ] Obligations post-octroi lues et calées dans l'agenda

> ⚠️ **Disclaimer** : information générale (as_of 2026-07), pas un conseil fiscal,
> comptable ou juridique personnalisé. Les programmes, montants et critères changent
> chaque année et par appel — vérifiez systématiquement sur le site officiel du guichet
> et faites valider votre dossier par un expert-comptable ou un avocat agréé en Belgique
> avant dépôt.
