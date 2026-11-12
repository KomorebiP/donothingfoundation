# Session notes

Author: Komorebi P.
Date: 2026-11-12

## Public delivery update

The public repository deploys the runtime only. The original source import workflow was retired. Use the runtime staging draft and the Pages workflow described in docs/GITHUB_SETUP.md. The earlier migration notes below document the scaffold before this change.

## Browser revision 116.1-web.1

Recovered the deployed Pages artifact into a private local working copy. Reproduced unrelated-storage deletion in all five legacy story-reset routines, then restricted them to exact BiB story/session keys. Preserved the visitor name, wake handling, and visual/audio preferences. Added a visible intro-skip button and a scrollable controls panel for short windows.

Local verification covered the five reset routines, actual query-reset navigation, saved preferences, name entry, intro skipping, system reduced motion, and playback of both gallery clips. Browser checks passed at 1440 x 1000, 390 x 844, 320 x 568, and 740 x 320 in headless Edge on Windows, with no page errors or failed asset responses. These checks are not a complete narrative playthrough or native EXE runtime test. The Windows executable's bytes are unchanged.

The new runtime has 72 files and is staged in a separate draft. Deployment now pins its release, asset, tag, and checksum; the earlier draft remains available for rollback. Application files, private test scripts, and detailed evidence remain outside the public repository.

## Browser revision 116.1-web.2

Reproduced a story cue overriding an audio-level setting of zero. Separated the story's cue volume from the visitor's selected level, updated all 28 cue-volume assignments, and applied the same level to procedural Web Audio. Media routed through the music analyser receives the user gain once. Added a persistent mute button that retains the selected level and synchronizes across tabs.

Kept utility controls outside legacy story input handling and above the terminal input layer. The final card's input catcher now owns its events, preventing older capture handlers from scheduling competing resets. Removed the obsolete override of native immediate event propagation.

Recorded-media level checks, rendered procedural-audio samples, analyser routing, reload persistence, cross-tab mute, and the media fallback without Web Audio passed. Four-viewport browser checks and all five storage-reset regressions passed. The scripted three-run route reached the final ending with mute enabled, using real timers and keyboard input. The terminal controls, reset, and wake dismissal also passed a separate coda fixture. These checks use disposable browser contexts; existing user saves and the Windows executable are unchanged.

A final continuous run against the completed update passed from visitor-name entry through all three runs, the ending, terminal card, reset, wake dismissal, and return to name entry. The visitor name, selected volume, mute, and unrelated local/session data were retained. This verifies that scripted path in headless Edge on Windows; it does not establish exhaustive branch coverage or native EXE behavior.

## Browser revision 116.1-web.3

Added browser checkpoint backups to the existing BiB menu. JSON downloads include the visitor name, completed signals, countdown state, and signal settings. Selecting a file previews its progress and audio/motion settings; confirmation preserves a recovery copy of the current checkpoint before restoring. Cancel, invalid files, and storage access failures leave progress intact. Partial write failures attempt rollback, with the recovery copy retained. Other origin data is excluded from both export and restore.

Twenty fresh backup checks passed, covering download/restore/recovery, all 13 checkpoint fields, invalid and oversized files, unsupported versions and foreign keys, prototype-like keys, simulated local/session write failures, older settings, late asynchronous reads, and unavailable storage. Preview/restore controls passed at 1440 x 1000, 390 x 844, 320 x 568, and 740 x 320. A terminal input fixture verified that downloading a backup does not answer the final card. The existing four-viewport browser suite also passed.

The 72-file runtime differs from the prior runtime only in controls.js, appended menu styles, and site status. Earlier control code is preserved as a byte prefix; the story, audio preferences module, original media, and executable are byte-identical. The previous three-run narrative evidence remains scoped to web.2; this update's fresh checks cover backup behavior and browser regressions. Application source, private test files, and detailed evidence stay outside this delivery repository.

## Browser revision 116.1-web.4

Ambient video and its timing manifest are deferred until the CRT needs them. Reduced motion uses the active phase's poster. The spark canvas skips empty frames, four legacy effects use visible-page timers at their existing update cadences, and three identical GIF references share one asset. The shorter prologue retains all footage. Automatic waits after name entry are 4.9 seconds shorter in total. Two existing interruptions now have uneven holds. Browser history restoration dismisses an interrupted prologue.

JavaScript syntax checks and isolated runtime checks covered deferred media, reduced motion, ambient pause, mute, checkpoint data, and restoration from browser history. The clock retained its rendered glyphs and styles in 58 seeded comparisons. These checks do not measure physical-device frame rate or replay the complete story. The Windows download remains the original v116.1 build.

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
