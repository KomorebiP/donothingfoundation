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

## Browser revision 116.1-web.5

Added an optional passage at the fifth glass fracture. It has five ink-drawn scenes, a hallway that changes on repeated visits, and a separate return route. The main CRT stays at the current fracture while the passage is open. Ambient media pauses without changing the visitor's preferences, and the original sixth crack remains available after returning.

Eight isolated JavaScript checks passed for fracture gating, keyboard focus, audio pause and resume, return handling, the branching scenes, reduced-motion propagation, and keeping the passage outside the checkpoint data. The Windows download stays on the original v116.1 build.

## Browser revision 116.1-web.6

Added a manual receiver after the questions and through the BiB menu after name entry. Two carriers reveal different voices. Holding and tracing the glass commits either a grounded boundary or an opening, with different returns to the existing story. Completed choices change subsequent questions and carrier positions. Only completed choices are saved; cancellation, power-off, and navigation abandon unfinished traces. Keyboard-guided tracing works with mute and reduced motion. The original glass route, optional passage, media, and Windows download are retained.

Seventeen browser interaction checks passed, including actual mouse events, emulated touch cancellation and tracing, native range keys, guided tracing, changed questions, persistence, denied storage, and lifecycle cleanup. Four viewport sizes passed from 320 x 568 to 1440 x 1000, including short landscape. Twenty backup/restore checks passed with the additional validated carrier field; older backups remain supported. Existing browser, gallery, reset, preference, and reduced-motion checks also passed at four viewports. These are headless Edge checks on Windows, rather than physical-phone or native EXE tests.

A fresh continuous three-visit run passed natural receiver entry, the grounded return, the opening and crash, changed questions, the original glass route, and entering/leaving the optional passage at the fifth fracture. It then reached the original ending, terminal card, reset, wake readiness, wake dismissal, and name entry with choice memory, mute, selected volume, and unrelated local/session data retained. This scripted route used real timers; it does not establish exhaustive narrative coverage.

The cumulative thirteen-file overlay reconstructs all 77 runtime files byte-for-byte from the verified web.3 base. Only site status, legacy dialogue integration, controls, and appended styles differ from web.5. The extractor retains exact whitelists for the six-file, eleven-file, and thirteen-file overlays and checks additions before writing. Eleven new deployment-boundary tests cover supported overlays, digests, paths, duplicate entries, symlinks, size limits, base metadata, missing targets, addition collisions, and payload counts. The 27 repository tests passed.

## Browser revision 116.1-web.7

Repaired the readable surfaces after reports of broken screen loading and overlays. Name entry now sits on its own surface with a 16-pixel input and visible submit button. The receiver docks inside the desktop CRT, uses an opaque background, and hides the underlying HUD. Phones use a readable receiver panel and a larger CRT within a clipped viewport; short landscape windows retain the full set. The idle glass offers an explicit power-on action. Browser scripts, styles, imported controls CSS, and passage assets now share the same revision query so returning visitors can fetch a coherent build.

Added an original procedural ink room around the physical set: converging doorways, engraved floorboards, scratched portraits, fine hatching, and peripheral eyes. Pointer gaze redraws on demand and settles to idle. Reduced motion, ambient pause, and a zero background level suppress pointer animation. No new image or audio files were added; existing media and the Windows executable are unchanged.

Fresh checks at 1366 x 768, 1440 x 1000, 390 x 844, 320 x 568, and 740 x 320 cover name-entry font and hit targets, actual form submission, the power action, physical switch visibility, questions, glass bounds, receiver docking, opacity, hidden underlying text, traced results, and stopped redraws under pause/reduced motion/idle. Screenshots of phone questions and short-landscape power entry were visually inspected. Seventeen receiver interaction checks, four receiver layouts, twenty backup/restore checks, and four existing browser/gallery/reset/preference checks also passed. The 27 repository tests passed. These checks use headless Edge and emulated touch on Windows, rather than physical phones or native EXE execution.

The cumulative thirteen-file overlay reconstructs all 77 tested runtime files. The existing controls are preserved as a byte prefix, with presentation appended. The original receiver outcomes, saved choice format, optional passage, media, and ending remain part of the build.

A fresh continuous three-visit run used real timers to reach both receiver outcomes, changed questions, the original glass sequence, passage entry/return at the fifth fracture, the third ending, terminal controls, reset, wake readiness, wake dismissal, and name entry. Choice memory, volume, mute, and unrelated local/session data were retained. This verifies that scripted route, rather than exhaustive narrative coverage.

A warm-cache regression reproduced the missing receiver by loading web.5 assets, serving web.6 in the same browser context, and observing that its unchanged asset URLs reused the cached scripts. Upgrading that context to web.7 fetched all fourteen scripts/styles under the new revision and restored the receiver and readable name-entry surface.

## Browser revision 116.1-web.8

The intro requests video only after its bypass and motion checks. Playback starts the timing of the prologue and a bounded still-image path handles unavailable or slow video. The skip link works before script setup. The CRT defers story audio until interaction and the procedural room renders once after the intro. Name entry accepts ordinary editing until submission, and mobile does not receive forced input focus.

The two utility panels share larger touch targets and independent scrolling. Opening one closes the other. Saved progress stays grouped in the BiB menu. The passage can return during loading and offers a retry after a timeout. Fourteen intro cases and eleven passage cases passed in isolated JavaScript tests. Utility tests covered panel dismissal, preferences, backup access, and coalesced room rendering.

## Browser revision 116.1-web.9

Live review found a horizontal scrollbar in the docked name panel caused by a one-pixel overflow. The panel clips inline overflow and keeps vertical scrolling.

## Browser revision 116.1-web.10

Rebuilt the environment around original generated illustrations, with separate landscape and portrait compositions. The room has dense material detail, damaged wallpaper, deep doorways and a watching face. CRT lighting, a floor shadow, subtle parallax and optical grain give the existing set more depth. Name entry, utility panels and the receiver have a consistent instrument finish. Tuning now resolves a face through the phosphor waveform, using the same artwork. The two optimized WebP images total 973242 bytes; private PNG masters and generation records are not included in Git or the runtime.

The latest intro/video, ordinary name editing, mobile utility, passage retry and inline-overflow fixes from web.9 are retained. Artwork requests and canvas rendering wait until the intro finishes, with surface updates coalesced.

The presentation uses a bounded canvas and stops JavaScript redraws when the pointer settles. Reduced motion and ambient pause stop the light animation and parallax. Artwork failure retains usable name and power controls. A 4K check exposed older duplicate shell fields obscuring the actual TV; those decorative duplicates are omitted on large displays, while the physical CRT and story effects remain. An unnecessary utility backdrop blur was removed.

Six presentation viewports passed, from 320 x 568 through 3840 x 2160, including asset selection, actual hit targets, glass bounds, default receiver buttons, paused/reduced behavior and an artwork-failure fixture. The 4K TV shell was also checked in rendered pixels. A warm-cache upgrade in the same browser context fetched all fourteen scripts/styles under the new revision and loaded both art files. Seventeen receiver interaction checks, four receiver layouts, twenty backup/recovery checks and four browser/gallery/reset checks passed. The updated nested Saved progress and passage toolbar controls were exercised through their current UI. The 29 repository tests passed, including the new production overlay and addition-directory checks.

The seventeen-file cumulative overlay reconstructs all 79 tested runtime files from the original verified web.3 base. The backup implementation remains a byte-identical prefix; receiver state/input/choice code is unchanged after normalizing the paint function and refresh hook. Legacy story, preferences, original media and the Windows executable are byte-identical to web.9. Native Windows execution and physical-phone testing remain separate tasks.

A fresh continuous three-visit run passed both receiver outcomes, changed questions, the original glass sequence, the current passage toolbar's return to the fifth fracture, the third ending, terminal controls, reset, wake readiness, wake dismissal and name entry. It used real timers and retained choice memory, mute, selected volume and foreign local/session data. This is a scripted route rather than exhaustive narrative coverage.

## Browser revision 116.1-web.11

Restored the CRT emphasis after the illustrated room obscured the original outer broadcast. The existing animated field now blends above the room and below the physical set. A separate interference canvas adds flowing cyan/magenta contours and tracking scars, with pointer response and a darker environment grade. The glass has stronger scan structure, phosphor bloom and a slow tracking roll; name entry and the receiver return to signal typography. Input surfaces stay fixed.

The new canvas is capped at 600000 pixels (300000 on phones or low quality), runs at 8 to 12 frames per second while the CRT is on, and stops for pause, reduced motion, zero intensity, hidden pages and the passage. It draws no frames during the intro. All six layout checks passed from 320 x 568 through 3840 x 2160, including hit targets, receiver opacity, rendered 4K shell pixels and the new motion/pixel limits. The warm-cache upgrade fetched all fourteen revised scripts/styles while reusing unchanged artwork. Seventeen receiver and touch checks, twenty backup checks and the 29 repository tests passed.

Four browser/gallery/reset layouts also passed. Five targeted lifecycle checks confirmed the original footage decodes and plays above the room, the interference advances, passage/visibility fixtures suspend and resume it, and pause stops the restored videos.

The existing controls, receiver and backup code remain a byte-identical prefix after normalizing the revision string. Artwork, media, legacy story scripts, preferences and the Windows executable are byte-identical to web.10. The seventeen-file cumulative update reconstructs all 79 runtime files from the pinned web.3 base. This presentation update did not repeat the prior continuous three-visit ending run or native Windows testing.

## Browser revision 116.1-web.12

Reframed the experience around the CRT glass. The display occupies roughly three quarters of the viewport height on desktop; responsive sizing keeps its glass and physical controls reachable. The illustrated room is recessed almost to black, and a mask shades the casing without dimming the image. Separate decorative shell copies are omitted. Original ambient broadcast footage and bounded raster interference now render inside the glass. Name entry is docked inside the display on all viewports and responds to the visible viewport while editing.

The larger layout exposed a race in the opening outcome: the original reveal's queued first-crack animation could overwrite the completed carrier breach. That callback now stands down once the terminal outro begins. The receiver regression explicitly waits through two animation frames before checking that the breach persists. The receiver, backup and controls implementation otherwise remains unchanged before the presentation module; original media, artwork, preferences and Windows bytes are preserved.

The cumulative seventeen-file overlay reconstructs all 79 runtime files. Validation covers six presentation layouts from 320 x 568 through 3840 x 2160, name entry inside the glass, physical hit targets, in-glass effects, motion/pixel limits, an artwork-failure fixture and a simulated reduced visible viewport. The warm-cache upgrade fetches fourteen revised scripts/styles and reuses unchanged art. Seventeen receiver/touch checks, twenty backup checks, four browser/gallery/reset layouts, five playback/lifecycle checks and 29 repository tests passed. A fresh real-timer three-visit route checks both carrier outcomes, original glass, passage return, the third ending, terminal controls, reset and wake readiness/dismissal. Native Windows execution, physical-phone keyboards and exhaustive narrative coverage remain separate verification tasks.

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
