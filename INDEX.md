# Index des skills — The Agency

> Généré par scripts/build_index.py — ne pas éditer à la main.
> Généré le 2026-09-04 — 22 skills.

## admin

| Skill | Déclencheur | as_of | Skills liés |
|---|---|---|---|
| [be-admin-deadlines](.agents/skills/be-admin-deadlines/SKILL.md) | Utilisez quand le solopreneur belge veut un calendrier fiscal annuel complet (TVA, INASTI, IPP/ISOC, BNB, listings), vé… | 2026-07 | be-accounting-basics, be-bookkeeping-ops, be-company-setup |
| [be-company-setup](.agents/skills/be-company-setup/SKILL.md) | Utilisez quand le futur solopreneur belge doit choisir sa forme juridique (personne physique vs SRL), créer son entrepr… | 2026-07 | be-accounting-basics, be-business-plan, be-invoicing-peppol |
| [be-rgpd-compliance](.agents/skills/be-rgpd-compliance/SKILL.md) | Utilisez quand le solopreneur belge collecte des données personnelles (formulaire de contact, newsletter, clients), doi… | 2026-07 | be-company-setup, secretary-ops, social-listening-be |

## content

| Skill | Déclencheur | as_of | Skills liés |
|---|---|---|---|
| [brand-voice-solopreneur](.agents/skills/brand-voice-solopreneur/SKILL.md) | Utilisez quand le solopreneur belge doit définir ou appliquer son ton d'écriture (site, LinkedIn, emails, devis) : char… | 2026-07 | content-engine-be, be-market-research |
| [content-engine-be](.agents/skills/content-engine-be/SKILL.md) | Utilisez quand le solopreneur belge doit produire du contenu régulièrement (LinkedIn, blog, newsletter) sans y passer s… | 2026-07 | brand-voice-solopreneur, be-market-research, social-listening-be |
| [social-listening-be](.agents/skills/social-listening-be/SKILL.md) | Utilisez quand le solopreneur belge veut surveiller sa réputation en ligne, suivre des concurrents, ou repérer des suje… | 2026-07 | content-engine-be, be-market-research, be-rgpd-compliance |

## finance

| Skill | Déclencheur | as_of | Skills liés |
|---|---|---|---|
| [be-accounting-basics](.agents/skills/be-accounting-basics/SKILL.md) | Utilisez quand le solopreneur belge pose une question TVA (régime normal/franchise/forfait, déclarations, délais), impô… | 2026-07 | be-invoicing-peppol, be-bookkeeping-ops |
| [be-bookkeeping-ops](.agents/skills/be-bookkeeping-ops/SKILL.md) | Utilisez quand le solopreneur belge doit organiser sa comptabilité courante : rituel mensuel de collecte des pièces, ra… | 2026-07 | be-accounting-basics, be-invoicing-peppol |
| [be-financial-modeling](.agents/skills/be-financial-modeling/SKILL.md) | Utilisez quand le solopreneur belge doit modéliser un projet d'investissement, calculer une valorisation (DCF, multiple… | 2026-07 | be-business-plan, be-market-research, be-funding-subsidies, fact-check-sourcing |
| [be-invoicing-peppol](.agents/skills/be-invoicing-peppol/SKILL.md) | Utilisez quand le solopreneur doit émettre une facture B2B en Belgique (Peppol obligatoire depuis janvier 2026), choisi… | 2026-07 | be-accounting-basics, be-bookkeeping-ops |

## legal

| Skill | Déclencheur | as_of | Skills liés |
|---|---|---|---|
| [be-contracts-legal](.agents/skills/be-contracts-legal/SKILL.md) | Utilisez quand le solopreneur belge doit rédiger ou vérifier un contrat (prestation, partenariat, NDA), des conditions… | 2026-07 | be-rgpd-compliance, be-company-setup, be-sales-outreach |

## meta

| Skill | Déclencheur | as_of | Skills liés |
|---|---|---|---|
| [activate-agency](.agents/skills/activate-agency/SKILL.md) | Utilisez quand un solopreneur installe The Agency pour la première fois, lance « activate the agency », demande « par o… | 2026-09 | be-company-setup, be-admin-deadlines, fact-check-sourcing |
| [agency-doc-keeper](.agents/skills/agency-doc-keeper/SKILL.md) | Utilisez quand le repo The Agency a changé — ajout, modification ou suppression d'un skill, changement de scripts ou de… | 2026-08 | skill-forge, fact-check-sourcing |
| [skill-forge](.agents/skills/skill-forge/SKILL.md) | Utilisez quand un agent IA doit créer un nouveau skill ou en étendre un existant dans ce repo (The Agency) — ou dans to… | 2026-08 | agency-doc-keeper, fact-check-sourcing |

## ops

| Skill | Déclencheur | as_of | Skills liés |
|---|---|---|---|
| [secretary-ops](.agents/skills/secretary-ops/SKILL.md) | Utilisez quand le solopreneur belge croule sous l'administratif quotidien : tri des emails, gestion d'agenda, préparati… | 2026-07 | be-bookkeeping-ops, be-rgpd-compliance, content-engine-be |

## rd

| Skill | Déclencheur | as_of | Skills liés |
|---|---|---|---|
| [be-business-plan](.agents/skills/be-business-plan/SKILL.md) | Utilisez quand le solopreneur belge doit rédiger un business plan (banque, subside, notaire pour SRL), construire son p… | 2026-07 | be-market-research, be-funding-subsidies, be-company-setup, be-accounting-basics |
| [be-competitor-watch](.agents/skills/be-competitor-watch/SKILL.md) | Utilisez quand le solopreneur belge veut cartographier ses concurrents directs (3-8 acteurs), surveiller leurs mouvemen… | 2026-07 | be-market-research, social-listening-be, content-engine-be |
| [be-funding-subsidies](.agents/skills/be-funding-subsidies/SKILL.md) | Utilisez quand le solopreneur belge cherche un financement non-dilutif (subside, prime, prêt d'honneur, microcrédit), v… | 2026-07 | be-business-plan, be-market-research, be-company-setup |
| [be-market-research](.agents/skills/be-market-research/SKILL.md) | Utilisez quand le solopreneur belge doit valider une idée (étude de marché), dimensionner son marché (TAM/SAM/SOM), ana… | 2026-07 | be-business-plan, be-funding-subsidies |
| [fact-check-sourcing](.agents/skills/fact-check-sourcing/SKILL.md) | Utilisez automatiquement après chaque recherche web ou extraction de données — GATE ACTIF harness-agnostic (ChatGPT, Mi… | 2026-07 | be-market-research, be-business-plan, be-funding-subsidies, content-engine-be, be-financial-modeling |

## sales

| Skill | Déclencheur | as_of | Skills liés |
|---|---|---|---|
| [be-devis-quotes](.agents/skills/be-devis-quotes/SKILL.md) | Utilisez quand le solopreneur belge doit chiffrer et envoyer un devis : tarification (TJM, forfait, par phase), structu… | 2026-09 | be-sales-outreach, be-invoicing-peppol, be-contracts-legal |
| [be-sales-outreach](.agents/skills/be-sales-outreach/SKILL.md) | Utilisez quand le solopreneur belge doit structurer sa prospection B2B : cold outreach (email, LinkedIn), qualification… | 2026-07 | be-market-research, be-competitor-watch, content-engine-be, brand-voice-solopreneur |
