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
│   ├── validate_skills.py    # validation structurelle
│   └── security_scan.py      # scan anti-leak (exit 1 si bloquant)
└── tests/
    ├── test_scanner_selftest.py
    └── ACTIVATION.md         # scénarios de test d'activation
```

## Installation dans ton harness

```bash
# Prévisualiser ce qui sera lié (aucune écriture)
bash adapters/link-skills.sh -n

# Créer les symlinks .claude/skills/, .cursor/skills/, .hermes/skills/…
bash adapters/link-skills.sh
```

Ou manuellement : pointe ton harness vers `.agents/skills/<nom>/SKILL.md`.

## Domaines couverts (vague 1)

| Domaine | Skills |
|---|---|
| 🔬 R&D & stratégie | `be-business-plan`, `be-market-research`, `be-funding-subsidies` |
| 💰 Finance & compta | `be-accounting-basics`, `be-invoicing-peppol`, `be-bookkeeping-ops` |
| ⚖️ Admin & légal | `be-company-setup`, `be-rgpd-compliance` |
| 📣 Contenu | `content-engine-be`, `brand-voice-solopreneur` |
| 📡 Veille | `social-listening-be` (lawful only : APIs officielles, RSS, exports manuels) |
| 🗂 Ops & secrétariat | `secretary-ops` |

## Contribuer

1. Copie `.agents/skills/_template/SKILL.md`.
2. Écris **deep** : Overview → When to Use → Workflow avec critères de complétion →
   Pitfalls → Verification Checklist. 6-15k caractères ; le détail lourd part en `references/`.
3. `python scripts/validate_skills.py && python scripts/security_scan.py` → les deux exit 0.
4. Commit.

## Disclaimer

Contenu informatif général (dates `as_of` indiquées). Pas du conseil fiscal, comptable ou
juridique personnalisé — faites valider par un professionnel agréé en Belgique.

Licence : [MIT](LICENSE).
