# The Agency 🇧🇪

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

## Structure

```
The agency/
├── AGENTS.md                 # Instructions pour tout agent qui entre ici
├── SECURITY.md               # Règles non négociables (leaks, scraping, disclaimers)
├── .agents/
│   ├── skills/               # ← les skills (canonique)
│   │   ├── _template/        #   squelette à copier pour contribuer
│   │   ├── be-business-plan/
│   │   └── …
│   └── agents/               # personas métier combinant plusieurs skills
├── adapters/
│   └── link-skills.sh        # symlink vers .claude/.cursor/.hermes/…
├── scripts/
│   ├── validate_skills.py    # validation structurelle (frontmatter, sections, disclaimer)
│   ├── security_scan.py      # scan anti-leak (secrets, chemins, injection, exfiltration)
│   └── check_related_links.py # vérifie que tous les related_skills résolvent
└── tests/
    ├── test_scanner_selftest.py   # 12 auto-tests du scanner
    ├── test_validator_selftest.py # 7 auto-tests du validateur
    └── ACTIVATION.md              # scénarios de test d'activation sémantique
```

## Installation dans ton harness

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

Ou manuellement : pointe ton harness vers `.agents/skills/<nom>/SKILL.md`.

## Domaines couverts (vague 1)

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

## Contribuer

1. Copie `.agents/skills/_template/SKILL.md`.
2. Écris **deep** : Overview → When to Use → Workflow avec critères de complétion →
   Pitfalls → Verification Checklist. 6-15k caractères ; le détail lourd part en `references/`.
3. `python scripts/validate_skills.py && python scripts/security_scan.py` → les deux exit 0.
4. Commit.

## Vérification complète (5 gates + TDD)

Avant chaque commit, les 5 gates doivent passer :

```bash
python scripts/validate_skills.py      # 18/18 skills valides
python scripts/security_scan.py        # 0 leak bloquant
python tests/test_scanner_selftest.py  # 12/12 auto-tests scanner
python tests/test_validator_selftest.py # 7/7 auto-tests validateur
python scripts/check_related_links.py  # 53 liens, 0 morts
```

**Tests TDD** (écrits avant le code) :
```bash
python tests/test_factcheck_tdd.py     # 8/8 tests fact-check-sourcing
python tests/test_vague3_tdd.py        # 18/18 tests vague 3
python tests/test_e2e.py               # 26/26 tests E2E workflow
```

Scénarios d'activation sémantique : voir [tests/ACTIVATION.md](tests/ACTIVATION.md).

## Pour les incubateurs

The Agency est un outil **open source** (MIT) que vous pouvez proposer à vos bénéficiaires :

### Valeur ajoutée pour vos entrepreneurs
- **18 skills** couvrant tout le cycle d'entrepreneuriat (R&D, finance, admin, contenu, veille, prospection, contrats)
- **Harness-agnostic** : fonctionne sur ChatGPT, Mistral, Claude, Cursor, Gemini — pas de lock-in
- **Données belges sourcées** : chaque chiffre a un `as_of` et une source officielle (SPF Finances, INASTI, BCE, VLAIO…)
- **Sécurisé** : 89 tests, 0 leak, gate actif de fact-checking
- **Gratuit** : licence MIT, réutilisable, modifiable

### Comment intégrer
1. **Partager le lien GitHub** avec vos bénéficiaires
2. **Recommander** les skills pertinents selon leur étape (création → `be-company-setup`, facturation → `be-invoicing-peppol`, etc.)
3. **Contribuer** : proposer des skills spécifiques à votre région ou votre secteur via CONTRIBUTING.md
4. **Adapter** : fork le repo et personnalisez pour votre incubateur

### Incubateurs partenaires (à compléter)
| Incubateur | Région | Contact |
|---|---|---|
| *Votre incubateur ici ?* | *Région* | *Ouvrir une issue GitHub* |

### Licence
MIT — libre de réutiliser, modifier, et distribuer. Voir [LICENSE](LICENSE).

## Disclaimer

Contenu informatif général (dates `as_of` indiquées). Pas du conseil fiscal, comptable ou
juridique personnalisé — faites valider par un professionnel agréé en Belgique.

Licence : [MIT](LICENSE).
