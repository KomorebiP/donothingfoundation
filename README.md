# Do Nothing Foundation

Author: Komorebi P.

BiB is an interactive CRT/VHS website and desktop application. Signal Studio is the separate Python procedural-effects renderer.

## Current setup

This repository starts as a verified import/deployment scaffold. The actual software is available here only after `BASELINE_IMPORT.json`, `native_source/`, and `studio_source/` appear. A setup homepage is not the full BiB experience.

Project site: https://komorebip.github.io/donothingfoundation/

## One-time source import

Before publication, read `docs/PUBLICATION_REVIEW.md`. The existing payment code contains a recipient email address and has not been altered.

1. Open the prepared **BiB Desktop v116.1 baseline** draft in Releases.
2. Attach the existing `BiB_v116_1_Windows_x64.zip` (158,375,826 bytes) without renaming or repacking it.
3. Publish the prerelease. **Import baseline** verifies its SHA-256, imports source and media, and invokes the Pages deployment. This is a migration of the existing project, not a rewrite.

The import accepts only SHA-256 `68a98401d026e56c1c33cac71907c8e3d277ad398157acb69ff252d6ed38bba3`. The executable stays in the release archive rather than Git history. The source import refuses to overwrite an existing source tree.

After a successful import, later changes are ordinary commits and pull requests. Pages deploys website changes merged into `main`. See `AGENTS.md`, `CODEX_START.md`, and `docs/GITHUB_SETUP.md`.

## Layout after import

- `native_source/`: Go desktop launcher and build tools.
- `studio_source/`: Python renderer, recovery engine, studio, websites, media, tests and documentation.
- `studio_source/web/`: canonical website sources. Do not edit generated copies.
- `site/`, `tools/build_pages.py`: project homepage and static-site assembly.
- `reports/`: historical baseline evidence. Do not present it as tests rerun here.

## Boundaries

GitHub Pages serves the website, not the Python renderer or desktop HTTP API. The baseline EXE is unsigned and native Windows execution remains unverified. Complete three-run narrative replay, payment flows and photosensitivity safety are not certified. No new media/software license is granted by publishing this repository. Retain original rights notices.
