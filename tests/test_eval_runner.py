#!/usr/bin/env python3
"""
TDD Tests — Eval Runner & Golden Scenarios pour The Agency.
Vérifie la robustesse du moteur d'évaluation et la conformité des 40 cas d'or belges.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from evals.eval_runner import evaluate_response, load_dataset, run_benchmark


def test_golden_dataset_integrity():
    data = load_dataset()
    assert "cases" in data
    cases = data["cases"]
    assert len(cases) == 40, f"Attendu 40 cas, trouvé {len(cases)}"

    for c in cases:
        assert "id" in c
        assert "domain" in c
        assert "user_prompt" in c
        assert "required_keywords" in c
        assert isinstance(c["required_keywords"], list)
        assert len(c["required_keywords"]) >= 1


def test_evaluator_detects_hallucinations():
    case = {
        "id": "test_hallucination",
        "domain": "tva",
        "required_keywords": ["56bis"],
        "forbidden_terms": ["CGI 293 B", "Siret"],
        "must_have_disclaimer": False,
    }
    # Réponse avec hallucination d'un terme français
    bad_response = "En vertu de l'article 56bis et du CGI 293 B, vous êtes exonéré avec votre Siret."
    res = evaluate_response(case, bad_response)
    assert res["passed"] is False
    assert "CGI 293 B" in res["hallucinations"]
    assert "Siret" in res["hallucinations"]


def test_evaluator_requires_disclaimer():
    case = {
        "id": "test_disclaimer",
        "domain": "inasti",
        "required_keywords": ["20,5 %"],
        "forbidden_terms": [],
        "must_have_disclaimer": True,
    }
    # Réponse sans disclaimer
    no_disc_response = "Le taux de base est de 20,5 % du revenu net."
    res_fail = evaluate_response(case, no_disc_response)
    assert res_fail["passed"] is False
    assert res_fail["disclaimer_ok"] is False

    # Réponse avec disclaimer
    with_disc_response = "Le taux de base est de 20,5 % du revenu net. Disclaimer : consultez un expert-comptable agréé."
    res_pass = evaluate_response(case, with_disc_response)
    assert res_pass["passed"] is True
    assert res_pass["disclaimer_ok"] is True


def test_benchmark_suite_pass():
    res = run_benchmark()
    assert res["total_cases"] == 40
    assert res["passed_count"] == 40
    assert res["pass_rate"] == 100.0
    assert res["hallucination_count"] == 0


if __name__ == "__main__":
    tests = [
        test_golden_dataset_integrity,
        test_evaluator_detects_hallucinations,
        test_evaluator_requires_disclaimer,
        test_benchmark_suite_pass,
    ]
    failures = []
    print("Exécution des tests de l'Eval Runner...")
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
        except Exception as e:
            failures.append((t.__name__, str(e)))
            print(f"  ✗ {t.__name__}: {e}")

    if failures:
        print(f"\nRED — {len(failures)} test(s) en échec :")
        for name, err in failures:
            print(f"  - {name}: {err}")
        sys.exit(1)

    print(f"\nGREEN — Tous les {len(tests)} tests de l'Eval Runner passent !")
    sys.exit(0)
