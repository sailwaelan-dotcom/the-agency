"""
Script de compilation PyInstaller pour générer TheAgency.exe.
Produit un binaire Windows autonome dans 'dist/TheAgency.exe'
embarquant l'interpréteur Python, les compétences .agents, le serveur MCP, adapters et le CLI.
"""
import os
import platform
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def force_utf8_stdio():
    """
    Force stdout/stderr en UTF-8 sur les consoles qui ne le sont pas par défaut
    (cp1252 sur Windows français, runners GitHub Actions inclus) : sans cela,
    le moindre emoji dans les messages de build lève UnicodeEncodeError.
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def build_exe():
    force_utf8_stdio()
    if platform.system() != "Windows":
        print("❌ Erreur : La compilation du binaire .exe est conçue exclusivement pour Windows.")
        sys.exit(1)

    sep = ";"

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--name",
        "TheAgency",
        "--clean",
        "--noconfirm",
        "--hidden-import=sqlite3",
        "--hidden-import=xml.etree.ElementTree",
        "--hidden-import=urllib.request",
        f"--add-data=.agents{sep}.agents",
        f"--add-data=mcp{sep}mcp",
        f"--add-data=agency{sep}agency",
        f"--add-data=adapters{sep}adapters",
        "launcher.py",
    ]

    print("==================================================================")
    print("🇧🇪 Compilation de TheAgency.exe en binaire Windows autonome...")
    print("==================================================================")
    print("Commande :", " ".join(cmd))

    ret = subprocess.run(cmd, cwd=str(REPO_ROOT))
    if ret.returncode == 0:
        exe_path = REPO_ROOT / "dist" / "TheAgency.exe"
        size_mb = exe_path.stat().st_size / (1024 * 1024) if exe_path.exists() else 0
        print("\n🎉 Compilation réussie !")
        print(f"Binaire généré : {exe_path} ({size_mb:.1f} Mo)")
        print("Ce fichier est 100% autonome et peut être distribué aux solopreneurs.")
    else:
        print(f"\n❌ Erreur lors de la compilation (code {ret.returncode}).")
        sys.exit(ret.returncode)


if __name__ == "__main__":
    build_exe()
