"""
Installateur & Auto-Configurateur Zéro-Friction pour The Agency.
Configure automatiquement le serveur MCP 'agency-be-mcp' dans :
- Claude Desktop (Windows, macOS, Linux)
- Cursor (.cursor/mcp.json)
- Claude Code (.claude/mcp.json)
Sans écraser les configurations existantes de l'utilisateur.
"""
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from agency.bootstrap import setup_environment

REPO_ROOT, APP_DIR = setup_environment()
# En mode gelé, __file__ vit dans le dossier temporaire _MEIPASS (détruit à la sortie) :
# les configs "workspace" (Cursor, Claude Code) doivent être écrites à côté de l'exe pour persister.
WORKSPACE_BASE = APP_DIR if getattr(sys, "frozen", False) else REPO_ROOT
SERVER_PY = REPO_ROOT / "mcp" / "servers" / "agency_be" / "server.py"


def get_claude_desktop_config_path() -> Optional[Path]:
    """Retourne le chemin standard du fichier claude_desktop_config.json selon l'OS."""
    system = platform.system()
    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / "Claude" / "claude_desktop_config.json"
    elif system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif system == "Linux":
        return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"
    return None


def get_cursor_config_path() -> Path:
    """Retourne le chemin de configuration MCP pour Cursor dans le workspace."""
    return WORKSPACE_BASE / ".cursor" / "mcp.json"


def get_claude_code_config_path() -> Path:
    """Retourne le chemin de configuration MCP pour Claude Code dans le workspace."""
    return WORKSPACE_BASE / ".claude" / "mcp.json"


def build_mcp_server_config() -> Dict[str, Any]:
    """Génère la définition standard du serveur MCP agency-be-mcp."""
    if getattr(sys, "frozen", False):
        # L'exe gelé expose le serveur stdio via sa route CLI 'mcp' (voir agency/cli.py) ;
        # un chemin vers server.py serait ici un chemin temporaire détruit à la sortie.
        return {
            "command": sys.executable,
            "args": ["mcp"],
            "env": {"PYTHONIOENCODING": "utf-8"},
        }
    py_exec = sys.executable
    pythonpath = str(REPO_ROOT / "mcp" / "servers") + os.pathsep + str(REPO_ROOT)
    return {
        "command": py_exec,
        "args": [str(SERVER_PY)],
        "env": {
            "PYTHONPATH": pythonpath,
            "PYTHONIOENCODING": "utf-8",
        },
    }


def inject_mcp_server_into_file(config_file: Path) -> Tuple[bool, str]:
    """
    Injecte ou met à jour 'agency-be-mcp' dans un fichier de configuration JSON.
    Préserve tous les autres serveurs MCP déjà configurés.
    """
    config_data: Dict[str, Any] = {}
    config_file.parent.mkdir(parents=True, exist_ok=True)

    if config_file.exists():
        try:
            content = config_file.read_text(encoding="utf-8").strip()
            if content:
                config_data = json.loads(content)
        except Exception as e:
            return False, f"Impossible de lire le fichier existant {config_file} : {e}"

    if "mcpServers" not in config_data or not isinstance(config_data["mcpServers"], dict):
        config_data["mcpServers"] = {}

    config_data["mcpServers"]["agency-be-mcp"] = build_mcp_server_config()

    try:
        config_file.write_text(json.dumps(config_data, indent=2, ensure_ascii=False), encoding="utf-8")
        return True, "Injecté avec succès"
    except Exception as e:
        return False, f"Erreur lors de l'écriture de {config_file} : {e}"


def run_link_skills() -> bool:
    """Exécute les adaptateurs de liaison de skills selon l'OS."""
    system = platform.system()
    try:
        if system == "Windows":
            ps_script = REPO_ROOT / "adapters" / "link-skills.ps1"
            if ps_script.exists():
                res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps_script)], capture_output=True)
                return res.returncode == 0
        else:
            sh_script = REPO_ROOT / "adapters" / "link-skills.sh"
            if sh_script.exists():
                res = subprocess.run(["bash", str(sh_script)], capture_output=True)
                return res.returncode == 0
    except Exception:
        pass
    return False


def create_desktop_shortcut() -> Tuple[bool, str]:
    """Crée un raccourci The Agency sur le Bureau de l'utilisateur."""
    if platform.system() != "Windows":
        return False, "Non supporté hors Windows"
    try:
        desktop = Path.home() / "Desktop"
        if not desktop.exists():
            userprofile = os.environ.get("USERPROFILE")
            if userprofile:
                desktop = Path(userprofile) / "Desktop"
        if not desktop.exists():
            return False, "Dossier Bureau introuvable"

        if getattr(sys, "frozen", False):
            target = sys.executable
        else:
            exe_target = REPO_ROOT / "dist" / "TheAgency.exe"
            target = str(exe_target) if exe_target.exists() else str(REPO_ROOT / "Lancer_The_Agency.cmd")

        shortcut = desktop / "The Agency.cmd"
        content = f"""@echo off\ntitle The Agency - Assistant Solopreneur Belge\nchcp 65001 > nul\n"{target}"\n"""
        shortcut.write_text(content, encoding="utf-8")
        return True, str(shortcut)
    except Exception as e:
        return False, str(e)


def run_full_installation(interactive: bool = True) -> Dict[str, Any]:
    """Exécute l'onboarding complet sans friction."""
    if interactive:
        print("==================================================================")
        print("🇧🇪 The Agency — Assistant d'Installation & Auto-Configuration")
        print("==================================================================")
        print("Détection et configuration automatique de vos applications IA...\n")

    results: Dict[str, Any] = {}

    # 1. Claude Desktop
    cd_path = get_claude_desktop_config_path()
    if cd_path:
        ok, msg = inject_mcp_server_into_file(cd_path)
        results["claude_desktop"] = {"path": str(cd_path), "success": ok, "message": msg}
        if interactive:
            status = "✓ Activé" if ok else "✗ Échec"
            print(f"  [{status}] Claude Desktop : {cd_path}")

    # 2. Cursor
    cursor_path = get_cursor_config_path()
    ok_c, msg_c = inject_mcp_server_into_file(cursor_path)
    results["cursor"] = {"path": str(cursor_path), "success": ok_c, "message": msg_c}
    if interactive:
        status = "✓ Activé" if ok_c else "✗ Échec"
        print(f"  [{status}] Cursor IDE     : {cursor_path}")

    # 3. Claude Code
    cc_path = get_claude_code_config_path()
    ok_cc, msg_cc = inject_mcp_server_into_file(cc_path)
    results["claude_code"] = {"path": str(cc_path), "success": ok_cc, "message": msg_cc}
    if interactive:
        status = "✓ Activé" if ok_cc else "✗ Échec"
        print(f"  [{status}] Claude Code    : {cc_path}")

    # 4. Liaison des skills
    skills_linked = run_link_skills()
    results["skills_linked"] = skills_linked
    if interactive:
        status_s = "✓ Activé" if skills_linked else "✗ Échec (à exécuter via adapters/)"
        print(f"  [{status_s}] Liaison des 22 compétences belges (adapters/link-skills)")

    # 5. Initialisation locale du coffre RGPD et de la base KBO
    try:
        sys.path.insert(0, str(REPO_ROOT / "mcp" / "servers"))
        sys.path.insert(0, str(REPO_ROOT))
        from agency_be.tools.kbo_db import init_kbo_db
        from agency.vault import get_vault_dir
        init_kbo_db()
        get_vault_dir()
        results["local_services"] = True
        if interactive:
            print("  [✓ Activé] Base KBO hors-ligne & Coffre RGPD local (~/.agency/)")
    except Exception as e:
        results["local_services"] = False
        results["local_error"] = str(e)

    # 6. Raccourci Bureau (Windows)
    if platform.system() == "Windows":
        ok_sc, path_sc = create_desktop_shortcut()
        results["desktop_shortcut"] = {"success": ok_sc, "path": path_sc}
        if interactive and ok_sc:
            print(f"  [✓ Activé] Raccourci Bureau : {path_sc}")

    if interactive:
        print("\n🎉 Félicitations ! The Agency est prêt à l'emploi.")
        print("💡 Redémarrez Claude Desktop ou Cursor pour voir apparaître les 13 outils belges.\n")

    return results


if __name__ == "__main__":
    run_full_installation(interactive=True)
