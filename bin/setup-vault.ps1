param(
  [Parameter(Mandatory = $true)]
  [string]$VaultPath,

  [ValidateSet("generic", "lyt", "para", "zettelkasten")]
  [string]$Mode = "generic"
)

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pluginRoot = Split-Path -Parent $scriptRoot
python (Join-Path $pluginRoot "scripts\setup_vault.py") $VaultPath --mode $Mode
