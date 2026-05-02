# stamped-principles/.github

The entry point to the [STAMPED Principles](https://stamped-principles.org)
GitHub organization.

This repository serves two purposes:

1. **Organization profile.** GitHub renders [`profile/README.md`](profile/README.md)
   on the [organization landing page](https://github.com/stamped-principles).

2. **Project website.** The same [`profile/README.md`](profile/README.md) is
   rendered into `index.html` and published to
   <https://stamped-principles.org> via GitHub Pages.

**Duplication is evil!** A single source (`profile/README.md`) drives both
the GitHub org page and the public website. To update either, edit
`profile/README.md` — the [Pages workflow](.github/workflows/pages.yml)
will rebuild and redeploy the site automatically.

## Local preview

```bash
pip install markdown
python tools/build_site.py
# then open _site/index.html
```

## Layout

- [`profile/README.md`](profile/README.md) — single source of truth for
  the org profile and the website body.
- [`tools/build_site.py`](tools/build_site.py) — Markdown → `index.html`
  renderer; also writes a `CNAME` and copies any images sitting next to
  the README.
- [`.github/workflows/pages.yml`](.github/workflows/pages.yml) — builds
  and deploys to GitHub Pages on pushes to `main` that touch the profile,
  the script, or the workflow.
