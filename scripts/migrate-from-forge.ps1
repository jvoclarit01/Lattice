param(
  [string]$Path = ".",
  [switch]$WhatIf
)
$planFile     = Join-Path $Path ".forge-plan.md"
$newPlanFile  = Join-Path $Path ".lattice-plan.md"
$oldDir       = Join-Path $Path ".forge"
$newDir       = Join-Path $Path ".lattice"

if (-not (Test-Path $planFile) -and -not (Test-Path $oldDir)) {
  Write-Host "No forge artifacts at $Path."; exit 0
}
if (Test-Path $newPlanFile) {
  Write-Warning ".lattice-plan.md already exists. Backing up to .lattice-plan.md.bak"
  if (-not $WhatIf) { Copy-Item $newPlanFile "$newPlanFile.bak" -Force }
}
if (Test-Path $planFile) {
  $utf8NoBom = New-Object System.Text.UTF8Encoding $false
  $content = [System.IO.File]::ReadAllText($planFile)
  $content = $content -creplace '\.forge-plan\.md', '.lattice-plan.md' `
                      -creplace '\.forge/', '.lattice/' `
                      -creplace 'project-forge', 'project-lattice' `
                      -creplace 'model-forge',   'model-lattice' `
                      -creplace 'thesis-forge',  'thesis-lattice' `
                      -creplace '\bForge\b',     'Lattice' `
                      -creplace '\bforge\b',     'lattice'
  if (-not $WhatIf) {
    [System.IO.File]::WriteAllText($newPlanFile, $content, $utf8NoBom)
    Remove-Item $planFile
  }
  Write-Host "Migrated $planFile -> $newPlanFile"
}
if (Test-Path $oldDir) {
  if (-not $WhatIf) { Move-Item $oldDir $newDir }
  Write-Host "Renamed $oldDir -> $newDir"
}
