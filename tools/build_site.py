#!/usr/bin/env python3
"""Render profile/README.md into a static index.html site.

Outputs to ``_site/`` by default, suitable for GitHub Pages. Copies any
images sitting next to the README and writes a CNAME file for the custom
domain.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import markdown

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="icon" type="image/x-icon" href="assets/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="assets/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="assets/apple-touch-icon.png">
<link rel="manifest" href="assets/site.webmanifest">
<style>
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    max-width: 860px;
    margin: 2rem auto;
    padding: 0 1rem;
    line-height: 1.6;
    color: #24292f;
  }}
  img {{ max-width: 100%; height: auto; }}
  a {{ color: #0969da; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  blockquote {{
    border-left: 4px solid #d0d7de;
    padding: .25rem 1rem;
    color: #57606a;
    margin-left: 0;
  }}
  h1, h2, h3 {{ border-bottom: 1px solid #d8dee4; padding-bottom: .3rem; }}
  code {{ background: #f6f8fa; padding: .15em .3em; border-radius: 4px; }}
  hr {{ border: none; border-top: 1px solid #d8dee4; }}
</style>
</head>
<body>
{body}
</body>
</html>
"""

# GitHub-flavored shortcodes the standard markdown library doesn't expand.
EMOJI_SHORTCODES = {
    ":octocat:": '<img src="https://github.githubassets.com/images/icons/emoji/octocat.png" alt="octocat" width="20" height="20" style="vertical-align:middle">',
    ":book:": "📖",
}

IMAGE_EXTS = ("png", "jpg", "jpeg", "gif", "svg", "webp", "ico")


def render(src: Path, title: str) -> str:
    text = src.read_text(encoding="utf-8")
    for code, replacement in EMOJI_SHORTCODES.items():
        text = text.replace(code, replacement)
    body = markdown.markdown(
        text,
        extensions=["extra", "sane_lists"],
        output_format="html5",
    )
    return TEMPLATE.format(title=title, body=body)


def copy_local_images(src_dir: Path, out_dir: Path) -> list[Path]:
    copied: list[Path] = []
    for ext in IMAGE_EXTS:
        for img in src_dir.glob(f"*.{ext}"):
            dest = out_dir / img.name
            shutil.copy2(img, dest)
            copied.append(dest)
    return copied


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="profile/README.md", type=Path)
    parser.add_argument("--output-dir", default="_site", type=Path)
    parser.add_argument("--title", default="STAMPED Principles")
    parser.add_argument(
        "--cname",
        default="stamped-principles.org",
        help="Custom domain to write into a CNAME file. Pass empty to skip.",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    html = render(args.input, args.title)
    index = args.output_dir / "index.html"
    index.write_text(html, encoding="utf-8")
    print(f"wrote {index}")

    for path in copy_local_images(args.input.parent, args.output_dir):
        print(f"copied {path}")

    assets_src = args.input.parent / "assets"
    if assets_src.is_dir():
        assets_dest = args.output_dir / "assets"
        shutil.copytree(assets_src, assets_dest, dirs_exist_ok=True)
        print(f"copied {assets_src} -> {assets_dest}")

    if args.cname:
        cname = args.output_dir / "CNAME"
        cname.write_text(args.cname + "\n", encoding="utf-8")
        print(f"wrote {cname}")


if __name__ == "__main__":
    main()
