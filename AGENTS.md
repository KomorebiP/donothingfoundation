# Project guidance

Author: Komorebi P.

Continue the existing Do Nothing Foundation / BiB / Signal Studio software. Do not replace it with a demonstration. If `BASELINE_IMPORT.json` or the source directories are absent, report the pending import instead of inventing missing code or claiming the application is ready.

Read `CODEX_START.md`, `SESSION_NOTES.md`, and, after import, `native_source/HANDOFF.md`, `reports/RELEASE_STATUS.json`, `studio_source/docs/HANDOFF.md`, and `studio_source/docs/FAILURE_REGISTER.md`.

Preserve the CRT/VHS aesthetic, exact narrative/questions, supplied media, crack route, ending, full-glass BREAK behavior, input deduplication, and post-name-entry effect gating. Preserve controls, seeded reproducibility, strict resume compatibility, author credit, and user saves. Use procedural rendering, not generated-image substitutes. Never commit credentials, uploaded private audio, browser profiles, save backups, frame caches, or virtual environments.

Canonical websites live in `studio_source/web/`. Native assets and `_site/` are generated. The EXE runs the website; the renderer is separate Python software. Pages cannot run Python or desktop APIs. Never describe a static studio screenshot as a functioning hosted renderer.

Baseline commands after inspecting scripts and obtaining dependency/network approval:

```sh
python -m unittest discover -s tests_repo -v
python tools/build_pages.py
cd studio_source
python -m pip install -r requirements-dev.txt
python -m pytest tests -q
cd ../native_source
python tools/prepare_assets.py --suite ../studio_source
go test ./...
```

Use a virtual environment for local Python work. Native source requires Go 1.23+, studio Python 3.10+. Build development EXEs to a new output path. Native Windows launch/storage behavior and full narrative replay require additional actual testing. Prior Chromium harness tests are not proof of real browser-origin persistence.

Make feature changes on branches and open pull requests unless the user explicitly authorizes direct main changes. Merging main publishes Pages. Do not change payment settings, widen data access, modify other repositories, delete saves, or publish additional private material. Update Markdown handoff, failure records and SESSION_NOTES.md with actual commands, results and skipped checks. Historical reports are not new evidence.
