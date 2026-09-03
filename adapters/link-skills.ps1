# link-skills.ps1 — Lie les skills canoniques (.agents/skills/) vers les dossiers
# natifs des harness (.claude/skills/, .cursor/skills/, .hermes/skills/, .kilocode/skills/).
#
# Crée des JUNCTIONS NTFS (pas des symlinks) — fonctionne sans droits admin.
# Idempotent : relancer ne duplique rien. Les junctions existantes sont conservées.
#
# Usage:
#   powershell -File adapters/link-skills.ps1          # applique les liens
#   powershell -File adapters/link-skills.ps1 -DryRun   # dry-run : affiche sans écrire
#   powershell -File adapters/link-skills.ps1 -Force    # force : remplace les copies figées par des junctions

param(
    [switch]$DryRun,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Src = Join-Path $RepoRoot ".agents\skills"

# Harness cibles
$Targets = @(
    (Join-Path $RepoRoot ".claude\skills"),
    (Join-Path $RepoRoot ".cursor\skills"),
    (Join-Path $RepoRoot ".hermes\skills"),
    (Join-Path $RepoRoot ".kilocode\skills")
)

if (-not (Test-Path $Src)) {
    Write-Error "ERREUR: $Src introuvable"
    exit 1
}

$linked = 0
$skipped = 0

foreach ($targetDir in $Targets) {
    # Créer le dossier cible si nécessaire
    if (-not (Test-Path $targetDir)) {
        if ($DryRun) {
            Write-Host "[dry-run] mkdir $targetDir"
        } else {
            New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
        }
    }

    # Parcourir les skills (ignorer _*)
    $skillDirs = Get-ChildItem -Path $Src -Directory | Where-Object { -not $_.Name.StartsWith("_") }

    foreach ($skillDir in $skillDirs) {
        $link = Join-Path $targetDir $skillDir.Name

        # Vérifier si la junction existe déjà
        if (Test-Path $link) {
            $item = Get-Item $link -Force
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                # C'est déjà une junction — on ne touche pas
                $skipped++
                continue
            } elseif ($Force) {
                # Copie figée périmée → remplacée par une junction
                if ($DryRun) {
                    Write-Host "[dry-run] supprimer $link (copie figée)"
                } else {
                    Remove-Item $link -Recurse -Force
                }
            } else {
                Write-Host "WARN: $link existe (pas une junction) — laissé tel quel (-Force pour forcer)"
                $skipped++
                continue
            }
        }

        # Créer la junction
        if ($DryRun) {
            Write-Host "[dry-run] junction $link -> $($skillDir.FullName)"
        } else {
            try {
                cmd /c mklink /J "`"$link`"" "`"$($skillDir.FullName)`"" 2>&1 | Out-Null
                $linked++
            } catch {
                Write-Host "WARN: impossible de créer $link — $($_.Exception.Message)"
                $skipped++
            }
        }
    }
}

Write-Host ""
Write-Host "Termine: $linked junction(s) creee(s), $skipped existante(s)/ignoree(s)."
if ($DryRun) {
    Write-Host "(dry-run — rien n'a ete ecrit)"
}
