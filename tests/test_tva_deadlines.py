#!/usr/bin/env python3
"""Régression — échéances TVA périodiques dans les contenus (skills, exemples, évals).

Règles SPF Finances vérifiées le 2026-09-15 (« La nouvelle chaîne TVA » §2 et §10.1,
calendrier TVA, page « Payer la TVA ») :
- trimestriel : dépôt et paiement au plus tard le 25 du mois qui suit le trimestre, sans report ;
- mensuel : le 20 du mois suivant, reporté au jour ouvrable suivant ;
- plus d'acomptes pour les trimestriels.

Exécutable en direct (`python tests/test_tva_deadlines.py`, mode du CI « gates ») et sous pytest.
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"
EVALS_PATH = REPO_ROOT / "evals" / "dataset" / "belgian_golden_evals.json"

# « 20 » employé comme jour d'échéance
JOUR_20 = re.compile(r"\ble 20\b|\b20 (du mois|janvier|avril|juillet|octobre)\b", re.I)
PLUS_D_ACOMPTE = re.compile(r"plus d['’]acomptes?|ne paient plus|ne devez plus", re.I)

FAILURES: list[str] = []


def check(label: str, condition: bool, detail: str = "") -> None:
    if not condition:
        entry = f"FAIL {label}: {detail}"
        FAILURES.append(entry)
        # Sous pytest, un échec doit lever (le runner __main__ seul lit FAILURES)
        if "pytest" in sys.modules:
            raise AssertionError(entry)


def blocs(path: Path):
    """(n° de ligne, texte) : chaque ligne de tableau, et chaque paragraphe (lignes non vides jointes)."""
    courant: list[str] = []
    debut = 0
    for n, ligne in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if ligne.lstrip("> ").startswith("|"):
            if courant:
                yield debut, " ".join(courant)
                courant = []
            yield n, ligne
        elif ligne.strip():
            if not courant:
                debut = n
            courant.append(ligne.strip())
        elif courant:
            yield debut, " ".join(courant)
            courant = []
    if courant:
        yield debut, " ".join(courant)


def skill_md(nom: str) -> Path:
    return SKILLS_DIR / nom / "SKILL.md"


def test_aucune_echeance_trimestrielle_au_20():
    fichiers = sorted(SKILLS_DIR.glob("*/SKILL.md")) + sorted((REPO_ROOT / "examples").glob("*.md"))
    fautes = [
        f"{path.relative_to(REPO_ROOT).as_posix()}:{n}: {bloc[:80]}"
        for path in fichiers
        for n, bloc in blocs(path)
        if re.search(r"trimestr", bloc, re.I) and JOUR_20.search(bloc)
        and "25" not in bloc and not re.search(r"mensuel", bloc, re.I)
    ]
    check("trimestriel-au-20", not fautes, "\n  " + "\n  ".join(fautes))


def test_evals_trimestre_au_25():
    cases = json.loads(EVALS_PATH.read_text(encoding="utf-8"))["cases"]
    fautifs = [c["id"] for c in cases
               if re.search(r"trimestre", c["user_prompt"], re.I)
               and any(JOUR_20.search(k) for k in c["required_keywords"])]
    check("evals-trimestre-au-20", not fautifs, f"cas exigeant un « 20 » pour un trimestre : {fautifs}")


def test_be_admin_deadlines_trimestres_au_25():
    contenu = skill_md("be-admin-deadlines").read_text(encoding="utf-8")
    for attendu in ("**T1 (jan-mars)** → 25 avril", "**T2 (avr-juin)** → 25 juillet",
                    "**T3 (juil-sept)** → 25 octobre", "**T4 (oct-déc)** → 25 janvier"):
        check(f"admin-deadlines-{attendu[2:4]}", attendu in contenu, f"« {attendu} » absent")
    check("admin-deadlines-sans-report", "aucun report" in contenu, "absence de report non signalée")


def test_be_accounting_basics_mensuel_20_trimestriel_25():
    contenu = skill_md("be-accounting-basics").read_text(encoding="utf-8")
    section = contenu.split("### TVA", 1)[1].split("\n### ", 1)[0]
    for attendu in ("**20 du mois suivant**", "**25 du mois suivant le trimestre**", "sans report"):
        check(f"accounting-basics-{attendu.strip('*')[:6]}", attendu in section,
              f"« {attendu} » absent de la section TVA")


def test_secretary_ops_mensuel_20_trimestriel_25():
    lignes = [l for l in skill_md("secretary-ops").read_text(encoding="utf-8").splitlines()
              if l.startswith("| Déclaration TVA")]
    check("secretary-ops-tva", len(lignes) == 1 and "le 20" in lignes[0] and "le 25" in lignes[0],
          f"lignes : {lignes}")


def test_pas_d_acompte_trimestriel_du():
    fautes = [
        f"{nom}:{n}: {bloc[:80]}"
        for nom in ("be-admin-deadlines", "be-accounting-basics")
        for n, bloc in blocs(skill_md(nom))
        if re.search(r"acompte", bloc, re.I) and re.search(r"décembre|trimestr", bloc, re.I)
        and not PLUS_D_ACOMPTE.search(bloc)
    ]
    check("acompte-trimestriel", not fautes, "\n  " + "\n  ".join(fautes))


TESTS = (test_aucune_echeance_trimestrielle_au_20, test_evals_trimestre_au_25,
         test_be_admin_deadlines_trimestres_au_25, test_be_accounting_basics_mensuel_20_trimestriel_25,
         test_secretary_ops_mensuel_20_trimestriel_25, test_pas_d_acompte_trimestriel_du)

if __name__ == "__main__":
    for test in TESTS:
        test()
    if FAILURES:
        print(f"RED — {len(FAILURES)} échec(s) :")
        for f in FAILURES:
            print(f"  {f}")
        sys.exit(1)
    print(f"GREEN — {len(TESTS)}/{len(TESTS)} tests échéances TVA passent")
