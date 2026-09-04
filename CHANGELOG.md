# Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et ce projet adhère au [Versionnage sémantique](https://semver.org/lang/fr/).

## [Non publié]

### Ajouté

- Skill `be-devis-quotes` : chiffrage et suivi des devis belges — tarification
  par phases (TJM/forfait), mentions obligatoires (BCE, TVA, validité, acompte),
  numérotation séquentielle, relances J+7/J+14, passage devis signé → facture Peppol.
- Persona `deviseur-be` : combine devis, vente, facturation Peppol et contrats ;
  prépare des fourchettes argumentées, ne fixe jamais le prix final.
- Tests TDD vague 6 (`test_vague6_tdd.py`, 9 familles) et 3 scénarios d'activation
  pour `be-devis-quotes` (42 scénarios au total).
- CI GitHub Actions (`gates`) : validation des skills, scan anti-leak, vérification
  des liens `related_skills` et exécution de tous les tests sur chaque push et PR.
- Workflow mensuel de fraîcheur (`freshness`) : détecte les skills dont le marqueur
  `as_of` dépasse 6 mois et ouvre une issue de revue réglementaire (sans doublon).
- Templates d'issues GitHub : bug de skill, proposition de nouveau skill,
  signalement de données obsolètes.
- Scripts `build_index`, `freshness_report` et `check_doc_sync`.
- Skills `skill-forge` (forge de nouveaux skills) et `agency-doc-keeper`
  (gardien de la cohérence documentaire).
- Persona `agency-operator` : orchestrateur de la journée du solopreneur,
  enchaînant ops, vente, facturation et contenu.
- Test d'activation automatisé des descriptions de skills.
- Dossier `examples/` d'exemples d'utilisation.
- Skill `activate-agency` : onboarding et personnalisation — interview 8 questions,
  profil persistant `AGENCY_PROFILE.md` (écrit hors du repo, jamais commité),
  shortlist de skills prioritaires, plan 30 jours avec phrase de handoff.
- Tests TDD vague 5 (`test_vague5_tdd.py`, 10 familles) et 3 scénarios d'activation
  pour `activate-agency` (39 scénarios au total).
- `check_doc_sync` détecte désormais les copies harness trackées par git
  (.claude/.cursor/.hermes/.kilocode doivent rester hors du dépôt).

### Modifié

- `fact-check-sourcing` v3.1.0 : section « Adaptation par plateforme » dédupliquée
  (une table au lieu de 4 blocs identiques) et patterns d'intégration condensés —
  même méthodologie, un tiers de moins à lire.

### Corrigé

- Réparation de la distribution harness via les adapters (`link-skills.sh` /
  `link-skills.ps1`).
- Les copies harness (.claude/.cursor/.hermes/.kilocode) sont dé-trackées : le
  README annonçait des liens créés après le clone, mais des copies figées étaient
  encore commitées — source de dérive copie vs canonique.
- Badge CI du README pointé vers le dépôt réel (au lieu du placeholder `<VOTRE_USER>`).

## [0.1.0]

### Ajouté

- 18 skills harness-agnostic pour solopreneurs belges : création d'entreprise
  (BCE, TVA, PP vs SRL), comptabilité, facturation Peppol, business plan,
  étude de marché, subsides, RGPD, contrats, veille concurrentielle et sociale,
  prospection, contenu, secrétariat, deadlines administratives, fact-checking…
- 6 personas métier (`.agents/agents/`) : comptable, stratège R&D, juriste,
  créateur de contenu, veilleur, secrétaire.
- 3 scripts de gates : `validate_skills.py` (validation structurelle),
  `security_scan.py` (scan anti-leak), `check_related_links.py` (liens entre skills).
- Suite de tests TDD : self-tests du validateur et du scanner, tests E2E du
  workflow de contribution, tests de qualité des descriptions.
- Adapters de distribution par symlinks (`.claude`, `.cursor`, `.hermes`, `.kilocode`).
- Documentation : `AGENTS.md`, `SECURITY.md`, `CONTRIBUTING.md`, `MAINTAINERS.md`,
  `DISCLAIMER.md`, `_template/SKILL.md`.
- Licence MIT.
