#!/usr/bin/env bash
# link-skills.sh — Lie les skills canoniques (.agents/skills/) vers les dossiers
# natifs des harness (.claude/skills/, .cursor/skills/, .hermes/skills/, .kilocode/skills/).
#
# Usage:
#   bash adapters/link-skills.sh          # applique les liens
#   bash adapters/link-skills.sh -n       # dry-run : affiche sans écrire
#   bash adapters/link-skills.sh -f       # force : remplace les copies figées par des liens
#
# Idempotent : relancer ne duplique rien. Les liens existants corrects sont conservés.
set -euo pipefail

DRY_RUN=0
FORCE=0
for arg in "$@"; do
  case "$arg" in
    -n) DRY_RUN=1 ;;
    -f|--force) FORCE=1 ;;
    *) echo "Usage: bash adapters/link-skills.sh [-n] [-f|--force]" >&2; exit 1 ;;
  esac
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO_ROOT/.agents/skills"

# Harness cibles (créés seulement si le harness semble utilisé OU toujours ? → toujours, léger)
TARGETS=(
  "$REPO_ROOT/.claude/skills"
  "$REPO_ROOT/.cursor/skills"
  "$REPO_ROOT/.hermes/skills"
  "$REPO_ROOT/.kilocode/skills"
)

run() {
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "[dry-run] $*"
  else
    eval "$@"
  fi
}

[[ -d "$SRC" ]] || { echo "ERREUR: $SRC introuvable" >&2; exit 1; }

linked=0
skipped=0

for target_dir in "${TARGETS[@]}"; do
  run "mkdir -p '$target_dir'"
  for skill_path in "$SRC"/*/; do
    skill_name="$(basename "$skill_path")"
    [[ "$skill_name" == _* ]] && continue   # ignore _template & co
    link="$target_dir/$skill_name"
    if [[ -L "$link" ]]; then
      current="$(readlink "$link" || true)"
      if [[ "$current" == "$skill_path" || "$current" == "../../.agents/skills/$skill_name" ]]; then
        ((skipped++)) || true
        continue
      fi
      echo "WARN: $link pointe vers '$current' — laissé tel quel"
      ((skipped++)) || true
      continue
    fi
    if [[ -e "$link" ]]; then
      if [[ $FORCE -eq 1 ]]; then
        # Copie figée périmée → remplacée par un lien
        run "rm -rf '$link'"
      else
        echo "WARN: $link existe (pas un symlink) — laissé tel quel (-f pour forcer)"
        ((skipped++)) || true
        continue
      fi
    fi
    # Lien relatif → portable si le repo bouge
    run "ln -s '../../.agents/skills/$skill_name' '$link'"
    ((linked++)) || true
  done
done

echo ""
echo "Terminé: $linked lien(s) créé(s), $skipped existant(s)/ignoré(s)."
[[ $DRY_RUN -eq 1 ]] && echo "(dry-run — rien n'a été écrit)"
