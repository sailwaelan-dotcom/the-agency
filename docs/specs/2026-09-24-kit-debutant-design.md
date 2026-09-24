# Kit débutant multi-IA — design (partie 1)

- **Date** : 2026-09-24
- **Statut** : design validé en conversation, corrigé après un déroulé du parcours
  (profil gardé sans fichier, instructions copiées depuis le guide, ZIP sur Mac) ; spec en
  relecture, essai réel à venir
- **Portée** : partie 1 d'un chantier en 4 parties (voir section 11)

## 1. Contexte

The Agency est solide techniquement (22 skills valides, 6 gates au vert, 165 tests, release
v1.0.0 avec `TheAgency.exe` et `TheAgency-Setup.exe`), mais un débutant complet décroche à
quatre endroits avant d'arriver à la valeur :

1. **Arrivée** — il atterrit sur GitHub ; le README parle de harness, MCP, TDD et gates, et
   ne donne aucun lien de téléchargement vers la release.
2. **Installation** — l'exe n'est pas signé : Windows affiche « Windows a protégé votre
   ordinateur ».
3. **Accès à son IA** — les skills, qui sont la vraie valeur, n'arrivent pas dans son IA :
   en mode exe, la liaison des skills écrit dans le dossier temporaire du bundle, effacé à
   la fermeture (`install.py`, `adapters/link-skills.ps1`) ; dans Claude Desktop,
   `load_skill_context` exige un nom exact que le modèle ne peut pas découvrir ; pour
   ChatGPT, Gemini ou Le Chat, aucun chemin n'existe.
4. **Premier usage** — une console à 7 options, dont une facture générée avec des données
   de démo codées en dur ; rien ne dit quoi demander à son IA.

## 2. Objectif et critères de succès

- **Pour qui** : des indépendants belges débutants complets en informatique, qui utilisent
  un mélange d'IA (ChatGPT, Claude, Gemini, Le Chat, Copilot…).
- **Pourquoi** : un outil gratuit et open source à diffuser (incubateurs, réseau) qui sert
  aussi de vitrine à l'activité de conseil de l'auteur (waelan.be).
- **Critère de succès** : le débutant obtient **son plan personnalisé** (onboarding
  `activate-agency` : profil, 3 à 5 skills prioritaires, plan 30 jours) en **moins de
  10 minutes, sans aide, quelle que soit son IA**.
- **Hypothèses** : v1 en français (l'IA répond dans la langue de l'utilisateur) ; rien à
  installer, donc indifférent Windows/Mac.

## 3. Décisions

- **Approche retenue : un kit multi-IA généré depuis le repo** (approche A). Écartées :
  l'exe Windows comme produit principal (exclut Mac et les IA web, signature payante) et
  l'assistant hébergé sur waelan.be (coût d'API par utilisateur, RGPD, responsabilité ;
  envisageable plus tard en démo limitée).
- **Ce que permettent les plateformes** (septembre 2026) :

  | IA | Constat | Conséquence |
  |---|---|---|
  | Claude | Skills sur tous les forfaits, gratuit compris ; import d'un ZIP ; exécution de code requise | ZIP natif, un seul import |
  | ChatGPT | Skills réservés à Business/Enterprise/Edu ; GPT personnalisés en retrait ; Projets sur tous les forfaits (instructions 8 000 car., 5 fichiers par projet et 3 envois par jour en gratuit) | Projet : instructions + fichiers |
  | Gemini | Gems gratuits, partageables par lien, 10 fichiers ; instructions limitées (~2 000 car., source secondaire) | Gem : instructions + fichiers ; Gem public en partie 2 |
  | Le Chat et autres | Pas de partage public confirmé ; envoi de documents limité en gratuit | Fichier joint + texte collé |

  Les constats ChatGPT et Le Chat viennent de sources secondaires : à revérifier pendant la
  recette (section 10).

## 4. Le kit

Quatre fichiers, joints à chaque release GitHub :

| Fichier | Pour | Contenu |
|---|---|---|
| `the-agency-claude.zip` | Claude | Un seul skill `the-agency` : un SKILL.md d'aiguillage et les 20 fiches en `references/`. |
| `the-agency-instructions.txt` | ChatGPT, Gemini, autres | ≤ 1 500 caractères : rôle, règles, « commence par l'accueil ». Se colle dans le champ Instructions d'un Projet ou d'un Gem, ou comme premier message. Le guide affiche le même texte avec un bouton copier : le débutant n'ouvre jamais ce fichier, qui sert aux pages web (waelan.be) et aux utilisateurs avancés. |
| `the-agency-accueil.md` | idem | Les règles communes, l'onboarding complet (`activate-agency`) et le sommaire des 20 fiches (~25 000 car.). Suffit à lui seul pour le premier résultat. |
| `the-agency-fiches.md` | idem | Les 19 autres fiches, une section chacune (~190 000 car.). |

- **Les 20 fiches** = les skills de `.agents/skills/` hors `_template`, `skill-forge` et
  `agency-doc-keeper` (maintenance du repo). Les personas (`.agents/agents/`), le serveur
  MCP et l'exe restent hors du kit (utilisateurs avancés).
- **Pourquoi 1 500 caractères** : ce qui rentre partout (Gem ~2 000, Projet ChatGPT 8 000,
  instructions personnalisées ChatGPT gratuit 1 500).
- **Pourquoi l'accueil à part** : les quotas d'envoi des forfaits gratuits ; le premier
  résultat ne dépend que du petit fichier.

### Parcours par IA

| IA | Gestes (une seule fois sauf mention) | Durée visée |
|---|---|---|
| Claude | Télécharger le ZIP **sans l'ouvrir** → menu Skills → importer → « Active l'agence » | ~3 min |
| ChatGPT | Créer un Projet → coller les instructions copiées depuis le guide → ajouter les 2 fichiers → « Active l'agence » | ~4 min |
| Gemini | Nouveau Gem → coller les instructions copiées depuis le guide → ajouter les 2 fichiers → « Active l'agence » (partie 2 : un lien, ~30 s) | ~4 min |
| Autre IA | Joindre `the-agency-accueil.md` → coller les instructions copiées depuis le guide (à chaque conversation) | ~1 min |

**Garder son profil, sans créer de fichier** : en fin d'accueil, l'IA donne le profil dans
un bloc à copier (≤ 1 500 caractères visés) et dit où le coller selon l'IA :

- **Projet ChatGPT** : à la fin des Instructions du Projet (1 500 + 1 500 caractères
  tiennent dans la limite de 8 000) ;
- **Gem** : à la fin des Instructions du Gem, si sa limite le permet ;
- **sinon** (Claude, autres IA, Gem trop court) : au début de la conversation suivante.

Les conversations suivantes démarrent alors avec son contexte. On ne demande jamais au
débutant de créer, d'enregistrer ou d'envoyer un fichier de profil.

### Brouillon des instructions (≤ 1 500 caractères)

```text
Tu es « The Agency », l'assistant des indépendants en Belgique. Tes connaissances sont dans
les fichiers the-agency-accueil.md et the-agency-fiches.md.
1. Si un profil « AGENCY_PROFILE » figure à la fin de ces instructions ou dans la
   conversation, pars de lui. Sinon, ou si l'on te dit « Active l'agence » : suis
   l'accueil du fichier the-agency-accueil.md, du début à la fin.
2. Pour toute autre demande : trouve la fiche adaptée dans le sommaire de
   the-agency-accueil.md, lis-la dans the-agency-fiches.md et suis sa méthode.
3. Pose tes questions en une seule fois, avec des choix simples. Si la personne ne sait
   pas, note « à confirmer ». N'invente jamais un chiffre.
4. Tout chiffre daté (TVA, cotisations, seuils) porte sa date « à jour au » et la mention
   « vérifier le taux en vigueur ».
5. Tu donnes de l'information générale, pas un conseil personnalisé : pour décider, fais
   valider par un comptable ou un avocat agréé en Belgique.
6. Parle simplement, sans jargon, dans la langue de la personne.
7. Si un fichier manque, dis-le et demande-le au lieu de répondre de mémoire.
```

### Brouillon de la description du skill `the-agency` (≤ 1 024 caractères)

> Utilisez quand un indépendant ou futur indépendant en Belgique demande de l'aide :
> démarrer (« Active l'agence »), TVA, INASTI, impôts, échéances, facture Peppol, devis,
> comptabilité, création d'entreprise ou de SRL, business plan, financement et subsides,
> RGPD, contrats, prospection, contenu LinkedIn, veille, secrétariat. Oriente vers la bonne
> fiche parmi 20, datée et avec avertissement.

## 5. Règles communes (`kit/regles.md`)

Écrites une fois, incluses dans le SKILL.md `the-agency` et dans l'accueil :

1. Questions en une seule salve, options fermées, échappatoire « je ne sais pas » notée
   « à confirmer » ; jamais de donnée inventée.
2. Tout chiffre daté porte son `as_of` et « vérifier le taux en vigueur ».
3. Information générale, pas un conseil : renvoi vers un comptable ou un avocat agréé en
   Belgique avant toute décision engageante.
4. Après toute recherche web, appliquer la méthode de la fiche `fact-check-sourcing`
   (sources officielles belges d'abord).
5. **Outils absents** : quand une fiche cite un outil `agency-be-mcp` que l'IA n'a pas
   (ex. vérification BCE modulo 97), l'IA fait le calcul en le montrant pas à pas, ou
   renvoie au site officiel (recherche publique KBO, VIES, annuaire Peppol).
6. Ne jamais demander de mot de passe, de code bancaire ni de numéro national ; pour des
   données personnelles de clients, rappeler le RGPD (fiche `be-rgpd-compliance`).
7. Veille : méthodes légales uniquement (fiche `social-listening-be`).
8. Répondre dans la langue de l'utilisateur, en mots simples ; termes légaux belges
   conservés (BCE, SRL, INASTI, Peppol).

## 6. Fabrication

### Sources écrites à la main — nouveau dossier `kit/`

- `kit/skill-routeur.md` — modèle du SKILL.md `the-agency` : frontmatter (`name:
  the-agency`, description ci-dessus, `license: MIT`, `metadata` : version, tags, as_of,
  language) et corps avec les sections exigées par `validate_skills.py` (Overview, When to
  Use, Questions à poser, Workflow, Common Pitfalls, Verification Checklist, Disclaimer).
  Repères remplis par le générateur : `{{REGLES}}`, `{{SOMMAIRE}}`, `{{VERSION}}`.
- `kit/regles.md` — les règles communes (section 5).
- `kit/instructions.txt` — le texte de la section 4.

### Générateur — `scripts/build_kit.py`

- Bibliothèque standard + PyYAML (déjà dépendance du repo) ; parsing du frontmatter
  aligné sur `build_index.py` et `skill_meta.split_list`.
- **Entrées** : `.agents/skills/*/SKILL.md` et leurs `references/`, hors `_template` et
  `KIT_EXCLUDE = {"skill-forge", "agency-doc-keeper"}` ; les trois fichiers de `kit/`.
- **Sortie** : `dist/kit/` (déjà ignoré par git). Options : `--out DIR` (tests),
  `--version VERSION` (défaut `dev` ; la CI passe le tag, le `v` initial est retiré pour
  `metadata.version`). `metadata.as_of` du skill `the-agency` = le plus récent des `as_of`
  des 20 fiches (déterministe, tiré des sources).
- **Structure du ZIP** : `the-agency/SKILL.md`, puis `the-agency/references/<skill>/FICHE.md`
  (le SKILL.md d'origine, renommé pour ne jamais avoir de SKILL.md imbriqué) et
  `the-agency/references/<skill>/references/*` (les liens relatifs des fiches restent
  valides).
- **Accueil** : en-tête court, règles communes, corps de `activate-agency` (frontmatter
  retiré, texte inchangé), sommaire des 20 fiches (nom, « quand l'utiliser » tiré de la
  `description`, emplacement).
- **Fiches** : sommaire, puis pour chacune des 19 fiches un en-tête `# Fiche n/19 — <nom>`
  (description, `as_of`), le corps inchangé (frontmatter retiré) et ses annexes
  `references/` sous `## Annexe — references/<fichier>`.
- **Aucune réécriture** du contenu des skills : seuls le sommaire et l'assemblage sont
  générés.
- **Reproductible** : entrées triées, date fixe dans le ZIP (1980-01-01), permissions
  fixes, aucune date de fabrication dans les fichiers — même source, mêmes octets.
- **Échecs bloquants (exit 1, message explicite)** : instructions > 1 500 caractères,
  description > 1 024, skill sans frontmatter lisible, fiche du sommaire absente du
  résultat, SKILL.md imbriqué dans le ZIP.

## 7. `activate-agency` 1.1.0

Tests d'abord (extension de `tests/test_vague5_tdd.py`), puis le skill :

- **Profil existant** : chercher aussi un profil collé dans la conversation ou présent
  dans les Instructions du Projet ou du Gem, pas seulement un fichier sur disque.
- **Mode conversation** : si l'IA n'a pas de dossier de travail, elle affiche le profil
  complet dans un bloc à copier (≤ 1 500 caractères visés) et dit où le coller selon l'IA
  (section 4, « Garder son profil ») — jamais « crée un fichier ». Quand un dossier de
  travail existe (Claude Code, Cursor…), le comportement actuel est conservé :
  `AGENCY_PROFILE.md` écrit hors du repo.
- **Mode débutant** : chaque option est expliquée en mots simples, **sans chiffre**
  (pitfall existant « chiffrer pendant l'onboarding ») ; « je ne sais pas » devient
  « à confirmer ».
- **Handoff en langage courant** : « Dis : Prépare mon calendrier d'échéances avec mon
  profil » (nom du skill entre parenthèses pour les utilisateurs avancés).
- **Inchangé** : les 8 questions en une salve, le format du profil, la shortlist de 3 à 5,
  le plan 30 jours, la règle « profil hors du repo ». Taille visée ~13 000 caractères.

## 8. Guide et documentation

### `DEMARRER.md` (racine du repo)

Porte d'entrée des débutants jusqu'à la page waelan.be (partie 2).

1. **C'est quoi ?** — trois lignes : « Tu gardes ton IA, on lui apprend la Belgique. »
2. **Tu utilises quelle IA ?** — quatre sections (Claude, ChatGPT, Gemini, Autre IA), 3 à 5
   étapes chacune, libellés de menus exacts, liens de téléchargement directs
   `https://github.com/sailwaelan-dotcom/the-agency/releases/latest/download/<fichier>`.
   Le **texte des instructions** et la **phrase à taper** sont dans des blocs de code
   (bouton copier de GitHub) : le débutant n'ouvre aucun fichier. Pour Claude : « télécharge
   le ZIP et ne l'ouvre pas ».
3. **Ce que tu vas obtenir, et comment le garder** — profil, 3 à 5 priorités, plan
   30 jours ; où coller le profil selon son IA (section 4).
4. **Ça ne marche pas ?** — 2 ou 3 cas par IA :
   - menu Skills absent → activer l'exécution de code ;
   - **Mac** : Safari a ouvert le ZIP tout seul → clic droit sur le dossier › Compresser,
     puis importer le ZIP obtenu ;
   - quota d'envois atteint → mode « Autre IA » avec le seul fichier d'accueil ;
   - l'IA ignore les fiches → « Suis le fichier the-agency-accueil.md ».
5. **Tes données** — The Agency ne collecte rien (aucun serveur) ; ne pas coller de
   données personnelles de clients ni de codes bancaires dans une IA.
6. **Important** — information générale datée, à faire valider par un professionnel agréé.
7. **Besoin d'un coup de main ?** — waelan.be et le rendez-vous de 15 minutes.
8. **Écrans vérifiés le AAAA-MM-JJ** — ligne mise à jour à chaque recette.

Contraintes :

- pas de captures d'écran en v1 ;
- libellés de menus rédigés d'après l'aide officielle de chaque IA, puis corrigés à la
  recette (section 10) ;
- **jargon interdit** (mots entiers, casse ignorée) : `harness`, `MCP`, `repo`, `CLI`,
  `TDD`, `frontmatter`, `YAML`, `JSON`, `commit`, `workflow` ;
- le mot « Skills » n'apparaît que là où l'interface de Claude l'impose, expliqué en une
  phrase.

### README, AGENTS, CONTRIBUTING, CHANGELOG

- **README** : bandeau sous le titre — « **Pas informaticien ?** 👉 [Commence ici](DEMARRER.md),
  5 minutes, gratuit » ; la section « Démarrage Rapide & Installation Zéro-Friction »
  devient « Installation avancée (Windows, Claude Desktop, Cursor, Claude Code) » et reçoit
  le lien vers la page des releases. Le bandeau n'introduit aucun compteur
  (`check_doc_sync`).
- **AGENTS.md** : `kit/`, `scripts/build_kit.py` et `DEMARRER.md` dans « Ce que tu trouves
  ici ».
- **CONTRIBUTING.md** : une ligne — modifier un skill met le kit à jour automatiquement ;
  `kit/` est la source du skill d'aiguillage.
- **agency-doc-keeper** : un item de checklist — kit reconstruit sans erreur et écrans de
  `DEMARRER.md` revérifiés avant chaque release.
- **CHANGELOG** : entrée « Ajouté — kit débutant multi-IA ».

## 9. Publication

- **`ci.yml`** : étape « Construire le kit » (`python scripts/build_kit.py`) avant les
  tests.
- **Nouveau `release-kit.yml`** : déclenché par `release: published` (la release existe
  forcément) et `workflow_dispatch` (artefact seul). Il construit le kit avec
  `--version "$GITHUB_REF_NAME"` et l'attache à la release (`gh release upload … --clobber`,
  permission `contents: write`). `build-exe.yml` ne change pas.
- **Liens stables** : `releases/latest/download/<fichier>` pointe toujours vers la
  dernière release.
- **v1.1.0** : les liens du guide ne fonctionnent qu'une fois une release contenant le kit
  publiée. La partie 1 se termine par la release v1.1.0, **poussée uniquement avec l'accord
  explicite du mainteneur**.

## 10. Tests et recette

### Tests automatiques — `tests/test_kit.py`

Écrits avant le code, exécutables en direct et sous pytest (motif `tdd_common.check`) :

1. Les 4 fichiers sont produits.
2. Le ZIP a un seul dossier racine `the-agency/` et un seul `SKILL.md`, qui passe
   `validate_skills.validate_skill()`.
3. Les 20 fiches sont présentes (20 dans le ZIP ; `activate-agency` dans l'accueil et 19
   dans les fiches) et les deux skills de maintenance sont absents partout.
4. Instructions ≤ 1 500 caractères, contenant « Active l'agence » et l'avertissement.
5. L'accueil contient les 8 thèmes de l'interview (liste de `test_vague5_tdd.py`), le mode
   conversation et le sommaire complet.
6. Deux fabrications donnent des fichiers identiques (sha256).
7. Le scan anti-leak (`security_scan`) ne trouve rien de bloquant dans les 4 fichiers.
8. Chaque lien `releases/latest/download/<fichier>` de `DEMARRER.md` désigne un fichier
   produit par le kit.
9. `DEMARRER.md` ne contient aucun mot de la liste de jargon interdit (section 8).
10. Le bloc d'instructions de `DEMARRER.md` est identique, au caractère près, à
    `kit/instructions.txt`.

`tests/test_vague5_tdd.py` gagne une famille « mode conversation et débutant » (profil
collé ou présent dans les Instructions, bloc à copier avec l'endroit où le coller, aucune
consigne de création de fichier en mode conversation, « je ne sais pas » → « à
confirmer », handoff en langage courant).

### Recette manuelle (mainteneur, avant la release)

Avec un profil fictif, sur les forfaits **gratuits** de Claude, ChatGPT et Gemini, puis
une autre IA :

- [ ] dérouler le parcours de `DEMARRER.md` pas à pas, chronomètre en main (< 10 min) ;
- [ ] relever les libellés exacts des menus et corriger le guide ;
- [ ] vérifier que le plan personnalisé et la phrase de handoff sortent bien ;
- [ ] coller le profil là où l'IA l'indique et vérifier qu'une deuxième conversation
      repart bien de ce profil ;
- [ ] si possible, importer le ZIP depuis un Mac avec Safari ;
- [ ] mettre à jour la ligne « Écrans vérifiés le … ».

## 11. Hors périmètre (parties suivantes)

- **Partie 2** : page dédiée sur waelan.be, Gem public partagé par lien, captures d'écran
  et vidéo.
- **Partie 3** : nettoyage de l'exe — liaison des skills en mode gelé, facture de démo
  codée en dur (`agency/menu.py`), version 2.0.0 d'`installer.iss` contre v1.0.0 publiée,
  rôle d'outil hors ligne optionnel.
- **Partie 4 (éventuelle)** : assistant hébergé en démo limitée à l'accueil.
- Versions néerlandaise et anglaise du kit et du guide.

## 12. Risques

| Risque | Parade |
|---|---|
| Les interfaces des IA changent (menus, quotas) | Libellés relevés à la recette, ligne « Écrans vérifiés le », item de checklist `agency-doc-keeper` |
| Limite réelle des instructions de Gem inconnue | Instructions ≤ 1 500 caractères, tout le reste dans les fichiers ; si le profil n'y tient pas, il se recolle en début de conversation |
| Infos ChatGPT et Le Chat de sources secondaires | Revérifiées à la recette avant publication |
| Recherche documentaire imparfaite dans les Projets ChatGPT | Règle 2 des instructions : sommaire d'abord, puis la fiche par son nom |
| Description large du skill Claude qui se déclenche trop souvent | Ancrage « en Belgique » ; skill installé volontairement pour cet usage |
| Gros fichier de fiches sur un forfait gratuit | Le premier résultat ne dépend que de l'accueil |

## 13. Ordre de mise en œuvre

Commits sur `main`, par lots cohérents, aucun push sans accord :

1. `activate-agency` 1.1.0 (tests vague 5 étendus, puis skill).
2. Kit : `tests/test_kit.py`, puis `kit/` et `scripts/build_kit.py`.
3. CI : étape dans `ci.yml`, workflow `release-kit.yml`.
4. Documentation : `DEMARRER.md`, README, AGENTS, CONTRIBUTING, `agency-doc-keeper`,
   CHANGELOG, rituel doc (`build_index.py`, `check_doc_sync.py`).
5. Recette manuelle, puis release v1.1.0 avec accord.

## Sources (septembre 2026)

- [Claude Help Center — Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
- [ChatGPT Skills — disponibilité par forfait](https://www.aiagentslibrary.com/blog/chatgpt-skills-availability/)
- [GPT personnalisés 2026 — limites et retrait](https://www.ai-toolbox.co/chatgpt-management-and-productivity/how-to-create-custom-gpts-walkthrough-2026)
- [Projets ChatGPT — limite des instructions](https://www.mywritingtwin.com/blog/chatgpt-projects-complete-guide)
- [Projets ChatGPT — fichiers par forfait](https://www.fileuploadgpt.com/blog/chatgpt-projects-file-limit)
- [ChatGPT gratuit — envois de fichiers par jour](https://www.fileuploadgpt.com/blog/chatgpt-file-upload-limit-free-plan)
- [Google — partage des Gems](https://blog.google/products/gemini/sharing-gems/)
- [Gems — forfait gratuit et fichiers](https://geotoolbox.ai/blog/gemini-gems)
- [Gems — limite des instructions](https://gemilab.net/en/articles/gemini-basics/gemini-gems-custom-instructions-troubleshooting)
- [Le Chat — forfait gratuit](https://costbench.com/software/ai-chatbots/mistral/free-plan/)
