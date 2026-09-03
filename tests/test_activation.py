#!/usr/bin/env python3
"""Auto-test d'activation sémantique — vérifie que chaque scénario de
tests/ACTIVATION.md (tableau du Test 1 : skill attendu + requêtes utilisateur)
est un déclencheur plausible pour la `description` du skill attendu.

Heuristique déterministe :
1. Termes saillants de la requête = mots de plus de 4 caractères, normalisés
   (minuscules, accents supprimés, élisions l'/d'/qu'… retirées), hors stopwords.
2. Couverture = fraction de ces termes retrouvés dans le « champ lexical » du skill :
   frontmatter `description` + `metadata.tags` + section « When to Use »
   (ACTIVATION.md précise que ses requêtes sont issues de cette section).
   Un terme matche s'il apparaît tel quel ou partage un préfixe d'au moins
   4 caractères avec un mot du champ lexical (variantes morphologiques simples).
3. Seuil : couverture >= 1/3 pour chaque scénario.
4. Collision : aucun autre skill ne doit obtenir un score STRICTEMENT supérieur
   au skill attendu sur la même requête.
5. Cas limites : ACTIVATION.md ne documente actuellement aucun scénario négatif
   (requête qui NE doit PAS déclencher un skill) ; le parser ci-dessous les
   détecterait (marqueur « NE doit PAS ») si le fichier en ajoutait.

Usage : python tests/test_activation.py  → exit 0 si tout passe.
"""
import re
import sys
import unicodedata
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"
ACTIVATION_MD = REPO_ROOT / "tests" / "ACTIVATION.md"

SEUIL_COUVERTURE = 1 / 3

FAILURES: list[str] = []

# Stopwords français courants + verbes trop génériques pour discriminer un skill.
STOPWORDS = {
    "alors", "aucun", "aucune", "aussi", "autre", "avant", "avec", "avoir",
    "bon", "car", "cela", "cette", "ces", "ceux", "chaque", "comme", "comment",
    "combien", "dans", "des", "elle", "elles", "encore", "entre", "est",
    "être", "fait", "faire", "faut", "ils", "juste", "leur", "leurs", "lors",
    "mais", "même", "merci", "moins", "monsieur", "nous", "notre", "ont",
    "par", "pas", "pendant", "peu", "plus", "pour", "pourquoi", "quand",
    "quel", "quelle", "quels", "quelles", "qui", "quoi", "sans", "ses",
    "soi", "sont", "sous", "sur", "tandis", "tel", "tels", "tous", "toute",
    "toutes", "très", "trop", "une", "vos", "votre", "vous", "veux", "veut",
    "dois", "peux", "doit", "peut", "passe", "mettre", "mets", "tient",
    "route", "chose", "choses", "chez", "dont", "aux", "son",
    # formes élidées fréquentes dans les requêtes
    "cest", "quest", "davoir", "quil", "quon", "madresse", "jai",
    # verbes trop génériques pour être discriminant d'un skill
    "viens", "lancer", "savoir", "envoyer", "demande", "cherche", "corrige",
    "calcule", "parle", "ressemble", "ressemblent", "transformer",
}


def normaliser(texte: str) -> str:
    """Minuscules + suppression des accents (déterministe)."""
    texte = texte.lower().replace("’", "'")
    decomp = unicodedata.normalize("NFD", texte)
    return "".join(c for c in decomp if unicodedata.category(c) != "Mn")


def termes_saillants(requete: str) -> list[str]:
    """Mots de plus de 4 caractères, hors stopwords, élisions retirées."""
    termes = []
    for mot in re.findall(r"[a-z0-9']+", normaliser(requete)):
        mot = re.sub(r"^(?:l|d|qu|j|m|n|s|c|t)'", "", mot).strip("'")
        if len(mot) > 4 and mot not in STOPWORDS:
            termes.append(mot)
    return termes


def prefixe_commun(a: str, b: str) -> int:
    n = 0
    for ca, cb in zip(a, b):
        if ca != cb:
            break
        n += 1
    return n


def terme_matche(terme: str, champ: str, mots_champ: set[str]) -> bool:
    """Match exact (sous-chaîne) ou préfixe commun >= 4 caractères."""
    if terme in champ:
        return True
    return any(
        len(mot) >= 4 and prefixe_commun(terme, mot) >= 4 for mot in mots_champ
    )


def parser_scenarios() -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """Extrait du tableau du Test 1 les (skill attendu, requête) positifs,
    et les éventuels cas limites négatifs (marqueur « NE doit PAS »)."""
    positifs: list[tuple[str, str]] = []
    negatifs: list[tuple[str, str]] = []
    for ligne in ACTIVATION_MD.read_text(encoding="utf-8").splitlines():
        if ligne.startswith("| `"):
            cellules = [c.strip() for c in ligne.strip().strip("|").split("|")]
            skill = cellules[0].strip("`")
            for req in cellules[1:]:
                req = req.strip("«» ").strip()
                if req:
                    positifs.append((skill, req))
        elif re.search(r"ne\s+doit\s+pas", ligne, re.I):
            m = re.search(r"`([a-z0-9-]+)`.*[«\"]([^»\"]+)[»\"]", ligne, re.I)
            if m:
                negatifs.append((m.group(1), m.group(2).strip()))
    return positifs, negatifs


def champ_lexical(skill: str) -> str:
    """description + tags metadata + section « When to Use », normalisés."""
    skill_md = SKILLS_DIR / skill / "SKILL.md"
    brut = skill_md.read_text(encoding="utf-8")
    fin_fm = brut.find("\n---", 3)
    if fin_fm == -1:
        raise ValueError(f"{skill_md}: frontmatter introuvable")
    fm = yaml.safe_load(brut[3:fin_fm])
    corps = brut[fin_fm + 4 :]
    m = re.search(r"## When to Use\n(.*?)(?=\n## |\Z)", corps, re.S)
    when_to_use = m.group(1) if m else ""
    texte = " ".join([
        fm.get("description", ""),
        " ".join(fm.get("metadata", {}).get("tags", [])),
        when_to_use,
    ])
    return normaliser(texte)


def score(terme_liste: list[str], champ: str, mots_champ: set[str]) -> float:
    if not terme_liste:
        return 1.0
    hits = sum(1 for t in terme_liste if terme_matche(t, champ, mots_champ))
    return hits / len(terme_liste)


def main() -> int:
    positifs, negatifs = parser_scenarios()
    if not positifs:
        print("ÉCHEC: aucun scénario parsé depuis tests/ACTIVATION.md")
        return 1

    tous_skills = sorted(
        d.name for d in SKILLS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith("_")
    )
    champs = {s: champ_lexical(s) for s in tous_skills}
    mots_champs = {s: set(re.findall(r"[a-z0-9]+", champs[s])) for s in tous_skills}

    for skill, requete in positifs:
        # 1. Le skill attendu doit exister dans le repo.
        if skill not in champs:
            FAILURES.append(f"FAIL skill-inexistant: '{skill}' absent de .agents/skills/")
            continue
        termes = termes_saillants(requete)
        # 2. Couverture minimale de la requête par le champ lexical du skill.
        couverture = score(termes, champs[skill], mots_champs[skill])
        if couverture < SEUIL_COUVERTURE:
            FAILURES.append(
                f"FAIL couverture {couverture:.0%} < {SEUIL_COUVERTURE:.0%} "
                f"[{skill}] « {requete} »"
            )
        # 3. Pas de collision : aucun autre skill ne score strictement mieux.
        for autre in tous_skills:
            if autre == skill:
                continue
            if score(termes, champs[autre], mots_champs[autre]) > couverture:
                FAILURES.append(
                    f"FAIL collision [{skill}] « {requete} » : "
                    f"'{autre}' score mieux"
                )

    # 4. Cas limites négatifs (aucun documenté actuellement dans ACTIVATION.md).
    for skill, requete in negatifs:
        if skill not in champs:
            continue
        termes = termes_saillants(requete)
        if score(termes, champs[skill], mots_champs[skill]) >= SEUIL_COUVERTURE:
            FAILURES.append(
                f"FAIL cas-limite [{skill}] « {requete} » déclenche à tort"
            )

    if FAILURES:
        print("ÉCHECS:")
        for f in FAILURES:
            print(f"  {f}")
        return 1
    print(
        f"OK: {len(positifs)}/{len(positifs)} scénarios d'activation couverts "
        f"({len(tous_skills)} skills, {len(negatifs)} cas limite négatif)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
