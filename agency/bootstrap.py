"""
Bootstrap & initialisation d'environnement pour The Agency.
Centralise la configuration UTF-8 Windows, la résolution des bundles PyInstaller
et la configuration de sys.path sans duplication.
"""
import sys
from pathlib import Path
from typing import Tuple


def setup_environment() -> Tuple[Path, Path]:
    """
    Initialise l'environnement d'exécution :
    - Reconfigure stdout/stderr en UTF-8 sous Windows.
    - Détermine BUNDLE_DIR (dossier des sources ou sys._MEIPASS) et APP_DIR (dossier de l'exécutable).
    - Configure sys.path pour importer les modules de The Agency et du serveur MCP.

    Retourne :
        Tuple[Path, Path]: (BUNDLE_DIR, APP_DIR)
    """
    # 1. Encodage UTF-8 pour Windows Console
    if sys.platform == "win32":
        try:
            if hasattr(sys.stdout, "reconfigure"):
                sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            if hasattr(sys.stderr, "reconfigure"):
                sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    # 2. Résolution des répertoires d'exécution
    if getattr(sys, "frozen", False):
        bundle_dir = Path(sys._MEIPASS)
        app_dir = Path(sys.executable).resolve().parent
    else:
        bundle_dir = Path(__file__).resolve().parent.parent
        app_dir = bundle_dir

    # 3. Injection sys.path
    servers_dir = bundle_dir / "mcp" / "servers"
    if str(servers_dir) not in sys.path:
        sys.path.insert(0, str(servers_dir))
    if str(bundle_dir) not in sys.path:
        sys.path.insert(0, str(bundle_dir))

    return bundle_dir, app_dir
