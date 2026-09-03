# Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et ce projet adhère au [Versionnage sémantique](https://semver.org/lang/fr/).

## [Non publié]

### Ajouté

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

### Corrigé

- Réparation de la distribution harness via les adapters (`link-skills.sh` /
  `link-skills.ps1`).

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
