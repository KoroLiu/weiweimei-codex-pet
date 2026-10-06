param([string]$Voice = 'Microsoft Huihui Desktop', [int]$Rate = 2)
$ErrorActionPreference = 'Stop'
$VideoRoot = Split-Path -Parent $PSScriptRoot
$OutputDir = Join-Path $VideoRoot 'public/voiceover'
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
Add-Type -AssemblyName System.Speech
$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speaker.SelectVoice($Voice)
$speaker.Rate = $Rate
$scenes = Get-Content -Raw -Encoding UTF8 (Join-Path $VideoRoot 'storyboard.json') | ConvertFrom-Json
$results = @()
foreach ($scene in $scenes) {
  $cues = @()
  $time = 0.45
  foreach ($cue in $scene.cues) {
    $file = "$($scene.id)-$($cues.Count + 1).wav"
    $out = Join-Path $OutputDir $file
    $speaker.SetOutputToWaveFile($out)
    $speaker.Speak($cue.say)
    $speaker.SetOutputToNull()
    $bytes = [System.IO.File]::ReadAllBytes($out)
    $offset = 12
    $rateBytes = 0
    $lengthBytes = 0
    while ($offset + 8 -le $bytes.Length) {
      $chunkId = [System.Text.Encoding]::ASCII.GetString($bytes, $offset, 4)
      $chunkLength = [BitConverter]::ToUInt32($bytes, $offset + 4)
      if ($chunkId -eq 'fmt ') { $rateBytes = [BitConverter]::ToUInt32($bytes, $offset + 16) }
      if ($chunkId -eq 'data') { $lengthBytes = $chunkLength; break }
      $offset += 8 + $chunkLength + ($chunkLength % 2)
    }
    if ($rateBytes -le 0 -or $lengthBytes -le 0) { throw "Invalid WAV: $out" }
    $duration = $lengthBytes / $rateBytes
    $startFrame = [int][Math]::Ceiling($time * 30)
    $cues += [ordered]@{ text=$cue.text; startMs=($startFrame / 30 * 1000); endMs=(($startFrame / 30 + $duration + 0.10) * 1000); timestampMs=$null; confidence=$null; pageBreakAfter=$true; audio="voiceover/$file"; frame=$startFrame; duration=$duration }
    $time = $startFrame / 30 + $duration + 0.20
  }
  $durationFrames = [int][Math]::Ceiling(($time + 0.55) * 30)
  $results += [ordered]@{id=$scene.id; title=$scene.title; durationInFrames=$durationFrames; cues=$cues}
}
$speaker.Dispose()
$results | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 (Join-Path $VideoRoot 'voiceover-timing.json')
$results | ForEach-Object { '{0}: {1:N2}s' -f $_.id,($_.durationInFrames/30) }
$totalFrames = 0
foreach ($result in $results) { $totalFrames += $result.durationInFrames }
'Total: {0:N2}s' -f ($totalFrames/30)
