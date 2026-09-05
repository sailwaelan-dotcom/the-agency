"""
Helpers partagés des suites TDD « par vagues » (tests/test_vague*_tdd.py).

Ces suites doivent rester exécutables de deux façons :
- directement : `python tests/test_vague3_tdd.py` (mode du CI « gates », qui
  n'installe pas pytest) — chaque fichier boucle sur ses skills et agrège
  ses échecs dans sa liste FAILURES avant de sortir avec un code non nul ;
- sous pytest : chaque famille de tests est paramétrée par skill.
"""
try:
    import pytest
except ImportError:  # exécution directe sans pytest installé
    pytest = None


def check(label: str, condition: bool, detail: str = "") -> None:
    """Échoue bruyamment (AssertionError) : un échec silencieux serait un faux vert sous pytest."""
    if not condition:
        raise AssertionError(f"{label}: {detail}")


def parametrize_skills(arg_name: str, names):
    """Paramètre la famille de tests par skill si pytest est disponible, sinon no-op."""
    def deco(fn):
        if pytest is not None:
            return pytest.mark.parametrize(arg_name, list(names))(fn)
        return fn
    return deco
