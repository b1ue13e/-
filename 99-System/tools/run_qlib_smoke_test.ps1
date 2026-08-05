param(
    [string]$PythonExecutable = "python",
    [string]$Workspace = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$VaultRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
if ([string]::IsNullOrWhiteSpace($Workspace)) {
    $Workspace = Join-Path $VaultRoot "99-System\tmp\qlib-pilot-runtime"
}
$Workspace = [System.IO.Path]::GetFullPath($Workspace)

$QlibCommit = "da920b7f954f48ab1bb64117c976710de198373e"
$QlibPackageVersion = "0.9.7"
$DataRelease = "2026-07-27"
$QlibRepo = Join-Path $Workspace "external\qlib"
$DataRepo = Join-Path $Workspace "external\investment_data"
$DownloadDir = Join-Path $Workspace "downloads"
$ProviderDir = Join-Path $Workspace "data\cn_data"
$RunDir = Join-Path $Workspace "run"
$LogDir = Join-Path $Workspace "logs"
$EvidenceDir = Join-Path $Workspace "data_manifest"
$VenvDir = Join-Path $Workspace ".venv"
$Archive = Join-Path $DownloadDir "qlib_bin.tar.gz"
$Manifest = Join-Path $DownloadDir "qlib_bin.manifest.json"
$ReleaseBase = "https://github.com/chenditc/investment_data/releases/download/$DataRelease"

New-Item -ItemType Directory -Force -Path $Workspace, $DownloadDir, $ProviderDir, $RunDir, $LogDir, $EvidenceDir | Out-Null
$Transcript = Join-Path $LogDir ("smoke-{0}.log" -f (Get-Date -Format "yyyyMMdd-HHmmss"))
Start-Transcript -Path $Transcript | Out-Null

try {
    function Get-PinnedRepository {
        param(
            [Parameter(Mandatory = $true)][string]$Url,
            [Parameter(Mandatory = $true)][string]$Path,
            [Parameter(Mandatory = $true)][string]$Revision
        )

        if (-not (Test-Path -LiteralPath (Join-Path $Path ".git"))) {
            git clone $Url $Path
            if ($LASTEXITCODE -ne 0) { throw "git clone failed: $Url" }
        }

        $dirty = git -C $Path status --porcelain
        if ($LASTEXITCODE -ne 0) { throw "git status failed: $Path" }
        if ($dirty) { throw "Refusing to change a modified checkout: $Path" }

        git -C $Path fetch --tags origin
        if ($LASTEXITCODE -ne 0) { throw "git fetch failed: $Path" }
        git -C $Path checkout --detach $Revision
        if ($LASTEXITCODE -ne 0) { throw "git checkout failed: $Revision" }
    }

    Get-PinnedRepository -Url "https://github.com/microsoft/qlib.git" -Path $QlibRepo -Revision $QlibCommit
    Get-PinnedRepository -Url "https://github.com/chenditc/investment_data.git" -Path $DataRepo -Revision $DataRelease

    if (-not (Test-Path -LiteralPath $Archive)) {
        Invoke-WebRequest "$ReleaseBase/qlib_bin.tar.gz" -OutFile $Archive -UseBasicParsing
    }
    if (-not (Test-Path -LiteralPath $Manifest)) {
        Invoke-WebRequest "$ReleaseBase/qlib_bin.manifest.json" -OutFile $Manifest -UseBasicParsing
    }

    $ValidationOutput = & $PythonExecutable (Join-Path $DataRepo "qlib\validate_archive.py") `
        --archive $Archive `
        --manifest $Manifest `
        --expected-tag $DataRelease `
        --require-publishable 2>&1
    $ValidationExitCode = $LASTEXITCODE
    $ValidationOutput | Tee-Object -FilePath (Join-Path $EvidenceDir "archive-validation.json")
    if ($ValidationExitCode -ne 0) { throw "investment_data archive validation failed" }
    Copy-Item -LiteralPath $Manifest -Destination (Join-Path $EvidenceDir "qlib_bin.manifest.json") -Force

    $ProviderMarker = Join-Path $ProviderDir "provider-release.txt"
    if (Test-Path -LiteralPath (Join-Path $ProviderDir "calendars\day.txt")) {
        if (-not (Test-Path -LiteralPath $ProviderMarker)) {
            throw "Existing provider data has no release marker: $ProviderDir"
        }
        $ExistingRelease = (Get-Content -LiteralPath $ProviderMarker -Raw -Encoding UTF8).Trim()
        if ($ExistingRelease -ne $DataRelease) {
            throw "Existing provider data is release $ExistingRelease, expected $DataRelease"
        }
    }
    else {
        tar.exe -xzf $Archive -C $ProviderDir --strip-components=1
        if ($LASTEXITCODE -ne 0) { throw "data extraction failed" }
        $DataRelease | Set-Content -LiteralPath $ProviderMarker -Encoding ASCII
    }

    if (-not (Test-Path -LiteralPath $VenvDir)) {
        & $PythonExecutable -m venv $VenvDir
        if ($LASTEXITCODE -ne 0) { throw "virtual environment creation failed" }
    }

    $VenvPython = Join-Path $VenvDir "Scripts\python.exe"
    $Qrun = Join-Path $VenvDir "Scripts\qrun.exe"
    & $VenvPython -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) { throw "pip upgrade failed" }
    # Windows users should use Qlib's official prebuilt wheel. Installing the
    # checkout directly requires the Microsoft C++ toolchain to compile Cython.
    & $VenvPython -m pip install --only-binary=pyqlib "pyqlib==$QlibPackageVersion"
    if ($LASTEXITCODE -ne 0) { throw "Qlib installation failed" }
    # Qlib 0.9.7 uses MLflow's local filesystem experiment store. MLflow 3.x
    # disables that backend by default, so keep the compatible 2.x line.
    & $VenvPython -m pip install "mlflow<3"
    if ($LASTEXITCODE -ne 0) { throw "MLflow compatibility installation failed" }
    & $VenvPython -m pip freeze | Set-Content -LiteralPath (Join-Path $Workspace "requirements.lock") -Encoding UTF8
    & $VenvPython --version 2>&1 | Set-Content -LiteralPath (Join-Path $Workspace "python-version.txt") -Encoding UTF8
    $QlibCommit | Set-Content -LiteralPath (Join-Path $Workspace "source_commit.txt") -Encoding UTF8
    $QlibPackageVersion | Set-Content -LiteralPath (Join-Path $Workspace "qlib-version.txt") -Encoding UTF8

    $TemplateConfig = Join-Path $QlibRepo "examples\benchmarks\LightGBM\workflow_config_lightgbm_Alpha158.yaml"
    $SmokeConfig = Join-Path $RunDir "workflow_config_lightgbm_Alpha158.smoke.yaml"
    $ProviderYaml = $ProviderDir.Replace("\", "/")
    $ConfigText = Get-Content -LiteralPath $TemplateConfig -Raw -Encoding UTF8
    $ConfigText = $ConfigText -replace 'provider_uri:\s*".*"', "provider_uri: `"$ProviderYaml`""
    $ConfigText = $ConfigText -replace 'num_threads:\s*20', 'num_threads: 4'
    Set-Content -LiteralPath $SmokeConfig -Value $ConfigText -Encoding UTF8

    if (-not (Test-Path -LiteralPath (Join-Path $RunDir ".git"))) {
        git -C $RunDir init | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "runtime Git initialization failed" }
    }

    Push-Location $RunDir
    try {
        $env:PYTHONUTF8 = "1"
        $JoblibTemp = Join-Path $Workspace "joblib_tmp"
        New-Item -ItemType Directory -Force -Path $JoblibTemp | Out-Null
        $env:TEMP = $JoblibTemp
        $env:TMP = $JoblibTemp
        $env:JOBLIB_TEMP_FOLDER = $JoblibTemp
        # The runtime lives inside the Obsidian vault's Git repository. Keep
        # Qlib from trying to capture the vault-wide (and partly binary) diff.
        $env:GIT_CEILING_DIRECTORIES = $Workspace
        # Qlib writes normal progress messages to stderr. PowerShell 5 turns
        # redirected native stderr into a terminating NativeCommandError when
        # the script-wide preference is Stop, so relax it only for qrun.
        $PreviousErrorActionPreference = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        try {
            $QrunCommand = "`"$Qrun`" `"$SmokeConfig`" 2>&1"
            & cmd.exe /d /s /c $QrunCommand | Tee-Object -FilePath (Join-Path $LogDir "qrun-output.log")
            $QrunExitCode = $LASTEXITCODE
        }
        finally {
            $ErrorActionPreference = $PreviousErrorActionPreference
        }
        $QrunExitCode | Set-Content -LiteralPath (Join-Path $LogDir "qrun-exit-code.txt") -Encoding ASCII
        if ($QrunExitCode -ne 0) { throw "Qlib smoke test failed with exit code $QrunExitCode" }
    }
    finally {
        Pop-Location
    }

    Write-Host "Qlib smoke test passed. Evidence: $Workspace"
}
finally {
    Stop-Transcript | Out-Null
}
