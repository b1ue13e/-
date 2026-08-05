$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command py -ErrorAction SilentlyContinue
}
if (-not $python) {
    Write-Error "Python was not found. Install Python, add it to PATH, or run scan_frontmatter.py with the bundled Codex Python runtime."
    exit 1
}
& $python.Source -X utf8 (Join-Path $root "scan_frontmatter.py")
