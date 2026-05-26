# quicksave.ps1 - Git-based quicksave snapshouter
# Non-destructively saves all changes (tracked and untracked) to a hidden Git ref.

git rev-parse --is-inside-work-tree >$null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Current directory is not a Git repository. Quicksave skipped." -ForegroundColor Yellow
    exit 0
}

# Stage all changes (tracked and untracked) to create the tree
git add -A

# Ensure there are actually changes to write
$treeSha = git write-tree 2>$null
if ([string]::IsNullOrEmpty($treeSha) -or $LASTEXITCODE -ne 0) {
    git reset >$null
    Write-Host "No changes detected. Snapshot skipped."
    exit 0
}

$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$headSha = git rev-parse HEAD 2>$null

# Create a commit from the staged tree
if ($headSha) {
    $commitSha = git commit-tree $treeSha -p $headSha -m "quicksave_snapshot_$timestamp" 2>$null
} else {
    # If initial repository with no commits yet
    $commitSha = git commit-tree $treeSha -m "quicksave_snapshot_$timestamp" 2>$null
}

if ([string]::IsNullOrEmpty($commitSha) -or $LASTEXITCODE -ne 0) {
    git reset >$null
    Write-Host "Error: Failed to create quicksave commit tree." -ForegroundColor Red
    exit 1
}

# Update the hidden ref to point to the new commit
git update-ref "refs/lattice/quicksaves/$timestamp" $commitSha

# Reset the index back so the user's workspace looks unchanged
git reset >$null

# Record the latest quicksave timestamp in the .git directory
$gitDir = git rev-parse --git-dir
$latestRefFile = Join-Path $gitDir "lattice_latest_quicksave"
$timestamp | Out-File -FilePath $latestRefFile -Encoding ascii -NoNewline

Write-Host "Quicksave snapshot created: refs/lattice/quicksaves/$timestamp (SHA: $commitSha)" -ForegroundColor Green
exit 0
