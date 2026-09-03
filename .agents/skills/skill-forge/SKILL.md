---
name: skill-forge
description: "Utilisez quand un agent IA doit créer un nouveau skill ou en étendre un existant dans ce repo (The Agency) — ou dans tout dépôt de skills au format agentskills.io. Produit un SKILL.md conforme aux standards du repo : frontmatter canonique, structure deep, règles de sécurité, gates de validation et test TDD de la vague."
version: 1.0.0
license: MIT
author: The Agency
metadata:
  tags: [meta, contribution, tooling]
  related_skills: [agency-doc-keeper, fact-check-sourcing]
  domain: meta
  language: fr
  as_of: "2026-08"
---

# Skill Forge — forger un skill conforme aux standards du repo

## Overview

Ce meta-skill apprend à un agent IA à **écrire un nouveau skill** (ou en étendre un)
conforme aux standards de ce dépôt : format agentskills.io, frontmatter canonique
harness-agnostic, structure « deep » (pas une checklist superficielle), règles de
sécurité de `SECURITY.md`, et passage des gates obligatoires. Il produit un dossier
`.agents/skills/<nom>/SKILL.md` validé, accompagné de son test TDD, prêt pour un
commit atomique.

Le principe directeur : **un skill est un produit, pas une note**. Il doit être
chargeable par n'importe quel harness (ChatGPT, Claude, Cursor, Gemini…), contenir
un workflow avec critères de complétion vérifiables, et passer tous les gates avant
d'exister dans le repo.

## When to Use

- « Crée un nouveau skill pour <sujet> »
- « Ajoute un skill sur <domaine métier belge> »
- « Étends le skill <nom> avec <section/cas d'usage> »
- « Ce skill ne passe pas le validateur, corrige-le »
- **Ne pas utiliser pour :** la maintenance documentaire après création (compteurs
  README, INDEX.md, CHANGELOG — c'est le rôle de `agency-doc-keeper`), ni la
  rédaction de contenu métier hors format skill.

## Inputs & Sorties

- **Entrées** : le sujet du skill, ses déclencheurs réels (formulations utilisateur),
  son domaine (`rd`, `finance`, `legal`, `marketing`, `meta`…), ses skills liés.
- **Sorties** :
  1. `tests/test_vagueN_tdd.py` — le test TDD écrit **avant** le skill (RED).
  2. `.agents/skills/<nom>/SKILL.md` — le skill lui-même (GREEN).
  3. Exit 0 sur les quatre gates (voir section Gates).

## Workflow

### 1. Cadrer le skill

Définir avant d'écrire une ligne :
- le **déclencheur précis** (une formulation utilisateur réelle, pas « utile pour
  plein de choses ») ;
- l'**artefact produit** (fichier, tableau, checklist — jamais « des conseils ») ;
- les **contre-déclencheurs** (« ne pas utiliser pour… ») ;
- le `domain`, les `tags`, les `related_skills` (qui doivent tous résoudre vers un
  dossier existant).

*Critère de complétion : la `description` tient en une phrase « Utilisez quand X.
Produit Y. » et un non-spécialiste sait quand NE PAS charger le skill.*

### 2. Approche TDD : le test d'abord

Écrire `tests/test_vagueN_tdd.py` dans le style de `tests/test_vague3_tdd.py` :
existence du skill, validateur `validate_skills.validate_skill()`, description
trigger-focused, sections obligatoires, `related_skills` qui résolvent, contenu
métier attendu. Le lancer et **constater l'échec (RED)** avant de créer le skill.

*Critère de complétion : `python tests/test_vagueN_tdd.py` sort en exit 1 avec des
échecs « skill n'existe pas ».*

### 3. Copier le template canonique

Partir de `.agents/skills/_template/SKILL.md`, jamais d'un fichier vide :

```bash
cp .agents/skills/_template/SKILL.md .agents/skills/<nom>/SKILL.md
```

Le `<nom>` est en kebab-case minuscule (`^[a-z0-9]+(-[a-z0-9]+)*$`), identique au
champ `name` du frontmatter.

*Critère de complétion : le dossier `.agents/skills/<nom>/` existe et `name` ==
nom du dossier.*

### 4. Écrire le frontmatter canonique

Champs autorisés en top-level (whitelist stricte) : `name`, `description`,
`version`, `license`, `author`, `compatibility`, `metadata`. Dans `metadata` :
`tags` (liste non vide), `related_skills`, `as_of`, `domain`, `language`.

**Champs INTERDITS** (harness-spécifiques, cassent la promesse agnostic) :
`allowed-tools`, `disallowed-tools`, `hooks`, `model`, `effort`, `context`,
`agent`, `shell`, `disable-model-invocation`, `user-invocable`, `argument-hint`,
`paths`, `mcp`. Le validateur les rejette en erreur.

La `description` doit être **trigger-focused** : commencer par « Utilisez quand… »
(ou « Use when… »), ≤ 1024 caractères.

*Critère de complétion : `python scripts/validate_skills.py` ne remonte aucune
erreur de frontmatter pour le skill.*

### 5. Écrire le corps « deep »

Cible : **6 000 à 15 000 caractères**. En dessous, c'est un shallow skill (à
étoffer) ; au-dessus de 25 000, déplacer le détail lourd (gabarits, grilles,
exemples longs) dans des fichiers `references/` et ne garder que l'essentiel dans
le SKILL.md. Structure :

1. **Overview** — 2-4 phrases : ce que fait le skill, pourquoi il existe, artefact
   concret produit.
2. **When to Use** — déclencheurs en formulations utilisateur réelles + « Ne pas
   utiliser pour : » explicite.
3. **Workflow** — étapes numérotées, chacune avec un *critère de complétion
   vérifiable* en italique. C'est le cœur du skill.
4. **Common Pitfalls** — pièges réels du domaine + comment les éviter.
5. **Verification Checklist** — cases à cocher actionnables.

*Critère de complétion : les 4 sections obligatoires/recommandées sont présentes
et chaque étape du workflow a son critère de complétion.*

### 6. Appliquer les règles de SECURITY.md

- **Zéro donnée réelle** : jamais de vrai numéro BCE/TVA/IBAN/compte, jamais de
  données clients, jamais de chemin machine personnel. Placeholders obligatoires :
  `BE0123.456.789`, `[NOM_CLIENT]`, `<VOTRE_USER>`.
- **Zéro exécution non auditée** : référencer un outil existant, oui ; ne jamais
  écrire d'instruction du type téléchargement pipé dans un shell (c'est interdit).
- **Exactitude réglementaire** : tout chiffre daté (taux, seuil, montant) porte un
  `as_of` + la mention « vérifier le taux en vigueur ».
- **Disclaimer** : obligatoire si et seulement si un tag réglementaire est présent
  (`finance`, `tax`, `legal`, `compliance`, `accounting`, `fiscal`, `social`) —
  bloc « ⚠️ Disclaimer » mentionnant comptable / expert-comptable / avocat agréé.
  Un skill meta comme celui-ci n'en a pas ; ne pas en mettre par réflexe.

*Critère de complétion : `python scripts/security_scan.py` sort en exit 0.*

### 7. Passer les gates obligatoires

Dans l'ordre, tous en exit 0 :

```bash
python tests/test_vagueN_tdd.py          # le test de la vague (GREEN)
python scripts/validate_skills.py        # structure + frontmatter
python scripts/security_scan.py          # anti-leak
python scripts/check_related_links.py    # related_skills qui résolvent
```

*Critère de complétion : les quatre commandes sortent en exit 0.*

### 8. Finaliser

Après le vert : commit atomique (un skill = un commit, ou un lot cohérent par
domaine), puis enchaîner avec `agency-doc-keeper` pour la synchronisation
documentaire (INDEX.md, compteurs README, CHANGELOG).

## Common Pitfalls

1. **Écrire le skill avant le test.** Sans RED constaté, le test ne prouve rien —
   il pourrait passer pour de mauvaises raisons. Toujours lancer le test sur un
   skill inexistant d'abord.
2. **Copier le frontmatter d'un skill trouvé en ligne.** Les exemples externes
   contiennent souvent `allowed-tools` ou `model` (Claude-specific) → rejetés par
   le validateur. Partir du `_template` du repo, point final.
3. **Un skill shallow.** Trois bullets « conseils » ne sont pas un skill. Si le
   workflow n'a pas de critères de complétion vérifiables, il n'est pas fini.
4. **Description générique.** « Skill utile pour la comptabilité » ne déclenchera
   jamais au bon moment. La description est le seul signal de routing du harness —
   elle doit contenir le déclencheur exact.
5. **`related_skills` vers des skills qui n'existent pas encore.** Le vérificateur
   de liens bloque. Créer les dépendances dans la même vague ou retirer le lien.
6. **Disclaimer en trop ou en moins.** La règle est mécanique : tag réglementaire
   → disclaimer obligatoire ; pas de tag réglementaire → pas de disclaimer. Ni
   oubli, ni réflexe.
7. **Données « d'exemple » réalistes.** Un faux numéro BCE plausible est traité
   comme un vrai par le scanner. Utiliser exclusivement les placeholders whitelistés.
8. **Oublier la taille.** Au-delà de ~25 000 caractères le validateur avertit :
   le détail part dans `references/`, le SKILL.md reste le squelette chargé par le
   harness.

## Verification Checklist

- [ ] Le test TDD de la vague existe, a échoué (RED) avant l'écriture, passe (GREEN) après
- [ ] `name` == nom du dossier, kebab-case, regex conforme
- [ ] `description` commence par « Utilisez quand » et nomme l'artefact produit
- [ ] Frontmatter 100 % whitelisté (aucun champ harness-spécifique)
- [ ] `metadata` complète : `tags`, `related_skills`, `domain`, `language`, `as_of`
- [ ] Sections présentes : Overview, When to Use, Workflow, Common Pitfalls, Verification Checklist
- [ ] Chaque étape du workflow a un critère de complétion vérifiable
- [ ] Taille entre 6 000 et 15 000 caractères (détail lourd dans `references/` sinon)
- [ ] Aucune donnée réelle — placeholders `BE0123.456.789` / `[NOM_CLIENT]` / `<VOTRE_USER>` uniquement
- [ ] Disclaimer présent si et seulement si tag réglementaire
- [ ] `python scripts/validate_skills.py` → exit 0
- [ ] `python scripts/security_scan.py` → exit 0
- [ ] `python scripts/check_related_links.py` → exit 0
