---
name: be-company-setup
description: "Utilisez quand le futur solopreneur belge doit choisir sa forme juridique (personne physique vs SRL), créer son entreprise (inscription BCE, guichet d'entreprises, acte notarié, activation TVA, caisse d'assurances sociales), ou accomplir les démarches post-création (compte pro, assurances, premier outil de facturation)."
version: 0.1.0
license: MIT
author: The Agency
metadata:
  tags: [legal, admin, compliance, company, be]
  related_skills: [be-accounting-basics, be-business-plan, be-invoicing-peppol]
  domain: admin
  language: fr
  as_of: "2026-07"
---

# Création d'entreprise en Belgique (solopreneur)

## Overview

Créer son activité en Belgique suit un chemin précis : **choisir la forme juridique**,
s'**inscrire à la Banque-Carrefour des Entreprises (BCE)** via un guichet d'entreprises
agréé, **activer le numéro TVA**, s'**affilier à une caisse d'assurances sociales**,
puis ouvrir un compte professionnel. Pour une SRL, s'ajoutent : plan financier,
acte constitutif devant notaire, apport, publication au Moniteur belge.

Ce skill produit : (1) une décision documentée PP vs SRL, (2) la séquence d'actes dans
le bon ordre avec les points de blocage classiques, (3) une checklist post-création.
Il ne remplace ni notaire ni expert-comptable — il prépare les rendez-vous avec eux.

## When to Use

- « Je veux me lancer indépendant en Belgique, par où je commence ? »
- « Personne physique ou SRL pour mon activité ? »
- « Je viens d'avoir mon numéro BCE, c'est quoi la suite ? »
- « C'est quoi un guichet d'entreprises / une caisse d'assurances sociales ? »

**Ne pas utiliser pour :**
- Questions TVA courantes (déclarations, régimes) → `be-accounting-basics`
- Business plan et étude de marché → `be-business-plan`, `be-market-research`
- Facturation au quotidien → `be-invoicing-peppol`

## Décision : personne physique ou SRL ?

| Critère | Personne physique (entreprise individuelle) | SRL |
|---|---|---|
| **Responsabilité** | Illimitée (patrimoine perso engagé) | Limitée à l'apport (sauf faute) |
| **Coût de création** | Faible (guichet + caisse sociale) | Plus élevé (notaire, plan financier, publication) — *ordre de grandeur à vérifier auprès d'un notaire* |
| **Fiscalité** | IPP progressif sur tout le bénéfice | ISOC sur la société (+ précompte mobilier sur dividendes) — optimisation possible à partir d'un certain bénéfice |
| **Capital minimum** | Aucun | Aucun minimum légal, mais **plan financier obligatoire** et apport suffisant exigé par le CSA |
| **Formalités** | Simples | Statuts, acte notarié, Moniteur, compte au nom de la société |
| **Image / crédibilité** | Correcte pour démarrer | Souvent perçue comme plus établie (B2B, marchés publics) |
| **Sortie / revente** | Difficile | Parts cessibles |

Règle de pouce : activité à faible risque et CA modeste → PP pour démarrer vite et pas
cher. Risque juridique réel, bénéfice visé élevé, ou besoin d'image B2B → SRL. La
conversion PP→SRL est possible plus tard mais coûteuse ; si le doute est fort, se faire
conseiller **avant** l'inscription.

## Workflow

### 1. Trancher la forme juridique

Appliquer le tableau ci-dessus à la situation réelle (risque, CA visé, patrimoine,
associés éventuels). *Critère de complétion* : décision écrite en 3 lignes avec la
justification — elle servira au notaire ou au guichet.

### 2. Préparer l'identité de l'entreprise

- Dénomination commerciale (vérifier qu'elle n'entre pas en conflit évident avec des
  entreprises existantes — recherche BCE publique)
- Objet social / activités (codes NACE-Bel) : ni trop étroit (bloque les évolutions)
  ni abusivement large
- Adresse de siège (règles d'urbanisme communales parfois applicables pour certains commerces)

*Critère de complétion* : nom + liste de codes NACE + adresse prêts à communiquer.

### 3. Inscription

**Personne physique :**
1. Guichet d'entreprises agréé → inscription BCE → numéro d'entreprise (format `BE0xxx.xxx.xxx`)
2. Activation TVA au guichet TVA (via le même guichet d'entreprises, souvent) → numéro TVA actif
3. Affiliation à une caisse d'assurances sociales (obligatoire **avant** le début d'activité)
4. Compte bancaire professionnel dédié

**SRL (ajouts) :**
1. **Plan financier** signé par le(s) fondateur(s) — document obligatoire conservé par le notaire
2. **Apport** : en numéraire (compte bloqué chez une banque, attestation) ou **en nature**
   (rapport d'un réviseur d'entreprises obligatoire — voir `be-business-plan` pour l'évaluation)
3. **Acte constitutif** devant notaire + publication au Moniteur belge
4. Inscription BCE + activation TVA + caisse sociale du dirigeant (statut indépendant)
5. Compte bancaire au nom de la société

*Critère de complétion* : numéro BCE obtenu, numéro TVA **activé** (pas seulement demandé),
attestation d'affiliation sociale reçue.

### 4. Post-création (avant la 1re facture)

- [ ] Outil de facturation conforme (Peppol-ready) → `be-invoicing-peppol`
- [ ] Assurances : RC exploitation selon activité ; autres selon secteur (obligatoires
      dans certaines professions réglementées — vérifier)
- [ ] Provision impôt + cotisations sur compte épargne dédié → `be-accounting-basics`
- [ ] Choix du comptable (ou logiciel si autogestion PP simple)
- [ ] Mentions légales du site web + registre RGPD si collecte de données → `be-rgpd-compliance`

*Critère de complétion* : chaque case cochée ou datée dans l'agenda.

## Références belges

- **BCE / KBO** (kbopub.economie.fgov.be) : registre public, recherche d'entreprises
- **Guichets d'entreprises agréés** : liste officielle sur le site du SPF Économie
- **SPF Finances** (finances.belgium.be) : activation TVA, guichets TVA
- **INASTI** (rsvz-inasti.fgov.be) : affiliation sociale indépendants
- **Code des sociétés et des associations (CSA)** : règles SRL (apport, plan financier)
- **Notariat** (notaire.be) : acte constitutif SRL, tarifs indicatifs
- Données datées : **as_of 2026-07** — vérifier montants et procédures en vigueur.

## Common Pitfalls

1. **Facturer avant l'activation TVA.** Le numéro BCE ne suffit pas : l'activation TVA
   prend parfois des jours. Aucune facture légale sans elle.
2. **Oublier la caisse d'assurances sociales** avant le démarrage. L'affiliation est
   obligatoire dès le premier jour d'activité ; des rappels de cotisations avec
   majorations sont possibles.
3. **Objet social trop étroit (SRL).** Modifier l'objet ensuite = acte notarié payant.
   Rédiger large (mais honnête) dès le départ.
4. **Apport en nature sans réviseur.** Tout apport en nature en SRL exige le rapport
   d'un réviseur d'entreprises ; sans lui, l'apport est contestable.
5. **Mélanger perso et pro.** Compte dédié dès le jour 1 — pour la SRL c'est impératif,
   pour la PP c'est la condition d'une comptabilité saine.
6. **Croire que la SRL protège de tout.** La responsabilité limitée ne couvre pas les
   fautes de gestion, les garanties personnelles signées, ni les dettes sociales/fiscales
   dans certains cas de faute.

## Verification Checklist

- [ ] Forme juridique choisie et justifiée par écrit
- [ ] Numéro BCE obtenu
- [ ] Numéro TVA activé (vérifié dans le registre public TVA)
- [ ] Attestation caisse d'assurances sociales
- [ ] Compte pro séparé ouvert
- [ ] SRL : plan financier signé, acte passé, publication Moniteur vérifiée
- [ ] Outil de facturation Peppol-ready configuré
- [ ] RC exploitation souscrite si applicable

> ⚠️ **Disclaimer** : information générale (as_of 2026-07), pas un conseil juridique,
> fiscal ou comptable personnalisé. Le choix de la forme juridique engage durablement :
> faites valider par un notaire, un avocat ou un expert-comptable agréé en Belgique
> avant l'inscription.
