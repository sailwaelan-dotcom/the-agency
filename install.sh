#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "🇧🇪 Lancement de l'auto-configuration de The Agency..."
echo "=========================================================="

if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "[ERREUR] Python n'est pas installé sur votre système."
        echo "Veuillez installer Python 3 via votre gestionnaire de paquets (brew, apt...)."
        exit 1
    else
        PYTHON_CMD=python
    fi
else
    PYTHON_CMD=python3
fi

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$PYTHON_CMD" "$DIR/install.py"
