# rollback.ps1 - Git-based rollback script
# Discards current changes and restores workspace to the last quicksave snapshot.

git rev-parse --is-inside-work-tree >$null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Current directory is not a Git repository. Rollback skipped." -ForegroundColor Yellow
    exit 0
}

$gitDir = git rev-parse --git-dir
$latestRefFile = Join-Path $gitDir "lattice_latest_quicksave"
if (-not (Test-Path $latestRefFile)) {
    Write-Host "No quicksave snapshots found. Nothing to rollback." -ForegroundColor Yellow
    exit 0
}

$timestamp = Get-Content $latestRefFile
$refName = "refs/lattice/quicksaves/$timestamp"

# Verify if the ref exists
$commitSha = git rev-parse --verify $refName 2>$null
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrEmpty($commitSha)) {
    Write-Host "Error: Quicksave ref $refName does not exist." -ForegroundColor Red
    exit 1
}

Write-Host "Rolling back to quicksave: $refName (SHA: $commitSha)..."

# 1. Clean untracked files
git clean -fd

# 2. Reset tracked changes to HEAD
git reset --hard HEAD >$null 2>&1

# 3. Checkout all files from the quicksave commit tree to the working directory
git checkout $commitSha -- . >$null 2>&1

# 4. Reset index so that the restored files are seen as unstaged modifications
git reset >$null

Write-Host "Successfully rolled back workspace to quicksave snapshot: $timestamp" -ForegroundColor Green
exit 0
