import importlib.util, json, tempfile, unittest, zipfile, stat
from unittest.mock import patch
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class SetupTests(unittest.TestCase):
    def test_safe_archive_path(self):
        mod = load("import_baseline")
        self.assertEqual(str(mod.safe_path(mod.PREFIX + "/native_source/main.go")), mod.PREFIX + "/native_source/main.go")

    def test_unsafe_archive_paths(self):
        mod = load("import_baseline")
        for name in ("../escape", "/absolute", "C:/escape", mod.PREFIX + "/../escape", mod.PREFIX + "/bad\\path", "another/source.py", mod.PREFIX + "/bad\nname"):
            with self.subTest(name=name), self.assertRaises(ValueError): mod.safe_path(name)

    def test_bad_hash_does_not_import(self):
        mod = load("import_baseline")
        with tempfile.TemporaryDirectory() as td:
            archive = Path(td) / "bad.zip"
            archive.write_bytes(b"not the baseline")
            target = Path(td) / "target"
            with self.assertRaises(ValueError): mod.import_archive(archive, target)
            self.assertFalse((target / "BASELINE_IMPORT.json").exists())

    def test_pending_site_is_honest(self):
        mod = load("build_pages")
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "site").mkdir()
            (root / "site/index.html").write_text((ROOT / "site/index.html").read_text())
            result = mod.build(root)
            html = (root / "_site/index.html").read_text()
            self.assertFalse(result["baseline_imported"])
            self.assertIn("awaiting", html)
            self.assertNotIn('href="experience/"', html)
            self.assertFalse(result["live_renderer"])

    def test_ready_site_copies_only_public_web(self):
        mod = load("build_pages")
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "site").mkdir()
            (root / "site/index.html").write_text((ROOT / "site/index.html").read_text())
            (root / "BASELINE_IMPORT.json").write_text('{}')
            for name in ("bib", "donation"):
                p = root / "studio_source/web" / name
                p.mkdir(parents=True)
                (p / "index.html").write_text('<html>fixture</html>')
                (p / ".env").write_text('private fixture')
                (p / "server.py").write_text('private fixture')
            result = mod.build(root)
            self.assertTrue(result["baseline_imported"])
            self.assertTrue((root / "_site/experience/index.html").exists())
            self.assertFalse((root / "_site/experience/.env").exists())
            self.assertFalse((root / "_site/experience/server.py").exists())
            self.assertIn('href="experience/"', (root / "_site/index.html").read_text())

    def test_broken_import_does_not_fake_ready(self):
        mod = load("build_pages")
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "BASELINE_IMPORT.json").write_text('{}')
            with self.assertRaises(ValueError): mod.build(root)

    def test_workflows_do_not_use_pull_request_target(self):
        for p in (ROOT / ".github/workflows").glob("*.yml"):
            self.assertNotIn("pull_request_target", p.read_text())

    def make_fixture(self, path, extra=None, omit=None):
        mod = load("import_baseline")
        with zipfile.ZipFile(path, "w") as z:
            for rel in sorted(mod.REQUIRED - set(omit or [])):
                z.writestr(mod.PREFIX + "/" + rel, "fixture source")
            z.writestr(mod.PREFIX + "/BiB_v116_1_Windows_x64.exe", b"fixture binary")
            z.writestr(mod.PREFIX + "/SHA256SUMS.txt", "fixture old hashes")
            for info, content in extra or []: z.writestr(info, content)
        return mod

    def test_import_and_idempotent_resume_preserve_edits(self):
        with tempfile.TemporaryDirectory() as td:
            archive = Path(td) / "fixture.zip"
            mod = self.make_fixture(archive)
            target = Path(td) / "repo"
            with patch.object(mod, "EXPECTED_SHA256", mod.sha256(archive)):
                result = mod.import_archive(archive, target)
                self.assertEqual(result["status"], "imported")
                json.loads((target / "BASELINE_IMPORT.json").read_text())
                self.assertFalse((target / "BiB_v116_1_Windows_x64.exe").exists())
                self.assertFalse((target / "SHA256SUMS.txt").exists())
                main = target / "native_source/main.go"
                main.write_text("later user edit")
                self.assertEqual(mod.import_archive(archive, target)["status"], "already_imported")
                self.assertEqual(main.read_text(), "later user edit")

    def test_import_rejects_collision(self):
        with tempfile.TemporaryDirectory() as td:
            archive = Path(td) / "fixture.zip"
            mod = self.make_fixture(archive)
            target = Path(td) / "repo"
            (target / "native_source").mkdir(parents=True)
            with patch.object(mod, "EXPECTED_SHA256", mod.sha256(archive)), self.assertRaises(FileExistsError): mod.import_archive(archive, target)

    def test_import_rejects_missing_source(self):
        with tempfile.TemporaryDirectory() as td:
            archive = Path(td) / "fixture.zip"
            mod = self.make_fixture(archive, omit=["native_source/main.go"])
            with patch.object(mod, "EXPECTED_SHA256", mod.sha256(archive)), self.assertRaises(ValueError): mod.import_archive(archive, Path(td) / "repo")

    def test_import_rejects_traversal_before_writing(self):
        with tempfile.TemporaryDirectory() as td:
            archive = Path(td) / "fixture.zip"
            mod = self.make_fixture(archive, [("BiB_v116_1_Windows_x64/../escape", "no")])
            target = Path(td) / "repo"
            with patch.object(mod, "EXPECTED_SHA256", mod.sha256(archive)), self.assertRaises(ValueError): mod.import_archive(archive, target)
            self.assertFalse((target / "native_source").exists())

    def test_import_rejects_symlink(self):
        with tempfile.TemporaryDirectory() as td:
            archive = Path(td) / "fixture.zip"
            info = zipfile.ZipInfo("BiB_v116_1_Windows_x64/native_source/link")
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            mod = self.make_fixture(archive, [(info, "../outside")])
            with patch.object(mod, "EXPECTED_SHA256", mod.sha256(archive)), self.assertRaises(ValueError): mod.import_archive(archive, Path(td) / "repo")

    def test_import_rejects_duplicate_case_paths(self):
        with tempfile.TemporaryDirectory() as td:
            archive = Path(td) / "fixture.zip"
            mod = self.make_fixture(archive, [("BiB_v116_1_Windows_x64/native_source/MAIN.GO", "duplicate")])
            with patch.object(mod, "EXPECTED_SHA256", mod.sha256(archive)), self.assertRaises(ValueError): mod.import_archive(archive, Path(td) / "repo")

    def test_import_rejects_private_directory(self):
        with tempfile.TemporaryDirectory() as td:
            archive = Path(td) / "fixture.zip"
            mod = self.make_fixture(archive, [("BiB_v116_1_Windows_x64/studio_source/uploads/private.wav", "private")])
            with patch.object(mod, "EXPECTED_SHA256", mod.sha256(archive)), self.assertRaises(ValueError): mod.import_archive(archive, Path(td) / "repo")

    def test_site_status_json_count(self):
        mod = load("build_pages")
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "site").mkdir()
            (root / "site/index.html").write_text((ROOT / "site/index.html").read_text())
            result = mod.build(root)
            status = json.loads((root / "_site/site-status.json").read_text())
            self.assertEqual(result, status)
            self.assertEqual(status["static_payload_files"], len([p for p in (root / "_site").rglob("*") if p.is_file()]))

    def test_import_dispatches_main_branch_workflows(self):
        workflow = (ROOT / ".github/workflows/import-baseline.yml").read_text()
        self.assertIn('gh workflow run ci.yml --repo "$GITHUB_REPOSITORY" --ref main', workflow)
        self.assertIn('gh workflow run pages.yml --repo "$GITHUB_REPOSITORY" --ref main', workflow)
        self.assertIn('actions: write', workflow)
        self.assertNotIn('git push --force', workflow)

if __name__ == "__main__": unittest.main()

