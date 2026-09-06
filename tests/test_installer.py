"""
Tests unitaires pour l'installateur auto-configurant (install.py),
le module bootstrap et l'interface console TUI (agency/menu.py).
"""
import io
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from agency.bootstrap import setup_environment
from agency.menu import (
    prompt_float,
    menu_check_client,
    menu_inasti,
    menu_deadlines,
    menu_ubl,
    menu_vault,
    menu_create_shortcut,
)
from agency import cli as agency_cli
from install import (
    build_mcp_server_config,
    inject_mcp_server_into_file,
    get_claude_desktop_config_path,
    run_link_skills,
    create_desktop_shortcut,
    run_full_installation,
)
from build_exe import force_utf8_stdio  # noqa: E402


class _FakeCp1252Stream:
    """Console Windows cp1252 fidèle : lève UnicodeEncodeError sur ce qu'elle ne peut pas encoder
    (c'est exactement ce qui a fait échouer le build v1.0.0 sur le runner GitHub Actions)."""

    def __init__(self):
        self.encoding = "cp1252"
        self.reconfigure_kwargs = None

    def reconfigure(self, **kwargs):
        self.reconfigure_kwargs = kwargs
        self.encoding = kwargs.get("encoding", self.encoding)

    def write(self, text):
        text.encode(self.encoding)
        return len(text)


def test_print_emoji_sans_fix_echoue_sur_cp1252():
    """Contre-preuve : sur une console cp1252, imprimer le drapeau lève — c'est le bug v1.0.0."""
    out = _FakeCp1252Stream()
    with patch("sys.stdout", out), pytest.raises(UnicodeEncodeError):
        print("🇧🇪")


def test_force_utf8_stdio_reconfigure_cp1252():
    out, err = _FakeCp1252Stream(), _FakeCp1252Stream()
    with patch("sys.stdout", out), patch("sys.stderr", err):
        force_utf8_stdio()
        print("🇧🇪 Compilation")
    assert out.reconfigure_kwargs is not None
    assert out.reconfigure_kwargs.get("encoding") == "utf-8"
    assert err.reconfigure_kwargs.get("encoding") == "utf-8"


def test_force_utf8_stdio_tolerates_stream_sans_reconfigure():
    class _Bare:
        pass

    with patch("sys.stdout", _Bare()), patch("sys.stderr", _Bare()):
        force_utf8_stdio()  # ne doit pas lever


def test_bootstrap_setup_environment():
    bundle_dir, app_dir = setup_environment()
    assert bundle_dir.exists()
    assert app_dir.exists()
    assert str(bundle_dir) in sys.path
    print("  ✓ test_bootstrap_setup_environment")


def test_build_mcp_server_config():
    cfg = build_mcp_server_config()
    assert "command" in cfg
    assert "args" in cfg
    assert "server.py" in cfg["args"][0]
    assert "env" in cfg
    assert "PYTHONPATH" in cfg["env"]
    print("  ✓ test_build_mcp_server_config")


def test_inject_mcp_server_into_file_new_file():
    tmp_dir = Path(tempfile.mkdtemp(prefix="agency_test_install_"))
    try:
        config_file = tmp_dir / "claude_desktop_config.json"
        ok, msg = inject_mcp_server_into_file(config_file)
        assert ok is True
        assert config_file.exists()

        data = json.loads(config_file.read_text(encoding="utf-8"))
        assert "mcpServers" in data
        assert "agency-be-mcp" in data["mcpServers"]
        print("  ✓ test_inject_mcp_server_into_file_new_file")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def test_inject_mcp_server_preserve_existing_servers():
    tmp_dir = Path(tempfile.mkdtemp(prefix="agency_test_install_"))
    try:
        config_file = tmp_dir / "claude_desktop_config.json"
        # Fichier existant avec un autre serveur
        initial = {
            "mcpServers": {
                "mon-serveur-existant": {
                    "command": "node",
                    "args": ["index.js"]
                }
            }
        }
        config_file.write_text(json.dumps(initial), encoding="utf-8")

        ok, msg = inject_mcp_server_into_file(config_file)
        assert ok is True

        data = json.loads(config_file.read_text(encoding="utf-8"))
        # Le serveur existant DOIT être préservé
        assert "mon-serveur-existant" in data["mcpServers"]
        # Le serveur agency-be-mcp DOIT être ajouté
        assert "agency-be-mcp" in data["mcpServers"]
        print("  ✓ test_inject_mcp_server_preserve_existing_servers")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def test_claude_desktop_path_resolution():
    p = get_claude_desktop_config_path()
    assert p is not None
    assert "claude_desktop_config.json" in str(p)
    print("  ✓ test_claude_desktop_path_resolution")


def test_run_link_skills_mock():
    with patch("subprocess.run") as mock_sub:
        mock_sub.return_value.returncode = 0
        assert run_link_skills() is True

        mock_sub.return_value.returncode = 1
        assert run_link_skills() is False
    print("  ✓ test_run_link_skills_mock")


def test_create_desktop_shortcut():
    tmp_desktop = Path(tempfile.mkdtemp(prefix="agency_test_desktop_"))
    try:
        (tmp_desktop / "Desktop").mkdir()
        # platform.system est patché pour que la logique du raccourci soit
        # testable sur tous les OS (le CI gates tourne sur Ubuntu).
        with patch("install.platform.system", return_value="Windows"), \
             patch("pathlib.Path.home", return_value=tmp_desktop), \
             patch.dict(os.environ, {"USERPROFILE": str(tmp_desktop)}):
            ok, path_or_msg = create_desktop_shortcut()
            assert ok is True, path_or_msg
            assert Path(path_or_msg).exists()
    finally:
        shutil.rmtree(tmp_desktop, ignore_errors=True)
    print("  ✓ test_create_desktop_shortcut")


def test_create_desktop_shortcut_frozen_targets_exe():
    """En mode gelé, le raccourci doit cibler l'exe lui-même (jamais un fichier du dossier temporaire)."""
    tmp_desktop = Path(tempfile.mkdtemp(prefix="agency_test_desktop_frozen_"))
    try:
        (tmp_desktop / "Desktop").mkdir()
        exe_path = tmp_desktop / "TheAgency.exe"
        with patch("install.platform.system", return_value="Windows"), \
             patch("pathlib.Path.home", return_value=tmp_desktop), \
             patch.dict(os.environ, {"USERPROFILE": str(tmp_desktop)}), \
             patch("sys.frozen", True, create=True), \
             patch("sys.executable", str(exe_path)):
            ok, path_or_msg = create_desktop_shortcut()
            assert ok is True, path_or_msg
            content = Path(path_or_msg).read_text(encoding="utf-8")
            assert str(exe_path) in content
            assert "Lancer_The_Agency.cmd" not in content
    finally:
        shutil.rmtree(tmp_desktop, ignore_errors=True)
    print("  ✓ test_create_desktop_shortcut_frozen_targets_exe")


def test_build_mcp_server_config_frozen():
    """En mode gelé, la config MCP doit pointer vers l'exe + la route 'mcp' (jamais un chemin temporaire)."""
    with patch("sys.frozen", True, create=True), \
         patch("sys.executable", "C:/Dist/TheAgency.exe"):
        cfg = build_mcp_server_config()
        assert cfg["command"] == "C:/Dist/TheAgency.exe"
        assert cfg["args"] == ["mcp"]
        assert "server.py" not in json.dumps(cfg)
    print("  ✓ test_build_mcp_server_config_frozen")


def test_cli_mcp_route_runs_stdio_server():
    """La route 'mcp' du CLI doit lancer le serveur stdio (utilisé par la config MCP de l'exe gelé)."""
    with patch("sys.argv", ["TheAgency.exe", "mcp"]), \
         patch("agency_be.server.run_stdio_server") as srv:
        agency_cli.main()
        srv.assert_called_once()
    print("  ✓ test_cli_mcp_route_runs_stdio_server")


def test_menu_shortcut_delegates_to_install():
    """L'option [7] du menu délègue à install.create_desktop_shortcut (une seule implémentation)."""
    with patch("install.create_desktop_shortcut", return_value=(True, "C:/fake/The Agency.cmd")) as sc, \
         patch("sys.stdout", new=io.StringIO()) as out:
        menu_create_shortcut()
        sc.assert_called_once()
        assert "C:/fake/The Agency.cmd" in out.getvalue()
    print("  ✓ test_menu_shortcut_delegates_to_install")


def test_run_full_installation_non_interactive():
    tmp_dir = Path(tempfile.mkdtemp(prefix="agency_test_full_"))
    try:
        with patch("install.get_claude_desktop_config_path", return_value=tmp_dir / "claude.json"), \
             patch("install.get_cursor_config_path", return_value=tmp_dir / "cursor.json"), \
             patch("install.get_claude_code_config_path", return_value=tmp_dir / "cc.json"), \
             patch("install.run_link_skills", return_value=True):
            res = run_full_installation(interactive=False)
            assert res["claude_desktop"]["success"] is True
            assert res["cursor"]["success"] is True
            assert res["claude_code"]["success"] is True
            assert res["skills_linked"] is True
            assert res["local_services"] is True
        print("  ✓ test_run_full_installation_non_interactive")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def test_prompt_float_safety():
    # 1. Valeur par défaut si vide
    with patch("builtins.input", return_value=""):
        assert prompt_float("Test", 42.0) == 42.0

    # 2. Virgule francophone acceptée
    with patch("builtins.input", return_value="1500,50"):
        assert prompt_float("Test", 0.0) == 1500.50

    # 3. Entrée invalide puis valide
    with patch("builtins.input", side_effect=["invalid", "-10", "2500"]):
        assert prompt_float("Test", 0.0) == 2500.0
    print("  ✓ test_prompt_float_safety")


def test_menu_check_client():
    # Client valide
    with patch("builtins.input", return_value="0202.239.951"), patch("sys.stdout", new=io.StringIO()) as out:
        menu_check_client()
        txt = out.getvalue()
        assert "0202.239.951" in txt
        assert "BCE valide" in txt

    # Client invalide
    with patch("builtins.input", return_value="0202.239.950"), patch("sys.stdout", new=io.StringIO()) as out:
        menu_check_client()
        assert "Numéro invalide" in out.getvalue()
    print("  ✓ test_menu_check_client")


def test_menu_inasti_disclaimer_and_as_of():
    with patch("agency.menu.prompt_float", return_value=45000.0), \
         patch("builtins.input", return_value="n"), \
         patch("sys.stdout", new=io.StringIO()) as out:
        menu_inasti()
        txt = out.getvalue()
        assert "as_of" in txt
        assert "Barèmes INASTI" in txt
        assert "TOTAL TRIMESTRIEL À PAYER" in txt
        assert "Ne constitue pas un conseil" in txt
    print("  ✓ test_menu_inasti_disclaimer_and_as_of")


def test_menu_deadlines():
    with patch("sys.stdout", new=io.StringIO()) as out:
        menu_deadlines()
        txt = out.getvalue()
        assert "ÉCHÉANCIER FISCAL & SOCIAL" in txt
        assert "as_of 2026" in txt
        assert "MyMinfin" in txt
    print("  ✓ test_menu_deadlines")


def test_menu_ubl_no_crash_and_file_written():
    """Vérifie que l'option [4] ne crashe plus et génère correctement le fichier XML Peppol."""
    tmp_cwd = Path(tempfile.mkdtemp(prefix="agency_test_ubl_"))
    try:
        old_cwd = Path.cwd()
        os.chdir(str(tmp_cwd))

        with patch("builtins.input", side_effect=["0202239951", "0403201185"]), \
             patch("agency.menu.prompt_float", return_value=2000.0), \
             patch("sys.stdout", new=io.StringIO()) as out:
            menu_ubl()
            txt = out.getvalue()
            assert "Facture XML Peppol générée avec succès" in txt
            assert "Total HTVA : 2000.00 €" in txt
            assert "TVA (21 %) : 420.00 €" in txt
            assert "Total TTC  : 2420.00 €" in txt
            assert "as_of 2026" in txt

            expected_file = tmp_cwd / "facture_INV-2026-001.xml"
            assert expected_file.exists(), f"Le fichier {expected_file} doit exister !"
            xml_data = expected_file.read_text(encoding="utf-8")
            assert "urn:cen.eu:en16931:2017" in xml_data
            assert "INV-2026-001" in xml_data
    finally:
        os.chdir(str(old_cwd))
        shutil.rmtree(tmp_cwd, ignore_errors=True)
    print("  ✓ test_menu_ubl_no_crash_and_file_written")


def test_menu_vault():
    with patch("sys.stdout", new=io.StringIO()) as out:
        menu_vault()
        txt = out.getvalue()
        assert "COFFRE-FORT LOCAL RGPD" in txt
    print("  ✓ test_menu_vault")


if __name__ == "__main__":
    print("Exécution des tests de l'installateur et de la console TUI...")
    test_print_emoji_sans_fix_echoue_sur_cp1252()
    test_force_utf8_stdio_reconfigure_cp1252()
    test_force_utf8_stdio_tolerates_stream_sans_reconfigure()
    test_bootstrap_setup_environment()
    test_build_mcp_server_config()
    test_inject_mcp_server_into_file_new_file()
    test_inject_mcp_server_preserve_existing_servers()
    test_claude_desktop_path_resolution()
    test_run_link_skills_mock()
    test_create_desktop_shortcut()
    test_create_desktop_shortcut_frozen_targets_exe()
    test_build_mcp_server_config_frozen()
    test_cli_mcp_route_runs_stdio_server()
    test_menu_shortcut_delegates_to_install()
    test_run_full_installation_non_interactive()
    test_prompt_float_safety()
    test_menu_check_client()
    test_menu_inasti_disclaimer_and_as_of()
    test_menu_deadlines()
    test_menu_ubl_no_crash_and_file_written()
    test_menu_vault()
    print("\nGREEN — Tous les 21 tests de l'installateur et de la console TUI passent !")
    sys.exit(0)
