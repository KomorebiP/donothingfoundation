#!/usr/bin/env python3
"""Build only the public static payload, never the repository root. Author: Komorebi P."""
from __future__ import annotations
import json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {".html", ".css", ".js", ".json", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico", ".mp3", ".mp4", ".ogg", ".wav", ".woff", ".woff2"}

def copy_web(source: Path, target: Path) -> int:
    count = 0
    for p in sorted(source.rglob("*")):
        if p.is_symlink():
            raise ValueError("Symlink in website source")
        if not p.is_file() or p.suffix.lower() not in ALLOWED or p.name == "alignment-check.png" or any(part.startswith(".") for part in p.relative_to(source).parts):
            continue
        dest = target / p.relative_to(source)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)
        count += 1
    return count

def build(root: Path = ROOT) -> dict:
    root = root.resolve()
    output = root / "_site"
    if output.is_symlink():
        raise ValueError("Refusing symlink output directory")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir()
    web = root / "studio_source/web"
    marker = root / "BASELINE_IMPORT.json"
    ready = marker.is_file() and (web / "bib/index.html").is_file() and (web / "donation/index.html").is_file()
    if marker.exists() and not ready:
        raise ValueError("Import marker exists but website source is missing")
    if ready:
        copy_web(web / "bib", output / "experience")
        copy_web(web / "donation", output / "donation")
        donation_index = output / "donation/index.html"
        donation_html = donation_index.read_text(encoding="utf-8")
        for attribute, filename in (("src", "preferences.js"), ("href", "controls.css"), ("src", "controls.js")):
            donation_html = donation_html.replace(
                f'{attribute}="../bib/{filename}"', f'{attribute}="../experience/{filename}"'
            )
        donation_index.write_text(donation_html, encoding="utf-8")
        examples = root / "studio_source/examples/v2_1"
        cards = []
        for name in ("linear_afterimage", "wrapped_field"):
            src = examples / name
            if (src / "signal.mp4").is_file():
                dst = output / "gallery" / name
                dst.mkdir(parents=True, exist_ok=True)
                for filename in ("signal.mp4", "contact_sheet.png", "settings.json"):
                    if (src / filename).is_file(): shutil.copy2(src / filename, dst / filename)
                cards.append('<section><h2>' + name.replace('_', ' ').title() + '</h2><video controls preload="none" playsinline width="640" style="max-width:100%" src="' + name + '/signal.mp4"></video></section>')
        gallery = output / "gallery"
        gallery.mkdir(exist_ok=True)
        (gallery / "index.html").write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Signal Studio examples</title><body style="background:#101612;color:#e5e6d8;font:17px/1.6 system-ui;margin:30px"><a style="color:#d5ef99" href="../">Project home</a><h1>Rendered examples</h1><p>Pre-rendered baseline examples, not a live hosted renderer. Strong motion and flashing imagery may occur. Playback is manual.</p>' + ''.join(cards) + '</body></html>', encoding="utf-8")
        status = "Baseline imported · static website available"
        detail = "The existing source and media are imported. Open the experience above, or use the repository to continue development. Consult Actions for current test and deployment results."
        links = '<a class="button primary" href="experience/">Enter BiB</a><a class="button" href="donation/">Original donation page</a><a class="button" href="gallery/">Rendered examples</a>'
    else:
        status = "Setup stage · awaiting the one-time baseline ZIP upload"
        detail = "The repository and deployment setup are present, but the BiB source and media have not yet been imported. Upload the original ZIP to the prepared draft release and publish that prerelease. The import workflow verifies and installs the source."
        links = ''
    template = (root / "site/index.html").read_text(encoding="utf-8")
    html = template.replace("{{STATUS}}", status).replace("{{DETAIL}}", detail).replace("{{EXPERIENCE_LINKS}}", links)
    (output / "index.html").write_text(html, encoding="utf-8")
    (output / ".nojekyll").touch()
    report = {"baseline_imported": ready, "static_payload_files": len([p for p in output.rglob("*") if p.is_file()]) + 1, "live_renderer": False}
    (output / "site-status.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report

if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
