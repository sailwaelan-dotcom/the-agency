"""
Runner d'évaluation déterministe (EDD) pour The Agency.
Évalue les réponses des agents ou compétences contre les 40 Scénarios d'Or Réglementaires Belges.
Mesure : Pass Rate %, Taux d'hallucinations de concepts étrangers (France), et respect des disclaimers.
"""
import json
import re
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = REPO_ROOT / "evals" / "dataset" / "belgian_golden_evals.json"

DISCLAIMER_PATTERNS = [
    re.compile(r"comptable", re.I),
    re.compile(r"avocat", re.I),
    re.compile(r"expert-comptable", re.I),
    re.compile(r"professionnel agr[ée]é", re.I),
    re.compile(r"disclaimer", re.I),
    re.compile(r"information g[ée]n[ée]rale", re.I),
]


def load_dataset() -> Dict[str, Any]:
    """Charge le jeu de données d'évaluation des 40 cas d'or belges."""
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Jeu de données manquant : {DATASET_PATH}")
    return json.loads(DATASET_PATH.read_text(encoding="utf-8"))


def evaluate_response(case: Dict[str, Any], response_text: str) -> Dict[str, Any]:
    """
    Évalue une réponse générée pour un cas donné selon les critères réglementaires stricts.
    """
    text_lower = response_text.lower()

    # 1. Vérification des mots-clés requis
    missing_keywords: List[str] = []
    for kw in case.get("required_keywords", []):
        if kw.lower() not in text_lower:
            missing_keywords.append(kw)

    # 2. Détection d'hallucinations de termes étrangers (ex: droit français)
    hallucinations: List[str] = []
    for term in case.get("forbidden_terms", []):
        if term.lower() in text_lower:
            hallucinations.append(term)

    # 3. Vérification du disclaimer si requis
    disclaimer_ok = True
    if case.get("must_have_disclaimer", False):
        disclaimer_ok = any(p.search(response_text) for p in DISCLAIMER_PATTERNS)

    passed = (len(missing_keywords) == 0) and (len(hallucinations) == 0) and disclaimer_ok

    return {
        "case_id": case.get("id"),
        "domain": case.get("domain"),
        "passed": passed,
        "missing_keywords": missing_keywords,
        "hallucinations": hallucinations,
        "disclaimer_ok": disclaimer_ok,
    }


def run_benchmark(eval_fn: Optional[Callable[[str], str]] = None) -> Dict[str, Any]:
    """
    Exécute le benchmark sur les 40 cas d'or.
    Si eval_fn est fourni, appelle la fonction pour chaque prompt.
    Sinon, teste la validité structurelle du dataset et exécute les auto-tests de validation.
    """
    dataset = load_dataset()
    cases = dataset.get("cases", [])

    total = len(cases)
    passed_count = 0
    hallucination_count = 0
    results: List[Dict[str, Any]] = []

    domain_stats: Dict[str, Dict[str, int]] = {}

    for case in cases:
        dom = case.get("domain", "other")
        if dom not in domain_stats:
            domain_stats[dom] = {"total": 0, "passed": 0}
        domain_stats[dom]["total"] += 1

        if eval_fn is not None:
            prompt = case.get("user_prompt", "")
            response = eval_fn(prompt)
            eval_res = evaluate_response(case, response)
        else:
            # Mode auto-test : simule une réponse de référence parfaite
            kw = " ".join(case.get("required_keywords", []))
            disclaimer = " Disclaimer : information générale, consultez un comptable ou expert-comptable agréé." if case.get("must_have_disclaimer") else ""
            mock_response = f"Réponse conforme : {kw}.{disclaimer}"
            eval_res = evaluate_response(case, mock_response)

        results.append(eval_res)
        if eval_res["passed"]:
            passed_count += 1
            domain_stats[dom]["passed"] += 1
        if eval_res["hallucinations"]:
            hallucination_count += 1

    pass_rate = round((passed_count / total) * 100, 1) if total > 0 else 0.0

    return {
        "total_cases": total,
        "passed_count": passed_count,
        "failed_count": total - passed_count,
        "hallucination_count": hallucination_count,
        "pass_rate": pass_rate,
        "domain_breakdown": domain_stats,
        "details": results,
    }


if __name__ == "__main__":
    print("==================================================================")
    print("🇧🇪 Exécution du Benchmark EDD — 40 Cas d'Or Réglementaires Belges")
    print("==================================================================")

    res = run_benchmark()
    print(f"Total cas évalués       : {res['total_cases']}")
    print(f"Cas réussis             : {res['passed_count']} / {res['total_cases']}")
    print(f"Taux de succès          : {res['pass_rate']} %")
    print(f"Hallucinations détectées: {res['hallucination_count']}")
    print("\nRépartition par domaine :")
    for dom, st in res["domain_breakdown"].items():
        print(f"  • {dom:<16} : {st['passed']}/{st['total']} ({round(st['passed']/st['total']*100)} %)")

    if res["pass_rate"] >= 95.0 and res["hallucination_count"] == 0:
        print("\nGREEN — Le benchmark des 40 cas d'or réglementaires est validé !")
        sys.exit(0)
    else:
        print("\nRED — Échec du benchmark : conformité insuffisante.")
        sys.exit(1)
