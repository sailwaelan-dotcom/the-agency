#!/usr/bin/env python3
"""
Scanner de sécurité — The Agency.
Détecte secrets, chemins machine, injection de prompt, exfiltration, identifiants belges réels.

Usage: python scripts/security_scan.py [path]
Exit 0 si clean, 1 avec liste des findings sinon.
Ne logue JAMAIS la ligne suspecte en clair — uniquement fichier + catégorie + numéro de ligne.

Mécanismes anti faux-positifs :
- Marqueur `<!-- nosec -->` ou `# nosec` en fin de ligne → ligne ignorée (usage restreint
  aux fichiers de politique/documentations de sécurité).
- Heuristique de négation : si la ligne matchée contient un marqueur de politique
  ("jamais", "ne doit", "interdit", "never", "do not"...), BLOCK → WARN.
"""
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Patterns bloquants : (catégorie, regex, est_bloquant)
PATTERNS: list[tuple[str, re.Pattern, bool]] = [
    # --- Secrets / clés ---
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), True),
    ("aws-key", re.compile(r"AKIA[0-9A-Z]{16}"), True),
    ("openai-style-key", re.compile(r"\bsk-[a-zA-Z0-9_-]{20,}"), True),
    ("github-token", re.compile(r"\bghp_[a-zA-Z0-9]{36,}"), True),
    ("github-oauth", re.compile(r"\bgho_[a-zA-Z0-9]{36,}"), True),
    ("slack-token", re.compile(r"\bxox[baprs]-[a-zA-Z0-9-]{10,}"), True),
    ("generic-api-key-assignment", re.compile(r"(api[_-]?key|apikey|secret|password|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}['\"]", re.I), True),
    ("bearer-token", re.compile(r"Bearer\s+[A-Za-z0-9_\-\.]{20,}"), True),

    # --- Chemins machine absolus personnels ---
    # NOTE: en raw string, \\ = regex \\ = 1 backslash littéral matché (chemins Windows réels)
    ("win-user-path", re.compile(r"[A-Za-z]:\\Users\\(?!<VOTRE_USER>|USERNAME|PLACEHOLDER)[A-Za-z0-9_.-]+\\"), True),
    ("win-user-path-forward", re.compile(r"[A-Za-z]:/Users/(?!<VOTRE_USER>|USERNAME|PLACEHOLDER)[A-Za-z0-9_.-]+/"), True),
    ("msys-user-path", re.compile(r"(?<![\w<])/[a-z]/Users/(?!<VOTRE_USER>|USERNAME|PLACEHOLDER)[A-Za-z0-9_.-]+/"), True),
    ("unix-home-path", re.compile(r"/home/(?!<VOTRE_USER>|user|username)[a-z][a-z0-9_-]+/"), True),
    ("mac-user-path", re.compile(r"(?<![\w<])/Users/(?!<VOTRE_USER>|USERNAME|PLACEHOLDER)[A-Za-z0-9_.-]+/"), True),

    # --- Exfiltration / exécution dangereuse ---
    ("curl-pipe-shell", re.compile(r"curl\s[^|\n]*\|\s*(sudo\s+)?(ba)?sh\b"), True),
    ("wget-pipe-shell", re.compile(r"wget\s[^|\n]*\|\s*(sudo\s+)?(ba)?sh\b"), True),
    ("webhook-exfil", re.compile(r"(discord|slack)\.com/api/webhooks/[A-Za-z0-9/_-]+"), True),
    ("pastebin", re.compile(r"pastebin\.com/(raw/)?[A-Za-z0-9]{6,}"), True),
    ("netcat-reverse", re.compile(r"\bnc\b.*-e\s*/bin/(ba)?sh"), True),
    ("eval-exec-danger", re.compile(r"\b(eval|exec)\s*\(\s*(base64|atob|request|urllib|fetch)"), True),

    # --- Injection de prompt ---
    ("prompt-injection-ignore", re.compile(r"ignore\s+(all\s+|the\s+)?(previous|prior|above)\s+instructions", re.I), True),
    ("prompt-injection-roleplay", re.compile(r"you\s+are\s+now\s+(a\s+)?(DAN|jailbroken|unrestricted)", re.I), True),
    ("prompt-injection-system", re.compile(r"(disclose|reveal|print|show)\s+(your\s+)?(system\s+prompt|initial\s+instructions)", re.I), True),

    # --- Identifiants belges réels (placeholders whitelistés) ---
    ("bce-number-real", re.compile(r"\bBE0(?!123\.456\.789)\d{3}\.\d{3}\.\d{3}\b"), True),
    ("iban-be", re.compile(r"\bBE\d{2}\s?\d{4}\s?\d{4}\s?\d{4}\b"), True),
    ("nn-be", re.compile(r"\b\d{2}\.\d{2}\.\d{2}-\d{3}\.\d{2}\b"), True),  # numéro national
]

# Marqueurs qui font passer un BLOCK en WARN (contexte de politique, pas d'exécution)
NEGATION_MARKERS = re.compile(
    r"(jamais|never|interdit|interdire|ne\s+doit|ne\s+pas|don'?t|do\s+not|forbidden"
    r"|must\s+not|avoid|éviter|beware|avertissement|what\s+not\s+to\s+do|n'\w+\s+pas)",
    re.I,
)
# Suppression explicite d'une ligne (documentation de sécurité uniquement)
NOSEC_MARKER = re.compile(r"(#\s*nosec\b|<!--\s*nosec\b)", re.I)

# Extensions à scanner
SCAN_EXT = {".md", ".py", ".sh", ".yaml", ".yml", ".json", ".toml", ".txt", ".ps1", ".js", ".ts"}
# Dirs à ignorer
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
# Fichiers à ignorer (le scanner lui-même contient les patterns)
SKIP_FILES = {"security_scan.py"}


def scan_file(path: Path) -> list[tuple[str, str, int]]:
    """Retourne [(severite, categorie, ligne)] — jamais le contenu de la ligne."""
    findings: list[tuple[str, str, int]] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings
    for lineno, line in enumerate(text.splitlines(), 1):
        if NOSEC_MARKER.search(line):
            continue
        for category, pattern, blocking in PATTERNS:
            if pattern.search(line):
                sev = "BLOCK" if blocking else "WARN"
                if blocking and NEGATION_MARKERS.search(line):
                    sev = "WARN"  # contexte de politique documentaire
                findings.append((sev, category, lineno))
    return findings


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO_ROOT
    if not root.is_dir():
        print(f"ERREUR: {root} introuvable", file=sys.stderr)
        return 1

    scanned = 0
    blocks: list[str] = []
    warns: list[str] = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn in SKIP_FILES:
                continue
            ext = Path(fn).suffix.lower()
            if ext not in SCAN_EXT:
                continue
            fpath = Path(dirpath) / fn
            scanned += 1
            rel = fpath.relative_to(root)
            for sev, category, lineno in scan_file(fpath):
                msg = f"{sev} {rel}:{lineno} [{category}]"
                (blocks if sev == "BLOCK" else warns).append(msg)

    print(f"Scanné: {scanned} fichier(s)")
    for w in warns:
        print(f"  {w}")
    if blocks:
        print(f"\n{'=' * 50}")
        print(f"BLOQUANT: {len(blocks)} finding(s)")
        for b in blocks:
            print(f"  {b}")
        return 1
    print("OK: aucun leak bloquant détecté")
    return 0


if __name__ == "__main__":
    sys.exit(main())
