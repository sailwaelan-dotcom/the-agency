# Contribuer à The Agency

Merci de votre intérêt pour contribuer à The Agency ! Ce document explique comment
proposer un nouveau skill, améliorer un skill existant, ou signaler un problème.

## Philosophie

The Agency est une boîte à outils de skills **harness-agnostic** pour les solopreneurs
belges. Chaque skill doit être :
- **Deep** (interface simple, contenu riche) — pas shallow (interface complexe, contenu vide)
- **Harness-agnostic** (fonctionne sur ChatGPT, Mistral, Claude, Cursor, Gemini…)
- **Sourcé** (chaque chiffre a un `as_of` et une source officielle)
- **Sécurisé** (aucun leak, aucun scraping, aucune donnée personnelle)

## Comment proposer un nouveau skill

1. **Fork** le repo
2. **Copier** `.agents/skills/_template/SKILL.md` dans un nouveau dossier
3. **Écrire** le skill (6-15k caractères, sections obligatoires : Overview, When to Use, Workflow, Pitfalls, Checklist)
4. **Valider** localement :
   ```bash
   python scripts/validate_skills.py
   python scripts/security_scan.py
   python scripts/check_related_links.py
   ```
5. **Tester** l'activation (le skill se charge-t-il quand on pose une question correspondante ?)
6. **Pull request** avec description claire du skill et de sa valeur ajoutée

## Standards de qualité

### Frontmatter (obligatoire)
```yaml
name: nom-du-skill              # lowercase, hyphens, ≤64 chars
description: "Utilisez quand…"  # trigger-focused, ≤1024 chars
version: 0.1.0
license: MIT
author: Votre nom
metadata:
  tags: [domaine, be]
  related_skills: [autre-skill]
  domain: rd|finance|admin|content|ops|sales|legal
  language: fr
  as_of: "YYYY-MM"
```

### Champs interdits (harness-specific)
`allowed-tools`, `disallowed-tools`, `hooks`, `model`, `effort`, `context`, `agent`, `shell`

### Sections obligatoires
- `## Overview` — 2-4 phrases
- `## When to Use` — triggers + contre-triggers
- `## Workflow` — étapes avec critères de complétion
- `## Common Pitfalls` — pièges réels
- `## Verification Checklist` — checkboxes actionnables

### Disclaimer (si tags finance/tax/legal/accounting)
```markdown
> ⚠️ **Disclaimer** : information générale (as_of YYYY-MM), pas un conseil [fiscal/comptable/juridique]
> personnalisé. Faites valider par un [comptable/expert-comptable/avocat] agréé en Belgique.
```

## Signaler un problème

- **Donnée obsolète** : ouvrir une issue avec le tag `outdated-data`
- **Bug de sécurité** : ouvrir une issue avec le tag `security` (ne pas publier de détails sensibles)
- **Suggestion d'amélioration** : ouvrir une issue avec le tag `enhancement`

## Licence

Tous les contributions sont sous licence MIT.
