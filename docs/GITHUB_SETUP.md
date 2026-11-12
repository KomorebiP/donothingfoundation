# GitHub and Pages workflow

Author: Komorebi P.

## Complete the one-time import

Open Releases, edit the existing v116.1-baseline draft, attach `BiB_v116_1_Windows_x64.zip`, wait for the browser upload to finish, then publish it as a prerelease. Do not replace it with GitHub's automatically generated Source code ZIP.

The workflow checks the exact archive hash before extracting. Only native_source, studio_source, licenses, reports, README.txt and Run_Diagnostics.cmd are imported. The EXE remains in the release archive. Re-running a completed import does not replace source changes. If a release was published before upload completed, attach the file and manually run **Import baseline** from Actions.

The importer checks paths, symlinks, duplicate names, per-file and expanded sizes, and source presence. It rejects conflicting target directories. This is validation for the known archive, not a general untrusted ZIP service.

## Deployment

Pages uses GitHub Actions. The Pages workflow builds `_site/` from the homepage and the canonical web sources. It never publishes repository root, Python server code, tests, reports or local saves as the site payload. `.htaccess` is not deployed because Pages does not execute Apache configuration. Relative paths retain project-subdirectory compatibility.

After import: homepage `/donothingfoundation/`, BiB `/donothingfoundation/experience/`, donation page `/donothingfoundation/donation/`, and rendered examples `/donothingfoundation/gallery/`. Before import, only a clearly labeled setup homepage exists.

The import workflow explicitly dispatches Checks and Pages on main because GITHUB_TOKEN-created commits do not trigger ordinary push workflows. Dispatching on main also avoids treating a release tag as the Pages deployment branch. Subsequent user/Codex merges into main trigger Pages normally. Review the separate Actions results before claiming tests or deployment succeeded. The import job needs contents:write and actions:write; the Pages job has its own pages/id-token permissions.

## Development and releases

Codex works on this repository. Use branches and pull requests. Merging main publishes the static site. Python renders run in a capable local/cloud compute environment, not Pages. Large EXEs/ZIPs belong in Releases, not Git history. The unsigned baseline EXE remains unverified on native Windows. Existing media licenses are not changed.

## References checked on 2026-11-12

- https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- https://learn.chatgpt.com/docs/environments/cloud-environments
