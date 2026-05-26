# verify-environment.ps1
# Asserts environment safety in a Lattice workspace. Exits with 1 if protocol files are missing.

$planFile = ".lattice-plan.md"
$currentDir = Get-Item .

# 1. Search upwards to see if we are inside a Lattice workspace
$isLatticeWorkspace = $false
$tempDir = $currentDir
while ($tempDir -ne $null) {
    if (Test-Path (Join-Path $tempDir.FullName $planFile)) {
        $isLatticeWorkspace = $true
        break
    }
    $tempDir = $tempDir.Parent
}

if (-not $isLatticeWorkspace) {
    # Not a Lattice workspace - no-op and pass
    Exit 0
}

Write-Host "Lattice workspace signature detected at: $($tempDir.FullName)"

# 2. Check global target search priorities
$userProfile = $env:USERPROFILE
$lookupPaths = @(
    (Join-Path $userProfile ".claude\skills\lattice"),
    (Join-Path $userProfile ".config\opencode\skills\lattice"),
    (Join-Path $userProfile ".gemini\skills\lattice")
)

$resolvedLatticeDir = $null
$criticalFiles = @(
    "shared/dpev-loop-protocol.md",
    "shared/unsure-protocol.md",
    "shared/verification-protocol.md"
)

foreach ($path in $lookupPaths) {
    if (Test-Path $path) {
        $allExist = $true
        foreach ($file in $criticalFiles) {
            $fullFilePath = Join-Path $path $file
            if (-not (Test-Path $fullFilePath)) {
                $allExist = $false
                break
            }
        }
        if ($allExist) {
            $resolvedLatticeDir = $path
            break
        }
    }
}

if ($resolvedLatticeDir -eq $null) {
    Write-Error "======================================================================"
    Write-Error "CRITICAL ERROR: LATTICE CORE COMPLIANCE FAIL-FAST"
    Write-Error "======================================================================"
    Write-Error "Lattice plan was detected, but protocol instructions are missing or unreachable!"
    Write-Error "Please verify that the global skills folders contain the required protocol files."
    Write-Error "Expected one of the following to be fully populated:"
    foreach ($p in $lookupPaths) {
        Write-Error "  - $p"
    }
    Write-Error "Halting agent execution immediately to prevent default non-compliant actions."
    Exit 1
}

Write-Host "Lattice core protocols verified successfully at: $resolvedLatticeDir"
Exit 0
