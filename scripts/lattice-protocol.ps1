# lattice-protocol.ps1
# Dynamically resolves and prints Lattice protocols to stdout.

$query = $args[0]
if ($query -eq "show" -or $query -eq "get" -or $query -eq "view") {
    $query = $args[1]
}

if ([string]::IsNullOrEmpty($query)) {
    Write-Error "Error: Please specify a protocol name to retrieve. Example: lattice-protocol unsure"
    Exit 1
}


# 1. Resolve global target search priorities
$userProfile = $env:USERPROFILE
$lookupPaths = @(
    (Join-Path $userProfile ".claude\skills\lattice"),
    (Join-Path $userProfile ".config\opencode\skills\lattice"),
    (Join-Path $userProfile ".gemini\skills\lattice")
)

$resolvedLatticeDir = $null
foreach ($path in $lookupPaths) {
    if (Test-Path $path) {
        $resolvedLatticeDir = $path
        break
    }
}

if ($resolvedLatticeDir -eq $null) {
    Write-Error "Error: Could not resolve a valid global Lattice skill directory. Checked paths: $lookupPaths"
    Exit 1
}

# 2. Key shorthand mappings
$shorthand = @{
    "unsure"          = "shared/unsure-protocol.md"
    "verification"    = "shared/verification-protocol.md"
    "dpev"            = "shared/dpev-loop-protocol.md"
    "tombstone"       = "shared/tombstone-template.md"
    "brainstorming"   = "shared/brainstorming-protocol.md"
    "plan-checker"    = "shared/plan-checker-protocol.md"
    "writing-plans"   = "shared/writing-plans-protocol.md"
    "resume"          = "shared/resume-protocol.md"
    "cheatsheet"      = "cheatsheet.md"
}

$targetRelativePath = $null
if ($shorthand.ContainsKey($Query.ToLower())) {
    $targetRelativePath = $shorthand[$Query.ToLower()]
}

$targetFile = $null
if ($targetRelativePath -ne $null) {
    $fullPath = Join-Path $resolvedLatticeDir $targetRelativePath
    if (Test-Path $fullPath) {
        $targetFile = Get-Item $fullPath
    }
}

# 3. If not shorthand, try matching files directly or searching recursively
if ($targetFile -eq $null) {
    # Check direct path relative to lattice directory
    $directPath = Join-Path $resolvedLatticeDir $Query
    if (Test-Path $directPath) {
        $targetFile = Get-Item $directPath
    }
    elseif (Test-Path "$directPath.md") {
        $targetFile = Get-Item "$directPath.md"
    }
    else {
        # Search recursively for files matching the query
        $matches = Get-ChildItem -Path $resolvedLatticeDir -Filter "*$Query*.md" -Recurse -File -ErrorAction SilentlyContinue
        if ($matches.Count -eq 1) {
            $targetFile = $matches[0]
        }
        elseif ($matches.Count -gt 1) {
            Write-Host "Multiple protocols matched your query '$Query':" -ForegroundColor Yellow
            foreach ($match in $matches) {
                $relPath = $match.FullName.Replace($resolvedLatticeDir, "").TrimStart("\").TrimStart("/")
                Write-Host "  - $relPath" -ForegroundColor Cyan
            }
            Exit 0
        }
    }
}

if ($targetFile -eq $null -or -not (Test-Path $targetFile.FullName)) {
    Write-Error "Error: Could not find any protocol matching '$Query' inside $resolvedLatticeDir"
    Exit 1
}

# 4. Dump content to stdout
Get-Content -Path $targetFile.FullName -Raw
Exit 0
