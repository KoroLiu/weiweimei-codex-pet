> 范围澄清（2026-10-06）：本文中的 16 方向计数仅是历史素材和 v2 格式校验。视线跟随已取消，不列为当前可用功能；原生持续手动鼠标跟随不可用。

# Asset QA

The v2 atlas and previews were produced on October 4, 2026. Native feedback was updated on October 5, 2026.

## Asset checks

- Atlas: 1536 × 2288 pixels; cell: 192 × 208; eight columns and eleven rows.
- Populated frames per row: `6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8`. Total: 73 populated cells and 15 fully transparent unused cells.
- Lossless WebP pixels match the assembled atlas. The encoded atlas hash is recorded in `validation.json`.
- Idle, failure, and happy completion reuse the approved v3 artwork. Completion uses the native `review` row.
- Missing poses and sixteen look directions were generated from saved references and prompts. Running uses the repaired v2 source artwork; two clipped directional poses were repaired separately.
- Connected-component crops retain full poses. Shared scales are used per set instead of independently stretching each frame.
- The five jump poses include vertical offsets of `0, 8, 16, 8, 0` pixels.
- Previews include nine transparent animations, directional artwork, a full contact sheet, a small contact sheet, and light/dark edge checks.
- Compositing checks for idle, completion, jumping, and failure are recorded in `preview-composite-review.json`.

## Native verification

The project owner confirmed native selection, display, and normal appearance. They reported a brief working reaction. Continuous physical-mouse tracking was unavailable in the inspected native client; persistent working animation remains unsupported by the current asset interface.

Completed, waiting, failed, dragging, and restart persistence still need individual runtime checks. Asset presence and browser preview behavior do not establish native runtime support.

Machine-specific installation receipts and application inspection dumps remain local. The repository's compatibility summary provides additional context.
