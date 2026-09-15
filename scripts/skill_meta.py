"""
Valeurs « liste » du frontmatter des skills — The Agency.

La spécification agentskills.io définit `metadata` comme une table de chaînes vers chaînes :
les listes (`tags`, `related_skills`) s'écrivent donc en une chaîne séparée par des virgules,
ex. `tags: "finance, tax, be"`. Ce module est l'unique définition de ce découpage ; il est
partagé par validate_skills.py, build_index.py, check_related_links.py, check_doc_sync.py
et les tests.
"""


def split_list(value) -> list[str]:
    """« a, b, c » → ["a", "b", "c"] ; None ou "" → [] ; une liste YAML (ancien format) est rendue telle quelle."""
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [str(item).strip() for item in value if str(item).strip()]
    return [part.strip() for part in str(value).split(",") if part.strip()]
