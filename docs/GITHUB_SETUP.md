# GitHub Pages deployment

Author: Komorebi P.

Build the browser runtime and Windows x64 executable in the private development workspace. Include only the app files required at runtime, the gallery, the executable, and its redistribution notice. Keep the original archive, native and renderer source, and private records outside this repository. Check the staged browser files and EXE for payment content and personal information.

Stage each verified browser update in its own draft release, leaving earlier runtime drafts available for rollback. The complete browser base is `BiB_Web_Runtime_v116_1.zip` in `v116.1-web.3-runtime`. The six changed web.4 files are in `BiB_Web_Update_116_1_web_4.zip` in `v116.1-web.4-runtime`. Leave both releases as drafts.

Pin the release IDs, asset IDs, staging tags, and locally verified SHA-256 values in `.github/workflows/pages.yml` on a branch. Open a pull request. After merge, Pages verifies both archives and applies the browser files to the verified base. Manual runs require the update ZIP's checksum as the `runtime_sha256` input.

The workflow extracts the archive and uploads the static Pages artifact. It never adds the archive or app files to Git history. The old baseline import workflow has been retired.

After a successful deployment, check the CRT entry page, gallery, and Windows download at https://komorebip.github.io/donothingfoundation/. The `.exe` runs on Windows after download. GitHub Pages runs the browser edition and serves pre-rendered clips.

Browser revision `116.1-web.2` retains the scoped resets, intro skip, and scrollable controls from the first browser update. Story sound cues now respect the selected audio level and persistent mute. Utility controls stay usable during the terminal sequence without answering the final card. The final card uses one reset handler, preserving the wake-up sequence.

Revision `116.1-web.3` adds device-local checkpoint backup and restore through the existing BiB menu. Restore validates the file, previews progress and settings, saves the previous checkpoint for recovery, and reloads after explicit confirmation. Only known BiB storage keys are included or replaced. The story, audio implementation, original media, and Windows download are unchanged from web.2.

The Windows download remains the original v116.1 build and does not include the browser updates. Native Windows execution, physical-phone testing, and exhaustive narrative branch coverage remain separate verification tasks.
