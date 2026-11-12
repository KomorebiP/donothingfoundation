#!/usr/bin/env python3
"""Hash-locked, non-overwriting migration of the supplied baseline. Author: Komorebi P."""
from __future__ import annotations
import argparse, hashlib, json, shutil, stat, tempfile, zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

EXPECTED_SHA256 = "68a98401d026e56c1c33cac71907c8e3d277ad398157acb69ff252d6ed38bba3"
PREFIX = "BiB_v116_1_Windows_x64"
DIRECTORIES = {"native_source", "studio_source", "licenses", "reports"}
ROOT_FILES = {"README.txt", "Run_Diagnostics.cmd"}
MAX_EXPANDED = 512 * 1024 * 1024
MAX_FILE = 100 * 1024 * 1024
REQUIRED = {"native_source/go.mod", "native_source/main.go", "studio_source/launcher.py", "studio_source/web/bib/index.html", "studio_source/web/donation/index.html"}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def safe_path(name: str) -> PurePosixPath:
    p = PurePosixPath(name)
    if not name or p.is_absolute() or "\\" in name or ":" in name or any(ord(c) < 32 for c in name) or ".." in p.parts or not p.parts or p.parts[0] != PREFIX:
        raise ValueError("Unsafe archive path")
    return p

def import_archive(archive: Path, destination: Path) -> dict:
    destination = destination.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    marker = destination / "BASELINE_IMPORT.json"
    if marker.exists():
        data = json.loads(marker.read_text())
        if data.get("archive_sha256") != EXPECTED_SHA256 or not all((destination / p).is_file() for p in REQUIRED):
            raise ValueError("Import marker/source mismatch; investigate without replacing source")
        return {"status": "already_imported", "source_replaced": False}
    if sha256(archive) != EXPECTED_SHA256:
        raise ValueError("Archive SHA-256 does not match the supplied baseline")
    collisions = [p for p in sorted(DIRECTORIES | ROOT_FILES) if (destination / p).exists()]
    if collisions:
        raise FileExistsError("Refusing to replace existing paths: " + ", ".join(collisions))
    hashes = {}
    with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory(prefix="dnf-import-", dir=destination.parent) as temp:
        infos = z.infolist()
        if len(infos) > 5000 or sum(i.file_size for i in infos) > MAX_EXPANDED:
            raise ValueError("Archive exceeds import limits")
        seen = set()
        planned = []
        for info in infos:
            p = safe_path(info.filename)
            key = str(p).casefold()
            if key in seen:
                raise ValueError("Duplicate archive path")
            seen.add(key)
            if stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError("Symlink archive entry")
            if info.file_size > MAX_FILE:
                raise ValueError("Archive member exceeds size limit")
            if info.is_dir() or len(p.parts) < 2:
                continue
            rel = PurePosixPath(*p.parts[1:])
            if rel.parts[0] not in DIRECTORIES and str(rel) not in ROOT_FILES:
                continue
            if any(x in {".git", ".env", ".venv", "__pycache__", "uploads", "saves", "frame_cache", "browser_profiles"} for x in rel.parts):
                raise ValueError("Private/generated data in source import")
            planned.append((info, rel))
        if not REQUIRED.issubset({str(rel) for _, rel in planned}):
            raise ValueError("Required source files missing")
        for info, rel in planned:
            out = Path(temp).joinpath(*rel.parts)
            out.parent.mkdir(parents=True, exist_ok=True)
            with z.open(info) as src, out.open("wb") as dst:
                shutil.copyfileobj(src, dst)
            hashes[str(rel)] = sha256(out)
        for name in sorted(DIRECTORIES | ROOT_FILES):
            src = Path(temp) / name
            if src.exists():
                shutil.move(str(src), str(destination / name))
    data = {"status": "imported", "archive_sha256": EXPECTED_SHA256, "imported_utc": datetime.now(timezone.utc).isoformat(), "source_files": len(hashes), "files": hashes, "exe_imported_to_git": False, "historical_reports_are_new_tests": False}
    marker.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return {k: v for k, v in data.items() if k != "files"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--destination", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(import_archive(args.archive, args.destination), indent=2))
