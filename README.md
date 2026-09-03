# The Agency 🇧🇪

![gates](https://github.com/<VOTRE_USER>/the-agency/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

> Boîte à outils de **skills et d'agents IA harness-agnostic** pour solopreneurs en Belgique.
> R&D, finance, admin, contenu, veille, secrétariat — tout ce qui mange le temps d'un indépendant,
> packagé en skills profonds, audités, et portables sur n'importe quel agent (Claude Code, Cursor,
> Hermes, Kilocode, Codex, …).

## Pourquoi ce repo

Un solopreneur belge passe un tiers de son temps sur l'administratif : TVA, INASTI, factures,
relances, veille, contenu. Ce repo transforme ce temps perdu en **workflows d'agent** :
des fichiers `SKILL.md` profonds (pas des prompts jetables), écrits une fois, utilisables
partout, sans dépendance à un outil propriétaire.

- **Harness-agnostic** : format [agentskills.io](https://agentskills.io/specification),
  frontmatter minimal portable, zéro clé spécifique à un éditeur.
- **Belgique d'abord** : BCE, TVA, INASTI, Peppol (obligatoire B2B depuis 2026), RGPD/APD,
  subsides VLAIO/Innoviris/SPW — avec marqueurs `as_of` et disclaimers.
- **Sécurité by design** : `scripts/security_scan.py` bloque secrets, chemins machine,
  injection de prompt, exfiltration. Zéro téléchargement exécuté. Voir [SECURITY.md](SECURITY.md).
- **Fraîcheur surveillée** : une CI mensuelle vérifie l'âge de chaque donnée réglementaire
  (`as_of`) et ouvre une issue quand un skill dépasse 6 mois sans revue.

📖 **[INDEX.md](INDEX.md)** — le catalogue complet des skills · 🎬 **[examples/](examples/)** — une journée de solopreneur orchestrée par l'agent

## Structure

```
The agency/
├── AGENTS.md                  # Instructions pour tout agent qui entre ici
├── SECURITY.md                # Règles non négociables (leaks, scraping, disclaimers)
├── INDEX.md                   # Catalogue des skills (généré — ne pas éditer à la main)
├── catalog.json               # Le même catalogue, machine-readable
├── .agents/
│   ├── skills/                # ← les skills (canonique)
│   │   ├── _template/         #   squelette à copier pour contribuer
│   │   ├── be-business-plan/
│   │   └── …
│   └── agents/                # personas métier (dont `agency-operator`, l'orchestrateur)
├── adapters/
│   ├── link-skills.sh         # symlinks vers .claude/.cursor/.hermes/.kilocode
│   └── link-skills.ps1        # junctions Windows (sans droits admin)
├── scripts/
│   ├── validate_skills.py     # validation structurelle (frontmatter, sections, disclaimer)
│   ├── security_scan.py       # scan anti-leak (secrets, chemins, injection, exfiltration)
│   ├── check_related_links.py # vérifie que tous les related_skills résolvent
│   ├── build_index.py         # régénère INDEX.md + catalog.json (--check pour la CI)
│   ├── freshness_report.py    # rapport de fraîcheur réglementaire des as_of
│   └── check_doc_sync.py      # vérifie que les chiffres du README sont à jour
├── examples/                  # walkthroughs de sorties réelles (anonymisées)
└── tests/                     # selftests, TDD par vague, E2E, activation sémantique
```

## Installation dans ton harness

Les liens `.claude/skills/`, `.cursor/skills/`, `.hermes/skills/`, `.kilocode/skills/` ne sont
**pas commités** (gitignorés) : ils se créent après le clone, en une commande.

```bash
# Prévisualiser ce qui sera lié (aucune écriture)
bash adapters/link-skills.sh -n

# Créer les symlinks .claude/skills/, .cursor/skills/, .hermes/skills/…
bash adapters/link-skills.sh
```

**Windows (PowerShell) :**
```powershell
# Prévisualiser (dry-run)
powershell -File adapters/link-skills.ps1 -DryRun

# Créer les junctions
powershell -File adapters/link-skills.ps1
```

Si une vieille copie figée d'un skill traîne dans un dossier harness, l'adapter la signale
et la saute ; `-f` / `-Force` la remplace par un lien propre.

Ou manuellement : pointe ton harness vers `.agents/skills/<nom>/SKILL.md`.

## Domaines couverts

| Domaine | Skills |
|---|---|
| 🔬 R&D & stratégie | `be-business-plan`, `be-market-research`, `be-funding-subsidies` |
| 💰 Finance & compta | `be-accounting-basics`, `be-invoicing-peppol`, `be-bookkeeping-ops` |
| ⚖️ Admin & légal | `be-company-setup`, `be-rgpd-compliance` |
| 📣 Contenu | `content-engine-be`, `brand-voice-solopreneur` |
| 📡 Veille | `social-listening-be` (lawful only : APIs officielles, RSS, exports manuels), `be-competitor-watch` |
| 🗂 Ops & secrétariat | `secretary-ops`, `be-admin-deadlines` |
| 🔍 Fact-check & sourcing | `fact-check-sourcing` |
| 💼 Vente & prospection | `be-sales-outreach` |
| 📊 Modélisation financière | `be-financial-modeling` |
| 📝 Contrats & légal | `be-contracts-legal` |
| 🛠 Meta & maintenance | `skill-forge` (créer un skill conforme), `agency-doc-keeper` (tenir la doc à jour) |

## Contribuer

1. Copie `.agents/skills/_template/SKILL.md` — ou laisse l'agent le faire avec le skill `skill-forge`.
2. Écris **deep** : Overview → When to Use → Workflow avec critères de complétion →
   Pitfalls → Verification Checklist. 6-15k caractères ; le détail lourd part en `references/`.
3. `python scripts/validate_skills.py && python scripts/security_scan.py` → les deux exit 0.
4. Tiens la doc à jour avec le rituel du skill `agency-doc-keeper` (index, compteurs, changelog).
5. Commit.

Dépendance de dev unique : `pip install -r requirements.txt` (PyYAML).

## Vérification complète (gates + TDD)

Les gates tournent en CI sur chaque push/PR (`.github/workflows/ci.yml`) :

```bash
python scripts/validate_skills.py       # 20/20 skills valides
python scripts/security_scan.py         # 0 leak bloquant
python scripts/check_related_links.py   # 58 liens, 0 morts
python scripts/build_index.py --check   # INDEX.md + catalog.json à jour
python scripts/check_doc_sync.py        # chiffres du README synchronisés
python scripts/freshness_report.py      # fraîcheur réglementaire (seuil 6 mois)
```

**Tests** (TDD : écrits avant le code) :
```bash
python tests/test_scanner_selftest.py    # 12/12 auto-tests scanner
python tests/test_validator_selftest.py  # 7/7 auto-tests validateur
python tests/test_factcheck_tdd.py       # 10/10 tests fact-check-sourcing
python tests/test_vague3_tdd.py          # 18/18 tests vague 3
python tests/test_vague4_tdd.py          # tests vague 4 (skill-forge, agency-doc-keeper)
python tests/test_build_index.py         # auto-tests build_index
python tests/test_freshness_report.py    # auto-tests freshness_report
python tests/test_doc_sync.py            # auto-tests check_doc_sync
python tests/test_activation.py          # 36/36 scénarios d'activation sémantique
python tests/test_e2e.py                 # 26/26 tests E2E workflow
```

Scénarios d'activation sémantique : voir [tests/ACTIVATION.md](tests/ACTIVATION.md).

## Pour les incubateurs

The Agency est un outil **open source** (MIT) que vous pouvez proposer à vos bénéficiaires :

### Valeur ajoutée pour vos entrepreneurs
- **20 skills** couvrant tout le cycle d'entrepreneuriat (R&D, finance, admin, contenu, veille, prospection, contrats)
- **Harness-agnostic** : fonctionne sur ChatGPT, Mistral, Claude, Cursor, Gemini — pas de lock-in
- **Données belges sourcées** : chaque chiffre a un `as_of` et une source officielle (SPF Finances, INASTI, BCE, VLAIO…), avec veille de fraîcheur automatisée en CI
- **Sécurisé** : 10 suites de tests automatisées, 0 leak, gate actif de fact-checking
- **Gratuit** : licence MIT, réutilisable, modifiable

### Comment intégrer
1. **Partager le lien GitHub** avec vos bénéficiaires
2. **Recommander** les skills pertinents selon leur étape (création → `be-company-setup`, facturation → `be-invoicing-peppol`, etc.)
3. **Contribuer** : proposer des skills spécifiques à votre région ou votre secteur via CONTRIBUTING.md
4. **Adapter** : fork le repo et personnalisez pour votre incubateur

Incubateur partenaire ? Ouvrez une issue GitHub pour être listé ici.

### Licence
MIT — libre de réutiliser, modifier, et distribuer. Voir [LICENSE](LICENSE).

## Disclaimer

Contenu informatif général (dates `as_of` indiquées). Pas du conseil fiscal, comptable ou
juridique personnalisé — faites valider par un professionnel agréé en Belgique.

Licence : [MIT](LICENSE).
