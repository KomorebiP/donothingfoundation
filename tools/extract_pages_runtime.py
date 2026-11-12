#!/usr/bin/env python3
"""Validate and unpack the Do Nothing Foundation Pages runtime."""

import argparse
import hashlib
import json
import shutil
import stat
from pathlib import Path, PurePosixPath
from zipfile import ZipFile


WINDOWS_APP = PurePosixPath("downloads/BiB_v116_1_Windows_x64.exe")
ROOT_FILES = {
    PurePosixPath("index.html"),
    PurePosixPath(".nojekyll"),
    PurePosixPath("site-status.json"),
}
EXTRA_FILES = {
    WINDOWS_APP,
    PurePosixPath("downloads/Go_LICENSE.txt"),
    PurePosixPath("experience/index.html"),
}
RUNTIME_DIRS = tuple(PurePosixPath(name) for name in ("web/bib", "gallery", "desktop"))
WEB_TYPES = {".html", ".css", ".js", ".json", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp",
             ".ico", ".mp3", ".mp4", ".ogg", ".wav", ".woff", ".woff2"}
REQUIRED = ROOT_FILES | {
    PurePosixPath("web/bib/index.html"),
    PurePosixPath("downloads/Go_LICENSE.txt"),
    WINDOWS_APP,
}


def runtime_files(archive):
    entries = archive.infolist()
    if len(entries) > 500 or sum(info.file_size for info in entries) > 500 * 1024**2:
        raise ValueError("The runtime ZIP exceeds deployment limits")
    paths = {}
    names = set()
    for info in entries:
        path = PurePosixPath(info.filename)
        mode = stat.S_IFMT(info.external_attr >> 16)
        if (not path.parts or path.is_absolute() or ".." in path.parts or "\\" in info.filename
                or ":" in info.filename or any(ord(char) < 32 for char in info.filename)
                or info.filename.rstrip("/") != str(path)
                or mode not in (0, stat.S_IFREG, stat.S_IFDIR)):
            raise ValueError(f"Unsafe runtime path {info.filename!r}")
        if info.is_dir():
            continue
        if mode == stat.S_IFDIR or info.file_size > 100 * 1024**2:
            raise ValueError(f"Unexpected runtime entry {str(path)!r}")
        if path not in ROOT_FILES | EXTRA_FILES:
            if (not any(path.is_relative_to(directory) for directory in RUNTIME_DIRS)
                    or path.suffix not in WEB_TYPES or any(part.startswith(".") for part in path.parts)):
                raise ValueError(f"File outside the public runtime: {str(path)!r}")
        if str(path).casefold() in names:
            raise ValueError(f"Duplicate runtime path {str(path)!r}")
        names.add(str(path).casefold())
        paths[path] = info
    if not REQUIRED <= paths.keys():
        raise ValueError("The runtime ZIP is missing a required file")
    if any(parent in paths for path in paths for parent in path.parents):
        raise ValueError("Runtime paths collide with file names")
    return paths


def extract(source, sha256, destination):
    with source.open("rb") as binary:
        actual = hashlib.file_digest(binary, "sha256").hexdigest()
    if actual != sha256:
        raise ValueError("Runtime ZIP checksum mismatch")
    with ZipFile(source) as archive:
        paths = runtime_files(archive)
        status = json.loads(archive.read("site-status.json"))
        if status.get("runtime_deployed") is not True or status.get("live_renderer") is not False:
            raise ValueError("The runtime status must describe the static browser application")
        with archive.open(paths[WINDOWS_APP]) as executable:
            if executable.read(2) != b"MZ":
                raise ValueError("The Windows download is missing its executable header")
        destination.mkdir()
        for path, info in paths.items():
            target = destination.joinpath(*path.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info) as entry, target.open("wb") as output:
                shutil.copyfileobj(entry, output)
    return len(paths)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("sha256")
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    print(f"Verified and unpacked {extract(args.source, args.sha256, args.destination)} runtime files.")
