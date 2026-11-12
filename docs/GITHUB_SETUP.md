# GitHub Pages deployment

Author: Komorebi P.

Build the browser runtime and Windows x64 executable in the private development workspace. Include only the app files required at runtime, the gallery, the executable, and its redistribution notice. Keep the original archive, native and renderer source, and private records outside this repository. Check the staged browser files and EXE for payment content and personal information.

Stage each verified browser update in its own draft release, leaving earlier runtime drafts available for rollback. The current draft is **BiB 116.1 browser update staging**, tagged `v116.1-web.1-runtime`, with the archive named `BiB_Web_Runtime_v116_1.zip`. Leave it as a draft.

Pin the draft's release ID, uploaded asset ID, staging tag, and locally verified SHA-256 in `.github/workflows/pages.yml` on a branch. Open a pull request. After merge, Pages verifies both the pinned identity and checksum before deploying. Manual runs also require the pinned checksum as the `runtime_sha256` input. This keeps later uploads from silently changing what an older revision deploys.

The workflow extracts the archive and uploads the static Pages artifact. It never adds the archive or app files to Git history. The old baseline import workflow has been retired.

After a successful deployment, check the CRT entry page, gallery, and Windows download at https://komorebip.github.io/donothingfoundation/. The `.exe` runs on Windows after download. GitHub Pages runs the browser edition and serves pre-rendered clips.

Browser revision `116.1-web.1` restricts story resets to BiB's own storage keys, preserves signal preferences, adds a touch-accessible intro skip, and keeps the controls reachable in short windows. The Windows download remains the original v116.1 build and does not include this browser update. Native Windows execution and a complete narrative playthrough remain separate verification tasks.
