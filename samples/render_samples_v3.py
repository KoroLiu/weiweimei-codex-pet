"""Extract supplied imagegen poses and encode the actual thinner-outline previews.

Only crops, alpha fringe cleanup, shared scaling and registration are performed.
No eyes, outlines, body parts or pet poses are drawn by this program.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent / "v3"
CELL = (192, 208)
FONT = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 18)
STATES = {"idle": ("常态", 3, 6), "happy": ("开心", 3, 6), "failed": ("炸毛", 4, 8)}
frames, extraction = {}, {}

for state, (label, columns, count) in STATES.items():
    path = ROOT / f"{state}-thin-source-v1.png"
    master = Image.open(path).convert("RGBA")
    poses, reviews = [], []
    for slot in range(count):
        column, row = slot % columns, slot // columns
        box = (round(column * master.width / columns), round(row * master.height / 2), round((column + 1) * master.width / columns), round((row + 1) * master.height / 2))
        pose = master.crop(box)
        data = np.array(pose)
        # Discard only almost invisible fringe and hidden RGB from the tool's
        # transparent output. All visible character color and alpha remain.
        data[data[:, :, 3] <= 8] = 0
        pose = Image.fromarray(data)
        bounds = pose.getbbox()
        if bounds is None or bounds[0] <= 0 or bounds[1] <= 0 or bounds[2] >= pose.width or bounds[3] >= pose.height:
            raise ValueError(f"Pose clipping at source slot {state}:{slot}, {bounds}")
        cropped = pose.crop(bounds)
        poses.append(cropped)
        reviews.append({"slot": slot, "grid_crop": list(box), "subject_bounds": list(bounds), "height": cropped.height, "width": cropped.width})
    heights = [pose.height for pose in poses]
    scale = min(180 / float(np.median(heights)), 168 / max(pose.width for pose in poses), 184 / max(heights))
    folder = ROOT / "native-frames" / state
    folder.mkdir(parents=True, exist_ok=True)
    frames[state] = []
    for index, pose in enumerate(poses):
        size = (round(pose.width * scale), round(pose.height * scale))
        fitted = pose.resize(size, Image.Resampling.LANCZOS)
        cell = Image.new("RGBA", CELL)
        cell.alpha_composite(fitted, ((192 - fitted.width) // 2, 196 - fitted.height))
        alpha = np.asarray(cell.getchannel("A"))
        if np.any(alpha[0]) or np.any(alpha[-1]) or np.any(alpha[:, 0]) or np.any(alpha[:, -1]):
            raise ValueError(f"Cell clips at {state}:{index}")
        cell.save(folder / f"{index + 1:03d}.png")
        frames[state].append(cell)
    extraction[state] = {"source": path.name, "sha256": hashlib.file_digest(path.open("rb"), "sha256").hexdigest(), "dimensions": list(master.size), "mode": master.mode, "alpha_extrema": list(master.getchannel("A").getextrema()), "frame_count": count, "fixed_shared_scale": scale, "source_height_ratio": max(heights) / min(heights), "registration": "one scale within state, centered silhouette, fixed floor at y196", "poses": reviews}


def stage(cell, state, theme):
    bg = (241, 243, 247) if theme == "light" else (28, 32, 42)
    fg = (35, 39, 49) if theme == "light" else (236, 238, 244)
    image = Image.new("RGB", (320, 300), bg)
    image.paste(cell, (64, 26), cell)
    ImageDraw.Draw(image).text((160, 264), STATES[state][0], font=FONT, fill=fg, anchor="mm")
    return image


encoding = {}
for state in STATES:
    if state == "idle":
        # Timing comes from the actual installed native idle renderer.
        sequence = frames[state]
        durations = [1680, 660, 660, 840, 840, 1920]
    elif state == "happy":
        sequence = [frames["idle"][0]] + frames[state] + [frames["idle"][0]]
        durations = [600] + [140] * len(frames[state]) + [1200]
    else:
        sequence = [frames["idle"][0]] + frames[state] + [frames["idle"][0]]
        durations = [1100] + [100] * len(frames[state]) + [1400]
    encoding[state] = {}
    for theme in ["light", "dark"]:
        previews = [stage(cell, state, theme) for cell in sequence]
        palette_source = Image.new("RGB", (320 * len(previews), 300))
        for index, preview in enumerate(previews):
            palette_source.paste(preview, (320 * index, 0))
        palette = palette_source.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
        quantized = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in previews]
        path = ROOT / f"{state}-{theme}.gif"
        quantized[0].save(path, save_all=True, append_images=quantized[1:], duration=durations, loop=0, disposal=2, optimize=False)
        stage(frames[state][0], state, theme).save(ROOT / f"{state}-{theme}-still.png")
        # Preserve real alpha in the separate lossless animated WebP.
        sequence[0].save(ROOT / f"{state}-transparent.webp", save_all=True, append_images=sequence[1:], duration=durations, loop=0, lossless=True, method=6)
        with Image.open(path) as encoded:
            total = 0
            for index in range(encoded.n_frames):
                encoded.seek(index)
                total += encoded.info.get("duration", 0)
            encoding[state][theme] = {"file": path.name, "frames": encoded.n_frames, "duration_ms": total}

contact = Image.new("RGB", (960, 900), "#f1f3f7")
comparison = Image.new("RGB", (960, 600), "#f1f3f7")
for column, state in enumerate(STATES):
    for row, index in enumerate([0, 1, len(frames[state]) - 1]):
        contact.paste(stage(frames[state][index], state, "light"), (column * 320, row * 300))
    old = Image.open(ROOT.parent / "v2" / "native-frames" / state / "001.png")
    comparison.paste(stage(old, state, "light"), (column * 320, 0))
    comparison.paste(stage(frames[state][0], state, "light"), (column * 320, 300))
contact.save(ROOT / "sample-contact.png")
comparison.save(ROOT / "animated-outline-comparison.png")
(ROOT / "extraction-review.json").write_text(json.dumps(extraction, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "preview-encoding.json").write_text(json.dumps(encoding, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"extraction": {state: {key: value for key, value in review.items() if key != "poses"} for state, review in extraction.items()}, "encoding": encoding}, ensure_ascii=False, indent=2))
