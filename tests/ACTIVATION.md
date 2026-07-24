# Tests d'activation — The Agency

Ce document décrit les scénarios de test d'activation sémantique des skills :
vérifier que les `description` des skills déclenchent correctement le chargement
par un agent IA, et que les skills produisent des artefacts utiles.

---

## Test 1 : activation par description trigger-focused

**Méthode** : pour chaque skill, formuler 3 requêtes utilisateur typiques (issues de
la section "When to Use") et vérifier qu'un agent charge le bon skill.

| Skill | Requête test 1 | Requête test 2 | Requête test 3 |
|---|---|---|---|
| `be-invoicing-peppol` | « Je dois envoyer une facture à un client belge » | « Peppol c'est quoi ? » | « Mon client me demande une facture UBL » |
| `be-accounting-basics` | « Franchise TVA ou régime normal ? » | « C'est quoi mes échéances ce trimestre ? » | « Combien je mets de côté pour l'impôt ? » |
| `be-bookkeeping-ops` | « C'est la fin du mois, qu'est-ce que je dois faire côté compta ? » | « Mon comptable me réclame mes pièces » | « Un client n'a pas payé, je relance comment ? » |
| `be-company-setup` | « Je veux me lancer indépendant en Belgique » | « Personne physique ou SRL ? » | « Je viens d'avoir mon numéro BCE, c'est quoi la suite ? » |
| `be-business-plan` | « Je dois faire un business plan pour la banque » | « C'est quoi un plan financier pour une SRL ? » | « Mon breakeven, je le calcule comment ? » |
| `be-market-research` | « Mon idée tient la route ? Il y a un marché en Belgique ? » | « Qui sont mes concurrents en Belgique ? » | « Comment je parle à des clients potentiels ? » |
| `be-funding-subsidies` | « Y a-t-il des subsides pour mon projet ? » | « Je suis en Wallonie, à quel guichet je m'adresse ? » | « Microcrédit ou prêt d'honneur ? » |
| `be-rgpd-compliance` | « Je lance un formulaire de contact, RGPD ? » | « Je veux envoyer une newsletter » | « Un client me demande de supprimer ses données » |
| `content-engine-be` | « Je ne sais pas quoi poster sur LinkedIn » | « Comment transformer un article en posts ? » | « Je passe 3h par post, c'est pas tenable » |
| `brand-voice-solopreneur` | « Mes textes ne se ressemblent pas » | « Comment je sonne professionnel sans être pompeux ? » | « Corrige ce post pour qu'il me ressemble » |
| `social-listening-be` | « Je veux savoir ce qu'on dit de moi en ligne » | « Comment suivre mes concurrents sur LinkedIn ? » | « Je cherche des sujets de contenu pour mon secteur » |
| `secretary-ops` | « Je passe mes matinées dans ma boîte mail » | « J'ai raté une échéance administrative » | « Je cherche un document pendant 20 minutes » |

**Résultat attendu** : chaque requête charge le skill correspondant (ou un agent persona
qui le charge en cascade).

---

## Test 2 : validation structurelle automatique

```bash
python scripts/validate_skills.py    # exit 0 = 12/12 valides
python scripts/security_scan.py     # exit 0 = aucun leak bloquant
python tests/test_scanner_selftest.py  # 12/12 auto-tests
python tests/test_validator_selftest.py # 7/7 auto-tests
python scripts/check_related_links.py  # 32 liens, 0 morts
```

---

## Test 3 : activation réelle (manuel)

Pour tester l'activation réelle dans un harness :

1. **Claude Code** : charger le repo, taper `/be-invoicing-peppol` ou poser une
   question facture → le skill doit se charger automatiquement.
2. **Cursor** : ouvrir le projet, taper une requête dans le chat → le skill doit
   apparaître dans le contexte.
3. **Hermes** : `skill_view(name='be-invoicing-peppol')` doit retourner le contenu.
4. **Kilocode** : même principe que Cursor.

**Critères de succès** :
- [ ] Le bon skill se charge pour chaque requête du tableau ci-dessus
- [ ] Le contenu du skill est actionnable (pas générique)
- [ ] Le disclaimer est présent sur les skills réglementaires
- [ ] Aucun skill harness-spécifique ne bloque le chargement

---

## Test 4 : sécurité (automatique)

Le scanner couvre :
- Secrets (clés API, tokens, clés privées)
- Chemins machine absolus (Windows, Unix, macOS, MSYS)
- Exfiltration (webhooks, curl|sh, pastebin)
- Injection de prompt (ignore instructions, roleplay, system prompt)
- Identifiants belges réels (numéros BCE, IBAN, numéros nationaux)

**Auto-tests** : `tests/test_scanner_selftest.py` (12 cas couverts).

---

## Test 5 : portabilité harness-agnostic

Le frontmatter de chaque skill ne contient QUE les champs portables :
- `name`, `description`, `version`, `license`, `author`, `compatibility`, `metadata`

**Champs interdits** (détectés par le validateur) :
`allowed-tools`, `disallowed-tools`, `hooks`, `model`, `effort`, `context`,
`agent`, `shell`, `disable-model-invocation`, `user-invocable`, `argument-hint`,
`paths`, `mcp`.

**Résultat attendu** : `python scripts/validate_skills.py` exit 0 = aucun champ
harness-spécifique détecté.
