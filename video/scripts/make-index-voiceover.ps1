param([Parameter(Mandatory=$true)][string]$BatchName, [string[]]$Scene)
$ErrorActionPreference = 'Stop'
$voiceArguments = @('-X', 'utf8', (Join-Path $PSScriptRoot 'make-index-voiceover.py'), '--batch-name', $BatchName)
if ($Scene) { $voiceArguments += @('--scenes') + $Scene }
& 'D:\Anaconda\envs\index-tts\python.exe' @voiceArguments
if ($LASTEXITCODE -ne 0) { throw "IndexTTS voiceover failed: $LASTEXITCODE" }
