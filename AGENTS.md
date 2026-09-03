# The Agency — Instructions pour agents IA

Ce dépôt est une **boîte à outils de skills harness-agnostic** pour solopreneurs belges.
Tu lis ce fichier parce qu'un harness t'a déposé ici. Voici les règles du jeu.

## Ce que tu trouves ici

- `.agents/skills/` — les skills (format [agentskills.io](https://agentskills.io/specification)).
  Chaque skill = un dossier `<nom>/SKILL.md`. Charge-le quand sa `description` matche la demande.
- `.agents/agents/` — personas métier (comptable, secrétaire, R&D…) qui combinent plusieurs skills.
- `SECURITY.md` — **à lire avant d'écrire quoi que ce soit** dans ce dépôt.
- `scripts/validate_skills.py` — validation structurelle (exit 0 requis avant commit).
- `scripts/security_scan.py` — scan anti-leak (exit 0 requis avant commit).
- `scripts/build_index.py` — régénère `INDEX.md` + `catalog.json` (à relancer après tout
  ajout/retrait de skill).
- `scripts/check_doc_sync.py` — vérifie que les chiffres du README matchent le repo.
- `scripts/freshness_report.py` — âge des `as_of` ; un skill > 6 mois doit être revu.

## Règles absolues

1. **Jamais de données réelles** : pas de vrai numéro BCE/TVA/IBAN/compte, pas de données
   clients, pas de chemins machine (`C:\Users\<nom>`). Placeholders : `BE0123.456.789`,
   `[NOM_CLIENT]`, `<VOTRE_USER>`.
2. **Zéro exécution non auditée** : aucun skill n'installe ni ne télécharge de code.
   Référencer un outil existant, oui ; lancer un script distant pipé dans un shell, jamais.
3. **Exactitude réglementaire** : tout chiffre daté (TVA, cotisations, seuils) porte
   `as_of` + « vérifier le taux en vigueur ». Disclaimer comptable/avocat obligatoire
   sur les skills finance/legal.
4. **Portabilité** : pas de clé frontmatter harness-spécifique (`allowed-tools`, `model`,
   `hooks`…). Le frontmatter canonique est dans `.agents/skills/_template/SKILL.md`.
5. **Veille lawful** : APIs officielles, RSS, exports manuels uniquement. Jamais de
   contournement CAPTCHA/proxy/auth (voir `social-listening-be`).
6. **Langue** : français par défaut ; termes légaux belges conservés (BCE, SRL, INASTI, Peppol).

## Workflow de contribution

1. Copier `_template/SKILL.md` → nouveau dossier sous `.agents/skills/<nom>/`
   (le skill `skill-forge` décrit ce processus en détail).
2. Écrire (deep > shallow : sections Overview / When to Use / Workflow / Pitfalls / Checklist).
3. `python scripts/validate_skills.py` → exit 0.
4. `python scripts/security_scan.py` → exit 0.
5. Rituel doc (skill `agency-doc-keeper`) : `build_index.py`, compteurs README,
   `check_doc_sync.py`, CHANGELOG.
6. Commit atomique : un skill = un commit, ou un lot cohérent par domaine.

## Disclaimer global

Les contenus fiscaux, comptables et juridiques sont de l'**information générale**
(as_of la date indiquée), pas du conseil personnalisé. Toujours faire valider par un
professionnel agréé en Belgique avant décision engageante.
