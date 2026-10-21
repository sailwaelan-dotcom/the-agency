"""
Écriture atomique de fichiers texte : un fichier temporaire du même dossier (créé en 0600),
puis un renommage. Une erreur en cours d'écriture laisse l'ancien fichier intact.
"""
import os
import tempfile
from pathlib import Path


def write_text_atomic(path: Path, text: str) -> None:
    """Remplace le contenu de `path` par `text`, sans jamais laisser un fichier tronqué."""
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp_name, path)
    except BaseException:
        os.unlink(tmp_name)
        raise
