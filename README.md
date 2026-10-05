# Weiweimei Codex Pet

**English** | [简体中文](README.zh-CN.md)

A custom 2D chibi pet for the Codex desktop app, with thin outlines, nine animation sets, and sixteen look directions. Preview it offline and install it in a desktop client that supports custom pets.

<p align="center">
  <img src="final/previews/idle.webp" width="144" alt="Idle blinking">
  <img src="final/previews/review.webp" width="144" alt="Happy completion reaction">
  <img src="final/previews/failed.webp" width="144" alt="Startled failure reaction">
</p>

## Included

- Nine animation sets: idle, run right, run left, wave, jump, failure, waiting, working, and happy completion.
- Sixteen look directions: clockwise in 22.5-degree steps, starting upward.
- A transparent, lossless WebP atlas, with light/dark background previews and a 96 × 104 small-size check.
- An offline interactive preview, a Windows installer, and a rebuildable ZIP package.

## Quick start

### 1. Download and preview

Select **Code → Download ZIP** above, extract the archive, and open [`final/index.html`](final/index.html) in a browser. No server or Python installation is needed.

The preview lets you switch animations, look directions, background, and display size. Its mouse tracking and continuous playback are artwork inspection controls.

### 2. Install in Codex

Use the Codex desktop app on Windows with custom-pet support. Copy the entire [`final/weiweimei/`](final/weiweimei/) folder to:

```text
%USERPROFILE%\.codex\pets\weiweimei\
```

If `CODEX_HOME` is set, use `<CODEX_HOME>\pets\weiweimei\` instead. The folder must directly contain `pet.json` and `spritesheet.webp`.

Alternatively, open PowerShell in the downloaded project root and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\final\Install-Pet.ps1
```

This sets the execution policy only for that PowerShell process. The installer checks the atlas hash and stops if a folder with the same name already exists.

### 3. Select the pet

In Codex settings, open the **Pets / Mini** page, refresh custom pets, select **维维美 (Weiweimei)**, then show the pet or wake Mini. Button labels depend on the client version.

See the [usage guide](final/USAGE.md) for additional steps.

## Verification and current limits

- Verified: v2 atlas structure, transparent edges, lossless decoding, and preview consistency. The project owner confirmed native selection, display, and normal appearance on Windows.
- In the inspected client, the working reaction plays three cycles, about 2.46 seconds, then returns to idle. **It does not continuously indicate that a task is running.**
- The directional artwork is included, but the current native client does not continuously track the physical mouse. Browser preview behavior does not establish native support.
- Completed, waiting, failed, dragging, and restart persistence still need individual runtime checks. Other client versions and operating systems have not been verified.

See [asset QA](final/QA.md) and [compatibility notes](docs/COMPATIBILITY.md).

## Repository layout

```text
README.md                   English project home
README.zh-CN.md             Chinese project home
final/
  weiweimei/                Installable pet.json and spritesheet.webp
  previews/                 Animation, direction, and alpha-edge previews
  index.html                Offline interactive preview
  Install-Pet.ps1           Windows installer
  USAGE.md                  English usage guide
  USAGE.zh-CN.md             Chinese usage guide
  sources/                  Generated pose artwork and saved prompts
  assemble_pet.py            Atlas assembly and asset checks
  build_delivery.py          Local ZIP packaging
samples/v3/                 Approved expression artwork and extracted frames
scripts/validate_release.py  Pre-release asset and file checks
docs/COMPATIBILITY.md       Verified behavior and client limits
```

## Development and packaging

Development requires Python 3.11+, Pillow, and NumPy. The assembly scripts currently use the Windows Microsoft YaHei font for Chinese QA labels.

```powershell
python -m pip install -r requirements.txt
python scripts/validate_release.py
python final/build_delivery.py
```

The builder writes `final/weiweimei-codex-pet-v1.zip`, `SHA256SUMS.txt`, and `ZIP-SHA256.txt`. Packaging does not require an installed pet or change Codex settings.

To rebuild the atlas, run `python final/assemble_pet.py`. To re-extract the three approved expression sets, first run `python samples/render_samples_v3.py`, then assemble, validate, and package.

## Sources

The character is based on Weiweimei video and expression references supplied by the project owner. Missing poses and look directions were supplemented with ImageGen. Processing scripts crop, clean alpha edges, scale, place, and encode the artwork. Production and installation organization were informed by [zili-codex-pet](https://github.com/2846182283/zili-codex-pet); its character atlas was not used.

Raw recordings, original expression references, and machine-specific investigation records remain local and are excluded from the repository. No open-source license has been assigned to this project; existing character and artwork rights remain with their respective holders.
