param(
    [Parameter(Mandatory=$true)]
    [string]$VaultPath,
    [switch]$Create
)

$scriptPath = Join-Path $PSScriptRoot "detect_vault.py"
$argsList = @($scriptPath, $VaultPath)
if ($Create) {
    $argsList += "--create"
}

python @argsList
exit $LASTEXITCODE
