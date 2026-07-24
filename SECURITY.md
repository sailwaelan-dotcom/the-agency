# Sécurité & Confidentialité — The Agency

Ce document définit les règles **non négociables** de sécurité pour ce dépôt de skills/agents.
Il s'applique à tout contributeur (humain ou agent IA) qui ajoute ou modifie un skill.

---

## 1. Zéro téléchargement non audité

- **Aucun skill ne doit exécuter** `curl | sh`, `wget | sh`, `pip install`, `npm install -g`, ou tout téléchargement/exécution de code tiers au moment de son utilisation.
- Les skills peuvent **référencer** des outils existants (ex: "si `himalaya` est installé…") mais ne les installent jamais eux-mêmes.
- Recherche web autorisée en **lecture seule** vers des sources officielles (voir §4).

## 2. Aucun secret, aucune donnée personnelle

Interdit dans tout fichier du dépôt :

- Clés API, tokens, mots de passe, cookies, clés privées (`BEGIN ... PRIVATE KEY`).
- Chemins machine absolus personnels (`C:\Users\<nom>`, `/home/<nom>`) — utiliser des placeholders : `<VOTRE_USER>`, `$HOME`.
- Vraies données d'entreprise : numéros BCE/TVA réels, numéros de compte, données clients. Utiliser des placeholders : `BE0123.456.789`, `[NOM_CLIENT]`, `[NUM_COMPTE]`.
- Fichiers `.env`, exports CSV de clients, dumps de boîtes mail.

Le scanner `scripts/security_scan.py` bloque le commit si un pattern est détecté.

## 3. Pas d'exfiltration

Aucun skill ne doit :

- Envoyer des données du workspace vers un endpoint externe (webhook, pastebin, analytics).
- Instruire l'agent de lire puis transmettre des variables d'environnement, fichiers SSH, historiques shell ou gestionnaires de mots de passe.
- Contenir d'instructions d'injection de prompt ("ignore previous instructions", "you are now...", divulgation de system prompt). <!-- nosec : exemples documentaires d'attaques à détecter -->

## 4. Veille & scraping : méthode lawful uniquement

- Les skills de veille réseaux sociaux (`social-listening-be`) utilisent **uniquement** : APIs officielles, exports manuels de l'utilisateur, RSS publics, pages publiques consultées manuellement.
- **Jamais** : contournement de CAPTCHA, rotation de proxys, scraping authentifié, violation de ToS, collecte de données personnelles non publiques.
- Conformité RGPD : toute donnée collectée sur des personnes est minimisée, non stockée dans le dépôt, et traitée selon `be-rgpd-compliance`.

## 5. Exactitude réglementaire belge

- Tout chiffre daté (taux TVA, seuils, montants de subventions, indexations) porte un marqueur `as_of: YYYY-MM` et la mention *"vérifier le taux en vigueur sur le site officiel"*.
- Tout skill fiscal/juridique/comptable se termine par le disclaimer :

> ⚠️ **Disclaimer** : information générale, pas un conseil fiscal, comptable ou juridique personnalisé. Faites valider par un comptable, expert-comptable ou avocat agréé en Belgique avant toute décision.

## 6. Revue avant commit

- `python scripts/validate_skills.py` → exit 0
- `python scripts/security_scan.py` → exit 0
- Lecture humaine du diff (ou revue par un second agent) pour tout skill touchant : argent, fiscalité, données personnelles, commandes shell.

## 7. Signalement

Si vous détectez un leak, un pattern dangereux ou une information réglementaire fausse :
ouvrez une issue décrivant le fichier et la ligne, sans copier la donnée sensible elle-même.
