# Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et ce projet adhère au [Versionnage sémantique](https://semver.org/lang/fr/).

## [Non publié]

### Corrigé

- `scripts/build_exe.py` reconfigure stdout/stderr en UTF-8 avant d'imprimer :
  le build de `TheAgency.exe` plantait (`UnicodeEncodeError`) sur toute console
  cp1252 — runner GitHub Actions Windows inclus — d'où une release v1.0.0
  publiée sans binaires.

### Modifié

- CI `build-exe.yml` : `PYTHONIOENCODING=utf-8` au niveau du job, permissions
  `contents: write`, et attachement automatique de `TheAgency.exe` et
  `TheAgency-Setup.exe` à la GitHub Release lors d'un push de tag.

## [1.0.0] — 2026-09-05

### Ajouté

- **Onboarding Zéro-Friction & Exécutable Windows Autonome (`TheAgency.exe`)** :
  - **Exécutable Windows autonome (`TheAgency.exe`)** : Binaire autonome PyInstaller (10 Mo) intégrant l'environnement d'exécution, le moteur BCE/KBO, le simulateur INASTI et le générateur Peppol UBL sans nécessiter Python sur le poste client.
  - **Menu interactif Solopreneur (`agency/menu.py`)** : TUI console guidée (6 modules métier) avec gestion automatique de l'encodage UTF-8 sous console Windows (`CP1252`), exécutable directement au double-clic via `Lancer_The_Agency.cmd`.
  - **Installateur auto-configurant multi-harness (`install.py`, `install.ps1`, `install.sh`)** : Détection automatique des installations Claude Desktop (Windows `%APPDATA%/Claude`, macOS, Linux), Cursor et Claude Code, avec injection et fusion non destructrice du serveur MCP `agency-be-mcp`.
  - **Assistant d'installation Windows classique (`installer.iss`)** : Script de compilation Inno Setup générant `TheAgency-Setup.exe` avec raccourci sur le Bureau et désinstallateur.
  - **CI de compilation Windows (`.github/workflows/build-exe.yml`)** : Workflow GitHub Actions automatisant le packaging binaire et la création de releases avec artefacts téléchargeables.
  - **Tests unitaires dédiés (`tests/test_installer.py`)** : Validation de la génération de configuration MCP (mode développement et mode gelé), de la résolution des chemins applicatifs, de la préservation des serveurs tiers existants, du routage CLI `mcp` et de la TUI console (18 tests).

- **Architecture Enterprise 2.0 (Améliorations Finales 6 à 10)** :
  - **Micro-moteur SQLite KBO / BCE Hors-Ligne** : Module `kbo_db.py`, script d'indexation `build_bce_index.py` et outil MCP `search_bce_by_name` permettant la recherche instantanée (< 1 ms) d'entreprises belges sans quota ni dépendance réseau.
  - **Watchdog de Dérive Réglementaire** : Script d'audit `scripts/regulatory_monitor.py` et workflow GitHub Actions `.github/workflows/regulatory-monitor.yml` surveillant automatiquement les seuils légaux du dépôt contre les sources officielles du Moniteur Belge et SPF Finances.
  - **Context Engineering à Deux Niveaux & Prompt-Caching** : Script `scripts/build_lite_catalog.py` générant `catalog_lite.json` (~2 300 tokens), outil MCP `load_skill_context` pour chargement on-demand (Tier 2), et guide d'optimisation de cache de préfixe (`.agents/CONTEXT_OPTIMIZATION.md`).
  - **Vault RGPD & Mémoire Épistémique Locale** : Module `agency/vault.py` et outils MCP (`vault_save_client`, `vault_get_client`, `vault_list_clients`, `vault_delete_client`) isolés hors-dépôt (`~/.agency/vault/`) avec conformité stricte APD / droit à l'oubli.
  - **CLI Solopreneur Zéro-Config** : Package exécutable `python -m agency` avec commandes dédiées `bce` (Modulo 97 + KBO), `inasti` (simulation cotisations trimestrielles), `deadlines` (calendrier fiscal dynamique), `check-client` (audit 3-en-1 BCE/VIES/Peppol) et `vault`.

- **Architecture Enterprise 2.0 (Top 5 Améliorations Critiques)** :
  - **Spécification MCP 2024-11-05 complète** : Ajout des endpoints `resources/list`, `resources/read`, `prompts/list`, et `prompts/get`. Fournit 3 URIs métier belges (`belgian-tax://2026/rates`, `inasti://2026/brackets`, `cir92://deductibility/rules`) et 2 templates de prompts guidés (`audit_client_peppol`, `prepare_quarterly_tax_closing`).
  - **Moteur Peppol BIS 3.0 UBL 2.1 XML natif** : Générateur pur Python (`generate_peppol_ubl`) conforme EN 16931 et validateur Schematron/mathématique (`validate_peppol_ubl`) garantissant la conformité fiscale Peppol obligatoire en Belgique.
  - **Execution Guardrails & Policy Interceptor** : Intercepteur pré-vol (validation Modulo 97 stricte sur BCE/TVA, blocage des numéros invalides) et assainisseur post-vol (masquage NISS/registre national, anonymisation des chemins locaux utilisateur `C:\Users\...`).
  - **Protocole A2A (Agent-to-Agent) & Schémas stricts** : Spécifications JSON Schema v1 (`quote_draft`, `contract_terms`, `invoice_event`) et machine à états documentée (`.agents/workflows/a2a_pipeline.md`) pour une collaboration inter-agents typée et auditable sans dérive de contexte.
  - **Suite d'évaluation EDD (Eval-Driven Development)** : 40 scénarios belges dorés (`evals/dataset/belgian_golden_evals.json`) couvrant TVA, INASTI, Peppol, RGPD, déductibilité CIR 92, statuts de société et contrats, avec runner automatisé (`evals/eval_runner.py`) certifiant exactitude factuelle, citations juridiques et zéro hallucination.

- **Couche MCP & APIs belges (`agency-be-mcp`)** :
  - Serveur Model Context Protocol standardisé (JSON-RPC 2.0 stdio, zéro dépendance tierce) pour assister les agents IA en temps réel.
  - Outils déterministes belges : `validate_bce_number` (Modulo 97 officiel SPF Economie), `get_be_tax_calendar` (calendrier dynamique TVA Intervat, VA1-VA4 SPF Finances, INASTI avec alertes J-14/J-3), `calc_inasti_provision` (barèmes et tranches légales INASTI).
  - Connexions APIs officielles : `check_vat_vies` (API REST VIES de la Commission Européenne), `lookup_peppol_participant` (OpenPeppol Directory API).
  - Configurations prêtes à l'emploi pour Claude Code, Cursor, Hermes et Kilocode (`mcp/configs/`).
  - Suite de tests TDD complète (`tests/test_mcp_integration.py`, 18 tests unitaires).
  - Intégration dans les personas (`comptable-be`, `secretaire-be`, `juriste-be`, `agency-operator`) et skills (`be-invoicing-peppol`, `be-admin-deadlines`, `be-accounting-basics`).
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

- `launcher.py` délègue tout le routage au CLI (`agency.cli`) : menu interactif
  sans argument, sous-commandes métier, et nouvelle route `mcp` (serveur stdio)
  empruntée par la configuration MCP de l'exe gelé.
- `agency/bootstrap.py` centralise l'initialisation (UTF-8 console Windows,
  résolution des bundles PyInstaller, `sys.path`) partagée par `cli.py`,
  `menu.py`, `launcher.py` et `install.py` — plus de blocs dupliqués.
- L'option [7] du menu (raccourci Bureau) délègue à `install.create_desktop_shortcut`
  (une seule implémentation, correcte en mode gelé et en mode développement).
- `TheAgency.spec` (artefact PyInstaller régénéré à chaque build local) est
  ignoré par git ; le build de référence reste `scripts/build_exe.py`.
- `fact-check-sourcing` v3.1.0 : section « Adaptation par plateforme » dédupliquée
  (une table au lieu de 4 blocs identiques) et patterns d'intégration condensés —
  même méthodologie, un tiers de moins à lire.

### Corrigé

- Les suites TDD « par vagues » (`test_vague3/4/5_tdd.py`) sont exécutables
  sous pytest comme en direct : familles paramétrées par skill via le helper
  partagé `tests/tdd_common.py` (import pytest gardé — le CI n'installe pas
  pytest), et `check()` lève désormais une `AssertionError` au lieu
  d'accumuler silencieusement (un échec silencieux aurait été un faux vert
  sous pytest). 42 items pytest, plus aucun faux positif.
- **Mode exe gelé (`TheAgency.exe`) fonctionnel de bout en bout** : la config MCP
  générée depuis l'exe référence désormais la route `mcp` de l'exe lui-même
  (au lieu d'un chemin `server.py` dans le dossier temporaire `_MEIPASS` détruit
  à la sortie) ; les configs Cursor / Claude Code sont écrites à côté de l'exe ;
  le raccourci Bureau cible l'exe réel.
- L'option [4] du menu (facture Peppol UBL) lit les bonnes clés retournées par
  `generate_peppol_ubl_xml` — elle plantait systématiquement (`KeyError`) — et
  écrit le XML dans le répertoire courant de l'utilisateur, jamais dans le
  dossier temporaire du bundle.
- `Lancer_The_Agency.cmd` : expansion retardée de `ERRORLEVEL` — la détection
  `py` en repli de `python` fonctionnait mal (message « Python n'est pas
  installé » même quand `py` existait).
- `install.ps1` utilise l'interpréteur détecté (`python` ou `py`) au lieu de
  hardcoder `python`.
- `install.py` : le statut `[✓ Activé] / [✗ Échec]` de la liaison des skills
  reflète le code de retour réel des adaptateurs (échec silencieux supprimé).
- `scripts/build_exe.py` : sortie immédiate (`sys.exit(1)`) hors Windows ;
  `adapters/` embarqué dans le bundle ; chemins `--add-data` relatifs.
- Saisies numériques du menu protégées (`prompt_float` : virgule française
  acceptée, re-saisie en cas d'erreur, refus des négatifs).
- Mentions `as_of` et disclaimers comptables ajoutés aux sorties INASTI,
  échéancier fiscal et facture Peppol du menu ; « CALCUL LÉGAL » renommé
  « SIMULATION » (information générale, pas un conseil personnalisé).
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
