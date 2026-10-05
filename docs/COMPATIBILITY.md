# Compatibility and verification

[Project home](../README.md) | [中文首页](../README.zh-CN.md)

Checked against the project owner's Windows Codex desktop installation on October 5, 2026. This is a custom local pet asset package, not a separate desktop application or a ChatGPT Work cloud pet.

## Verified assets

- Native v2 atlas: 1536 × 2288 pixels, eight columns and eleven rows, 192 × 208 pixels per cell.
- Required frames per row: `6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8`; 73 populated cells and 15 transparent unused cells.
- Native rows: `idle`, `running-right`, `running-left`, `waving`, `jumping`, `failed`, `waiting`, `running`, `review`, followed by two rows of look directions.
- The completed-task artwork occupies the `review` row. There is no separate `happy` manifest state.
- WebP decoding, alpha edges, and selected previews were checked against the installed atlas.

## Observed native behavior

The project owner confirmed selecting the pet, seeing it in the native desktop window, and normal appearance. They also observed that the working animation only appears briefly.

The inspected client plays the working reaction for three cycles, approximately 2.46 seconds, then returns to idle. The local manifest does not provide a persistent working-loop setting. The pet's expression should therefore not be used as the sole indicator of task progress.

The sixteen directional frames are present. In this client, gaze targets come from text insertion or computer-operation events; continuous tracking of the physical mouse in the native pet window was not available. The web preview's mouse tracking and continuous-loop controls only demonstrate the artwork.

Completed, waiting, failed, dragging, and restart persistence still require individual end-to-end checks. Their presence in the atlas or client mapping does not establish native runtime success. Other operating systems and client versions have not been tested.

## Installation scope

The installer copies `pet.json` and `spritesheet.webp` into `<CODEX_HOME>/pets/weiweimei/`, or the current user's `.codex/pets/weiweimei/` when `CODEX_HOME` is unset. It refuses to replace an existing folder. Pet selection is performed manually in Codex settings.

The release builder only reads project assets and writes release files under `final/`. It does not require a previously installed pet or change application settings.
