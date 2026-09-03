---
name: activate-agency
description: "Utilisez quand un solopreneur installe The Agency pour la première fois, lance « activate the agency », demande « par où commencer ? » ou « quels skills sont faits pour moi ? », ou veut personnaliser l'agence pour son activité. Conduit l'interview d'onboarding (stade, forme juridique, TVA, objectifs), écrit le profil persistant AGENCY_PROFILE.md hors du repo, puis produit la shortlist des skills prioritaires et le plan 30 jours avec handoff."
version: 1.0.0
license: MIT
author: The Agency
metadata:
  tags: [meta, onboarding, configuration, profil, be]
  related_skills: [be-company-setup, be-admin-deadlines, fact-check-sourcing]
  domain: meta
  language: fr
  as_of: "2026-09"
---

# Activate the Agency — onboarding et personnalisation

## Overview

C'est le **premier skill à charger après l'installation** de The Agency. En une
session de 5-10 minutes, il transforme une boîte à outils générique en agence
personnalisée : une interview courte, un profil persistant, une shortlist de
skills prioritaires et un plan des 30 premiers jours qui se termine par un
handoff concret vers le premier skill à lancer.

Le skill ne remplace aucun skill métier : il configure l'agence pour que chaque
skill démarre chaud, sans re-poser les mêmes questions de contexte à chaque fois.

## When to Use

- « Je viens d'installer The Agency, par où commencer ? »
- « Activate the agency » / « Personnalise l'agence pour mon activité »
- « Quels skills sont faits pour moi ? »
- « Mon profil a changé — nouveau CA, passage en SRL, nouvel objectif — mets à jour »

**Ne pas utiliser pour :**
- Exécuter un skill métier déjà identifié → charger directement le skill
  (`be-invoicing-peppol`, `secretary-ops`, …)
- Recherches de fond sur un marché → `be-market-research`
- Produire un chiffre réglementaire pendant l'onboarding → skill spécialisé
  (chaque chiffre porte son `as_of` et son disclaimer à la maison)

## Inputs & Sorties

- **Entrées** : réponses à l'interview (8 questions, voir Workflow) ou contexte
  déjà fourni par l'utilisateur — dans ce cas, proposer le profil prérempli à
  corriger plutôt que re-poser tout.
- **Sorties** (trois artefacts) :
  1. `AGENCY_PROFILE.md` — le profil persistant, écrit dans le **dossier de
     travail du solopreneur**, hors du repo The Agency ;
  2. une **shortlist** de 3 à 5 skills prioritaires, chacun justifié en une ligne ;
  3. un **plan 30 jours** adapté au stade, terminé par une phrase de handoff
     prête à copier.

## Le profil AGENCY_PROFILE.md

**Règle absolue** : le profil contient des données réelles (statut, CA,
objectifs). Les données réelles ne vont **jamais dans le repo** The Agency
(règle n°1 du dépôt). Le profil vit dans le dossier de travail du solopreneur,
hors du repo, et n'est **jamais commité** dans ce dépôt. Si l'utilisateur veut
le versionner, il le fait dans SON dépôt, pas ici.

Format fixe (les sections sont stables pour rester lisibles par les autres
skills et par une future re-activation) :

```markdown
# AGENCY_PROFILE — [prénom] (ne jamais committer ce fichier dans The Agency)

## Vous
- Langue de travail : FR | NL | EN
- Région : Bruxelles | Flandre | Wallonie

## Entreprise
- Stade : idée | lancement | établi
- Forme juridique : personne physique | SRL | à choisir
- Régime TVA : franchise | normal | forfait | à confirmer
- Secteur d'activité + clientèle : … (B2B / B2C / mixte)
- CA estimé : …
- Année de démarrage : …
- Numéro BCE : … (optionnel)

## Outils & réseau
- Comptable : oui | non | à chercher
- Logiciel facturation / Peppol : …
- Caisse d'assurances sociales : …

## Objectifs 90 jours
1. … (mesurable)
2. …

## Journal
- 2026-09-03 — activation v1.0.0 — profil initial
```

Chaque champ non renseigné porte la mention « à confirmer » (avec le comptable
le cas échéant) — jamais un chiffre inventé.

## Workflow

### 1. Détecter un profil existant

Chercher `AGENCY_PROFILE.md` dans le dossier de travail courant. S'il existe →
passer directement en **mode mise à jour** (étape 6). Sinon, onboarding complet.

*Critère de complétion* : le mode (création / mise à jour) est annoncé à
l'utilisateur avant toute question.

### 2. Conduire l'interview — une seule salve de 8 questions

Poser les 8 questions **en une fois**, avec options fermées et une échappatoire
« à confirmer » sur chaque ligne. C'est un onboarding produit, pas un interrogatoire.

1. **Stade** : idée / lancement / établi ?
2. **Forme juridique** : personne physique / SRL / à choisir ? — si « à choisir »,
   le premier chantier sera `be-company-setup`.
3. **Régime TVA** : franchise / normal / forfait / à confirmer ?
4. **Secteur + clientèle** : quoi, pour qui (B2B → Peppol devient prioritaire) ?
5. **Région + langue** : Bruxelles / Flandre / Wallonie ; FR / NL / EN ?
6. **CA estimé + année de démarrage** : les deux paramètres comptables de base.
7. **Entourage** : comptable (oui / non / à chercher) ? logiciel de facturation ?
   caisse d'assurances sociales ?
8. **Objectifs 90 jours** : 1 à 3 objectifs mesurables (« signer 3 clients B2B »,
   pas « développer mon business »).

*Critère de complétion* : les 8 questions sont notées ou explicitement marquées
« à confirmer ». Aucun champ laissé vide en silence.

### 3. Rédiger le profil et le faire valider

Écrire `AGENCY_PROFILE.md` (format ci-dessus) dans le dossier de travail, puis
l'afficher en entier. Demander la correction section par section.

*Critère de complétion* : chaque section a été vue et validée par l'utilisateur ;
le Journal porte sa première ligne datée (activation, version du skill).

### 4. Produire la shortlist (3 à 5 skills, pas plus)

Croiser stade + objectifs + entourage pour choisir **3 à 5 skills prioritaires**.
Pour chacun, une ligne « pourquoi toi » reliée à une réponse de l'interview —
pas une description générique du skill.

Points de départ par stade (à ajuster selon les objectifs) :

| Stade | Shortlist type |
|---|---|
| Idée | `be-market-research`, `be-business-plan`, `be-company-setup`, `be-funding-subsidies` |
| Lancement | `be-company-setup`, `be-invoicing-peppol`, `be-accounting-basics`, `be-admin-deadlines` |
| Établi | `be-admin-deadlines`, `be-bookkeeping-ops`, `be-sales-outreach`, `content-engine-be` |

Croisements transversaux : B2B → `be-invoicing-peppol` monte d'un cran ;
objectif notoriété → `content-engine-be` / `social-listening-be` ;
`fact-check-sourcing` reste le gate actif sur toute donnée externe.

*Critère de complétion* : shortlist entre 3 et 5 skills, chaque skill suivi de
sa justification personnalisée. Une liste de 10 skills est un échec.

### 5. Plan 30 jours + handoff

Construire le plan à partir de la shortlist, en 4 semaines :

- **Semaine 1 — fondations admin** : statut/régime en règle, échéances connues
  (souvent via `be-admin-deadlines` ou `be-company-setup` selon le stade).
- **Semaine 2 — revenu** : premier chantier qui rapproche de l'argent
  (devis, prospection `be-sales-outreach`, offres).
- **Semaine 3 — visibilité** : contenu ou veille selon l'objectif 90 jours.
- **Semaine 4 — bilan + rituels** : ce qui a tenu, ce qu'on installe en récurrent.

Terminer **obligatoirement** par le handoff — une phrase prête à copier qui
nomme le premier skill et son point d'appui :

> Dis : « Lance `be-admin-deadlines` avec mon AGENCY_PROFILE.md »

(adapte le skill au plan ; la phrase est copiée telle quelle pour démarrer chaud).

*Critère de complétion* : le plan 30 jours est affiché ET la phrase de handoff
figure dans la réponse finale. Une activation sans handoff est une activation
incomplète.

### 6. Mode mise à jour (profil existant)

Afficher le profil actuel **section par section**, demander « quoi a changé ? »,
patcher uniquement les champs concernés, ajouter une ligne au Journal (date,
version, nature du changement). **Jamais de réécriture silencieuse** : le
solopreneur doit voir exactement ce qui change avant que ce soit écrit.

*Critère de complétion* : les modifications sont montrées (avant/après) et
validées ; le Journal est à jour. Enchaîner sur un rafraîchissement de la
shortlist si le stade ou les objectifs ont bougé.

## Common Pitfalls

1. **Écrire le profil dans le repo cloné.** Données réelles dans un dépôt
   public = la violation n°1 de SECURITY.md. Le profil vit dans le dossier de
   travail du solopreneur, jamais dans The Agency.
2. **Poser 8 questions ouvertes d'affilée.** Personne ne répond à « parlez-moi
   de vous ». Options fermées + « à confirmer », salve unique, 5 minutes.
3. **Confondre shortlist et catalogue.** 10 skills « prioritaires » = zéro
   priorité. Max 5, chacun justifié par une réponse d'interview.
4. **Réécrire le profil existant sans demander.** Le Journal et les nuances
   (« à confirmer depuis mars ») sont de l'information. Mode mise à jour =
   patch visible, pas remplacement.
5. **Chiffrer pendant l'onboarding.** « Tu seras à 21 % de TVA » n'a pas sa
   place ici : le profil note « à confirmer » et le skill spécialisé (avec son
   `as_of` et son disclaimer) tranche plus tard.
6. **Oublier le handoff.** Sans phrase prête à copier, l'activation se termine
   sur « ok, et maintenant ? » — le silence tue les onboardings.
7. **Calquer le profil type sur l'utilisateur précédent.** Pas d'hypothèse par
   défaut (consultant PP bruxellois francophone) : les réponses pilotent, pas
   l'intuition de l'agent.

## Verification Checklist

- [ ] `AGENCY_PROFILE.md` créé dans le dossier de travail, hors du repo, jamais commité ici
- [ ] Les 8 questions notées, inconnus marqués « à confirmer » (rien de vide en silence)
- [ ] Chaque section du profil validée par l'utilisateur
- [ ] Journal : ligne datée (activation ou mise à jour)
- [ ] Shortlist de 3 à 5 skills, un « pourquoi toi » par skill
- [ ] Plan 30 jours adapté au stade et aux objectifs
- [ ] Phrase de handoff prête à copier dans la réponse finale
- [ ] Aucune donnée réelle écrite dans le repo The Agency

> ⚠️ **Disclaimer** : ce skill configure l'agence, il ne conseille pas. Les
> renvois réglementaires (forme juridique, TVA) sont de l'information générale —
> les skills spécialisés portent leur `as_of` et leur disclaimer, et toute
> décision engageante se valide avec un professionnel agréé en Belgique.
