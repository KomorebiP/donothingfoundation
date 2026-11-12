# Session notes

Author: Komorebi P.
Date: 2026-11-12

## Public delivery update

The public repository deploys the runtime only. The original source import workflow was retired. Use the runtime staging draft and the Pages workflow described in docs/GITHUB_SETUP.md. The earlier migration notes below document the scaffold before this change.

## Browser revision 116.1-web.1

Recovered the deployed Pages artifact into a private local working copy. Reproduced unrelated-storage deletion in all five legacy story-reset routines, then restricted them to exact BiB story/session keys. Preserved the visitor name, wake handling, and visual/audio preferences. Added a visible intro-skip button and a scrollable controls panel for short windows.

Local verification covered the five reset routines, actual query-reset navigation, saved preferences, name entry, intro skipping, system reduced motion, and playback of both gallery clips. Browser checks passed at 1440 x 1000, 390 x 844, 320 x 568, and 740 x 320 in headless Edge on Windows, with no page errors or failed asset responses. These checks are not a complete narrative playthrough or native EXE runtime test. The Windows executable's bytes are unchanged.

The new runtime has 72 files and is staged in a separate draft. Deployment now pins its release, asset, tag, and checksum; the earlier draft remains available for rollback. Application files, private test scripts, and detailed evidence remain outside the public repository.

## Migration scope

Created a separate GitHub project for Do Nothing Foundation, leaving the research repositories untouched. Baseline is BiB Desktop 116.1.0 plus Signal Studio 2.1 source. Added a hash-locked baseline importer, static Pages builder, CI configuration and Codex handoff.

## Transfer limitation

The chat-mounted 158,375,826-byte ZIP could not be uploaded through the connected release action: that action requires a remote FileUploadable reference, not a chat-local path. The remote tool workspace did not contain the mounted archive. No successful source/media transfer should be inferred from repository creation alone.

The prepared draft release accepts the existing ZIP through GitHub's upload interface. Publishing it starts the import workflow. This is a one-time step. Consult BASELINE_IMPORT.json and Actions for actual import/deployment state.

## Local import and Pages verification

Recovered the original ZIP and matched its SHA-256 to the importer's expected digest. Ran `python3 tools/import_baseline.py ../dnf-input/BiB_v116_1_Windows_x64.zip` in a fresh checkout and imported 232 files. The Pages builder rewrites three donation-page asset URLs to match the deployed experience directory. The canonical web sources and original archive were unchanged.

`python3 -m unittest discover -s tests_repo -v` passed 16 tests. `python3 tools/build_pages.py` produced a 71-file static site with the experience, donation page, and two rendered examples. These results describe the local build. The draft still needed its release asset when these checks were run.

## Next verification

Check real website navigation and origin storage after deployment. Rerun Python and Go suites. Verify full narrative and native Windows behavior separately. Preserve historical reports without upgrading their claims.
