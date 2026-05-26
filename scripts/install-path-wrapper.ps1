# install-path-wrapper.ps1
# Deploys lattice-protocol to system PATH using the Smart Fallback protocol.

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$sourcePsScript = Join-Path $scriptDir "lattice-protocol.ps1"
$sourceCmdScript = Join-Path $scriptDir "lattice-protocol.cmd"

$npmPath = Join-Path $env:APPDATA "npm"
$globalDeployed = $false

Write-Host "Starting Smart PATH Fallback installation for lattice-protocol..."

# 1. Attempt deployment to Global NPM Directory
if (Test-Path $npmPath) {
    try {
        $targetPs = Join-Path $npmPath "lattice-protocol.ps1"
        $targetCmd = Join-Path $npmPath "lattice-protocol.cmd"
        
        Copy-Item -Path $sourcePsScript -Destination $targetPs -Force -ErrorAction Stop
        Copy-Item -Path $sourceCmdScript -Destination $targetCmd -Force -ErrorAction Stop
        
        Write-Host "Success: Global PATH installation complete. Commands copied to: $npmPath" -ForegroundColor Green
        $globalDeployed = $true
    }
    catch {
        Write-Warning "Global NPM folder write failed: $_. Falling back to shell profiles..."
    }
}
else {
    Write-Host "Global NPM folder not found ($npmPath). Falling back to shell profiles..."
}

# 2. Fallback to Shell Profiles if Global fails
if (-not $globalDeployed) {
    Write-Host "Registering fallback functions/aliases..."
    
    # PowerShell Profile setup
    $profilePath = $PROFILE
    if (-not $profilePath) {
        $profilePath = Join-Path $env:USERPROFILE "Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
    }
    
    $profileDir = Split-Path -Parent $profilePath
    if (-not (Test-Path $profileDir)) {
        New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    }
    
    $psFunction = @"

# LATTICE PROTOCOL FALLBACK ALIAS
function lattice-protocol {
    param([string]`$Name)
    powershell -NoProfile -ExecutionPolicy Bypass -File "$sourcePsScript" `$Name
}
"@
    
    if (Test-Path $profilePath) {
        $content = Get-Content -Path $profilePath -Raw
        if ($content -notlike "*function lattice-protocol*") {
            Add-Content -Path $profilePath -Value $psFunction -ErrorAction SilentlyContinue
            Write-Host "Added powershell function alias to profile: $profilePath" -ForegroundColor Cyan
        }
        else {
            Write-Host "Powershell alias already exists in profile: $profilePath"
        }
    }
    else {
        New-Item -ItemType File -Path $profilePath -Value $psFunction -Force | Out-Null
        Write-Host "Created profile and added powershell function alias: $profilePath" -ForegroundColor Cyan
    }
    
    # Git Bash setup
    $bashrcPath = Join-Path $env:USERPROFILE ".bashrc"
    $unixPath = $sourcePsScript.Replace("\", "/")
    $bashAlias = "`nalias lattice-protocol=`"powershell.exe -NoProfile -ExecutionPolicy Bypass -File '$unixPath'`"`n"
    
    if (Test-Path $bashrcPath) {
        $content = Get-Content -Path $bashrcPath -Raw
        if ($content -notlike "*alias lattice-protocol*") {
            Add-Content -Path $bashrcPath -Value $bashAlias -ErrorAction SilentlyContinue
            Write-Host "Added Git Bash alias to: $bashrcPath" -ForegroundColor Cyan
        }
        else {
            Write-Host "Git Bash alias already exists in: $bashrcPath"
        }
    }
    else {
        New-Item -ItemType File -Path $bashrcPath -Value $bashAlias -Force | Out-Null
        Write-Host "Created .bashrc and added Git Bash alias: $bashrcPath" -ForegroundColor Cyan
    }
}

Write-Host "Lattice protocol installation finished."
Exit 0
