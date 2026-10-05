"""Validate the shipped atlas, first-cycle previews, and documentation links."""
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "final"
COUNTS = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]
NAMES = ["idle", "running-right", "running-left", "waving", "jumping", "failed", "waiting", "running", "review"]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    manifest = json.loads((FINAL / "weiweimei/pet.json").read_text(encoding="utf-8"))
    require(manifest["id"] == "weiweimei" and manifest["spriteVersionNumber"] == 2, "Invalid manifest")
    require(manifest["spritesheetPath"] == "spritesheet.webp", "Unexpected sprite path")
    path = FINAL / "weiweimei/spritesheet.webp"
    report = json.loads((FINAL / "validation.json").read_text(encoding="utf-8"))
    require(hashlib.sha256(path.read_bytes()).hexdigest() == report["atlas_sha256"], "Atlas hash differs")
    with Image.open(path) as image:
        require(image.size == (1536, 2288) and image.mode == "RGBA", "Invalid v2 atlas")
        pixels = np.array(image)
    populated = 0
    for row, count in enumerate(COUNTS):
        for column in range(8):
            cell = pixels[row*208:(row+1)*208, column*192:(column+1)*192]
            alpha = cell[:, :, 3]
            if column < count:
                require(np.any(alpha), f"Empty required cell {row}:{column}")
                require(not any(np.any(edge) for edge in [alpha[0], alpha[-1], alpha[:, 0], alpha[:, -1]]),
                        f"Clipped cell {row}:{column}")
                populated += 1
            else:
                require(not np.any(alpha), f"Populated unused cell {row}:{column}")
    for row, name in enumerate(NAMES):
        with Image.open(FINAL / "previews" / f"{name}.webp") as animation:
            require(animation.n_frames >= COUNTS[row], f"Missing preview frames: {name}")
            for column in range(COUNTS[row]):
                animation.seek(column)
                actual = np.array(animation.convert("RGBA"))
                expected = pixels[row*208:(row+1)*208, column*192:(column+1)*192].copy()
                actual[actual[:, :, 3] == 0, :3] = 0
                expected[expected[:, :, 3] == 0, :3] = 0
                require(np.array_equal(actual, expected), f"Preview differs: {name}:{column}")

    links = 0
    for relative in ["README.md", "README.zh-CN.md", "final/USAGE.md", "final/USAGE.zh-CN.md", "final/QA.md", "docs/COMPATIBILITY.md"]:
        document = ROOT / relative
        text = document.read_text(encoding="utf-8")
        targets = re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', text) + re.findall(r'src="([^"]+)"', text)
        for target in targets:
            url = urlsplit(target)
            if url.scheme or target.startswith("#"):
                continue
            require((document.parent / unquote(url.path)).exists(), f"Broken link in {relative}: {target}")
            links += 1
    if (ROOT / ".git").exists():
        result = subprocess.run(["git", "-c", f"safe.directory={ROOT.as_posix()}", "ls-files", "-z"],
                                capture_output=True, check=True)
        names = result.stdout.decode("utf-8").split("\0")
    else:
        names = [path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*")
                 if not any(part in {"__pycache__", ".local"} for part in path.relative_to(ROOT).parts)]
    require(all(name.isascii() for name in names), "Non-English release filename remains")
    print(json.dumps({"atlas_cells": populated, "transparent_unused_cells": 88-populated,
                      "preview_sets": len(NAMES), "local_document_links": links,
                      "english_filenames": True, "passed": True}, indent=2))


if __name__ == "__main__":
    main()
