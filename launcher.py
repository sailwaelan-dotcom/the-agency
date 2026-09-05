"""
Point d'entrée exécutable autonome pour The Agency (TheAgency.exe).
Permet aux solopreneurs d'exécuter l'agence par double-clic ou en ligne de commande,
sans nécessiter l'installation préalable de Python ou de Git sur leur ordinateur.
Tout le routage (menu interactif, sous-commandes CLI, serveur MCP) vit dans agency.cli.
"""
from agency.bootstrap import setup_environment

setup_environment()

from agency.cli import main as cli_main

if __name__ == "__main__":
    cli_main()
