#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create a static publish directory and a ZIP for manual deployment."""
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
ARCHIVE = ROOT / "netlify-deploy.zip"
SITE_FILES = (
    "index.html",
    "tour.html",
    "tour_data.json",
    "cover.jpg",
    "_headers",
    "_redirects",
)
SITE_DIRS = ("images", "thumbs", "viewer")


def main():
    sources = [ROOT / name for name in (*SITE_FILES, *SITE_DIRS)]
    missing = [path.name for path in sources if not path.exists()]
    if missing:
        raise SystemExit("Missing site files: " + ", ".join(missing))

    # Resolve and check the fixed output directory before recursive deletion.
    if DIST.is_symlink() or DIST.resolve() != ROOT / "dist":
        raise SystemExit("The publish directory must stay inside the project.")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    for name in SITE_FILES:
        shutil.copy2(ROOT / name, DIST / name)
    for name in SITE_DIRS:
        shutil.copytree(ROOT / name, DIST / name)

    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(DIST.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(DIST).as_posix())
    print(f"Publish directory: {DIST}")
    print(f"Deployment archive: {ARCHIVE} ({ARCHIVE.stat().st_size / 1048576:.1f} MiB)")


if __name__ == "__main__":
    main()
