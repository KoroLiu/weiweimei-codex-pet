[CmdletBinding()]
param([string]$PetCodexHome = [Environment]::GetEnvironmentVariable('CODEX_HOME'))
$ErrorActionPreference = 'Stop'
if ([string]::IsNullOrWhiteSpace($PetCodexHome)) {
    $PetCodexHome = Join-Path ([Environment]::GetFolderPath('UserProfile')) '.codex'
}
$taskSource = Join-Path $PSScriptRoot 'weiweimei'
$taskPetsRoot = [IO.Path]::GetFullPath((Join-Path $PetCodexHome 'pets'))
$taskDestination = [IO.Path]::GetFullPath((Join-Path $taskPetsRoot 'weiweimei'))
if (-not $taskDestination.StartsWith($taskPetsRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'The pet directory is outside the expected pets folder.'
}
$taskManifest = Get-Content -LiteralPath (Join-Path $taskSource 'pet.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if ($taskManifest.spriteVersionNumber -ne 2 -or $taskManifest.spritesheetPath -ne 'spritesheet.webp') { throw 'Invalid pet manifest.' }
$taskHash = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $taskSource 'spritesheet.webp')).Hash.ToLowerInvariant()
if ($taskHash -ne '1e8dee1f15f93195137d647fbef5bc5bab8b43f3e5be06da6b7c511dff0e109e') { throw 'The sprite sheet has changed; revalidate it before installing.' }
if (Test-Path -LiteralPath $taskDestination) {
    throw "A pet already exists at $taskDestination. No files were overwritten."
}
New-Item -ItemType Directory -Path $taskDestination -Force | Out-Null
foreach ($taskFilename in @('pet.json','spritesheet.webp')) {
    Copy-Item -LiteralPath (Join-Path $taskSource $taskFilename) -Destination (Join-Path $taskDestination $taskFilename)
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $taskSource $taskFilename)).Hash -ne (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $taskDestination $taskFilename)).Hash) { throw "Copy verification failed: $taskFilename" }
}
Write-Output "Pet files installed and hashes verified: $taskDestination"
Write-Output 'Next: Settings > Pets or Mini > Refresh > select Weiweimei > Wake Mini / show pet.'
