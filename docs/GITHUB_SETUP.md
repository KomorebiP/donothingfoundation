# GitHub Pages deployment

Author: Komorebi P.

Build the browser runtime and Windows x64 executable in the private development workspace. Include only the app files required at runtime, the gallery, the executable, and its redistribution notice. Keep the original archive, native and renderer source, and private records outside this repository. Check the staged browser files and EXE for payment content and personal information.

Attach BiB_Web_Runtime_v116_1.zip to the **BiB v116.1 runtime staging** draft release. Leave it as a draft. In Actions, run **Pages** on main with the local ZIP SHA-256 as the runtime_sha256 input. The workflow verifies and extracts the ZIP, then uploads the static Pages artifact. It never adds the archive or app files to Git history. The old baseline import workflow has been retired.

After a successful deployment, check the CRT entry page, gallery, and Windows download at https://komorebip.github.io/donothingfoundation/. The `.exe` runs on Windows after download. GitHub Pages runs the browser edition and serves pre-rendered clips.
