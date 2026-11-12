"""Exercise the public overlay boundary before any runtime files are replaced."""
import hashlib
import importlib.util
import json
import stat
import tempfile
import unittest
import warnings
from pathlib import Path
from zipfile import ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("runtime", ROOT / "tools/extract_pages_runtime.py")
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)


class BrowserUpdateTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.base = self.root / "base"
        self.status = {"runtime_deployed": True, "live_renderer": False,
                       "windows_sha256": "original", "browser_revision": "old", "static_payload_files": 72}
        self.files = {name: b"updated" for name in runtime.INTERACTIVE_UPDATE}
        self.files["site-status.json"] = json.dumps({**self.status, "static_payload_files": 77, "browser_revision": "new",
                                                    "browser_changes": ["receiver"]}).encode()
        self.make_base(self.base)

    def make_base(self, directory):
        for name in self.files.keys() - runtime.BROWSER_ADDITIONS:
            path = directory / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(json.dumps(self.status).encode() if name == "site-status.json" else b"original")

    def archive(self, files=None, extra=()):
        path = self.root / "update.zip"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with ZipFile(path, "w") as archive:
                for name, content in (self.files if files is None else files).items():
                    archive.writestr(name, content)
                for name, content in extra:
                    archive.writestr(name, content)
        return path, hashlib.sha256(path.read_bytes()).hexdigest()

    def reject_unchanged(self, archive, digest):
        before = {p.relative_to(self.base): p.read_bytes() for p in self.base.rglob("*") if p.is_file()}
        with self.assertRaises(ValueError):
            runtime.apply_browser_update(archive, digest, self.base)
        self.assertEqual(before, {p.relative_to(self.base): p.read_bytes() for p in self.base.rglob("*") if p.is_file()})

    def test_all_supported_versions(self):
        for names in (runtime.PERFORMANCE_UPDATE, runtime.BROWSER_UPDATE, runtime.INTERACTIVE_UPDATE):
            with self.subTest(files=len(names)):
                destination = self.root / str(len(names))
                self.make_base(destination)
                files = {name: self.files[name] for name in names}
                if names == runtime.PERFORMANCE_UPDATE:
                    status = json.loads(files["site-status.json"])
                    status["static_payload_files"] = 72
                    files["site-status.json"] = json.dumps(status).encode()
                archive, digest = self.archive(files)
                self.assertEqual(runtime.apply_browser_update(archive, digest, destination), len(names))
                for name in names:
                    self.assertEqual((destination / name).read_bytes(), files[name])

    def test_wrong_digest(self):
        archive, _ = self.archive()
        self.reject_unchanged(archive, "0" * 64)

    def test_partial_set(self):
        self.files.pop("web/bib/controls.js")
        self.reject_unchanged(*self.archive())

    def test_unlisted_and_traversal_paths(self):
        for name in ("native_source/main.go", "../escape", "downloads/new.exe", "web/bib/Controls.js"):
            with self.subTest(name=name):
                self.reject_unchanged(*self.archive(extra=[(name, b"unexpected")]))
        self.assertFalse((self.root / "escape").exists())

    def test_duplicate(self):
        self.reject_unchanged(*self.archive(extra=[("web/bib/controls.js", b"duplicate")]))

    def test_symlink(self):
        info = ZipInfo("web/bib/controls.js")
        info.create_system = 3
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        files = {k: v for k, v in self.files.items() if k != info.filename}
        self.reject_unchanged(*self.archive(files, [(info, b"../outside")]))

    def test_oversized_file(self):
        self.files["web/bib/controls.js"] = b"x" * (2 * 1024**2 + 1)
        self.reject_unchanged(*self.archive())

    def test_native_metadata_cannot_change(self):
        self.files["site-status.json"] = json.dumps({**self.status, "windows_sha256": "different"}).encode()
        self.reject_unchanged(*self.archive())

    def test_missing_base_target(self):
        (self.base / "web/bib/controls.js").unlink()
        self.reject_unchanged(*self.archive())

    def test_addition_cannot_replace_existing_file(self):
        (self.base / "web/bib/breach.js").write_bytes(b"existing")
        self.reject_unchanged(*self.archive())

    def test_payload_count_must_match_additions(self):
        status = json.loads(self.files["site-status.json"])
        status["static_payload_files"] = 72
        self.files["site-status.json"] = json.dumps(status).encode()
        self.reject_unchanged(*self.archive())


if __name__ == "__main__":
    unittest.main()
