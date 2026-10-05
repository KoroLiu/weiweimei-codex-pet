"""Build a portable release ZIP without installing the pet."""
import hashlib
import json
import zipfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent

def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()

def build_delivery():
    package = ROOT / "weiweimei"
    config = json.loads((package / "pet.json").read_text(encoding="utf-8"))
    if config["spriteVersionNumber"] != 2 or config["spritesheetPath"] != "spritesheet.webp":
        raise ValueError("Unexpected pet manifest")
    atlas = package / "spritesheet.webp"
    with Image.open(atlas) as image:
        if image.size != (1536, 2288) or image.mode != "RGBA":
            raise ValueError("Unexpected v2 sprite dimensions or transparency")
    validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
    if sha(atlas) != validation["atlas_sha256"]:
        raise ValueError("Atlas differs from the validated asset")

    html = (ROOT / "preview.html").read_text(encoding="utf-8")
    html = html.replace("url('spritesheet.webp')", "url('weiweimei/spritesheet.webp')")
    for name in ["look-directions.png", "all-frames-contact.png", "edges-light-dark.png"]:
        html = html.replace(f'src="{name}"', f'src="previews/{name}"')
    html = html.replace("`${name}.webp`", "`previews/${name}.webp`")
    (ROOT / "index.html").write_text(html, encoding="utf-8")

    files = [ROOT / name for name in [
        "Install-Pet.ps1", "USAGE.md", "USAGE.zh-CN.md", "QA.md", "validation.json",
        "index.html", "preview-composite-review.json",
    ]]
    files += sorted(package.glob("*")) + sorted((ROOT / "previews").glob("*"))
    files += sorted((ROOT / "sources").glob("*prompt.txt"))
    for path in files:
        if not path.is_file() or not path.relative_to(ROOT).as_posix().isascii():
            raise ValueError(f"Missing file or non-English package path: {path.name}")
    checksums = [f"{sha(path)}  {path.relative_to(ROOT).as_posix()}" for path in files]
    (ROOT / "SHA256SUMS.txt").write_text("\n".join(checksums) + "\n", encoding="utf-8")
    files.append(ROOT / "SHA256SUMS.txt")

    target = ROOT / "weiweimei-codex-pet-v1.zip"
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise ValueError("Corrupt ZIP")
        for path in files:
            name = path.relative_to(ROOT).as_posix()
            if hashlib.sha256(archive.read(name)).hexdigest() != sha(path):
                raise ValueError(f"ZIP content differs: {name}")
    report = {
        "zip": target.name, "bytes": target.stat().st_size, "sha256": sha(target),
        "entries": len(files), "zip_integrity_verified": True,
        "asset_validation_verified": True, "installation_required": False,
    }
    (ROOT / "delivery.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (ROOT / "ZIP-SHA256.txt").write_text(f"{sha(target)}  {target.name}\n", encoding="utf-8")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    build_delivery()
