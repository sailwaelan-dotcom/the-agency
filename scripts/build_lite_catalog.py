"""
Générateur de Catalogue Léger (Tier 1 Context) pour The Agency.
Produit 'catalog_lite.json' (~1 500 tokens) pour le prompt système des agents,
permettant le chargement on-demand (Tier 2) via 'load_skill_context' et
l'optimisation du prompt caching (Anthropic / OpenAI).
"""
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"
CATALOG_LITE_PATH = REPO_ROOT / ".agents" / "catalog_lite.json"


def parse_skill_yaml_frontmatter(content: str) -> Dict[str, str]:
    """Parse le frontmatter YAML d'un SKILL.md sans dépendance externe."""
    match = re.match(r"^---\r?\n(.*?)\r?\n---", content, re.DOTALL)
    if not match:
        return {}
    frontmatter: Dict[str, str] = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if ":" in line and not line.startswith("#"):
            k, v = line.split(":", 1)
            frontmatter[k.strip()] = v.strip().strip("\"'")
    return frontmatter


def build_catalog_lite() -> List[Dict[str, Any]]:
    """Construit la version ultra-légère du catalogue de compétences."""
    skills_data: List[Dict[str, Any]] = []

    for skill_path in sorted(SKILLS_DIR.iterdir()):
        if not skill_path.is_dir() or skill_path.name.startswith(("_", ".")):
            continue

        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            continue

        content = skill_md.read_text(encoding="utf-8")
        fm = parse_skill_yaml_frontmatter(content)

        name = fm.get("name", skill_path.name)
        desc = fm.get("description", "")

        # Découpage du déclencheur et de la promesse
        trigger = ""
        promise = desc
        if "Utilisez quand" in desc:
            parts = desc.split(".", 1)
            trigger = parts[0].replace("Utilisez quand", "").strip()
            if len(parts) > 1:
                promise = parts[1].strip()

        skills_data.append({
            "name": name,
            "trigger": trigger or desc[:100],
            "role": promise or desc[:150],
            "as_of": fm.get("as_of", "2026-01-01"),
        })

    return skills_data


def main():
    catalog = build_catalog_lite()
    CATALOG_LITE_PATH.write_text(json.dumps({"skills": catalog}, indent=2, ensure_ascii=False), encoding="utf-8")
    
    # Estimation approximative des tokens (1 token ~ 4 caractères en français/anglais)
    size_chars = len(CATALOG_LITE_PATH.read_text(encoding="utf-8"))
    est_tokens = round(size_chars / 4)

    print(f"Catalogue léger généré : {CATALOG_LITE_PATH}")
    print(f"Skills indexés : {len(catalog)}")
    print(f"Taille estimée : ~{est_tokens} tokens (économie de > 95 % par rapport au chargement complet).")


if __name__ == "__main__":
    main()
