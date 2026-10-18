# portfolio-ep

Source for [ekkehardpetzold.de](https://ekkehardpetzold.de) — static HTML, Tailwind CSS, and project detail pages.

## Setup

```bash
npm install
npm run build:css
```

## Local preview

```bash
npm run dev
```

Open [http://localhost:8000/](http://localhost:8000/). CSS is served with no-cache headers (see `dev-server.py`).

Asset paths are **relative** (not root-absolute `/…`) so the site works on [GitHub Pages project URLs](https://ekkip.github.io/portfolio-ep/) and on a custom domain at the site root. After changing Tailwind classes with background images, run `npm run build:css` — those URLs are resolved from `dist/output.css`, so use `../img/…` in HTML classes.

## GitHub Pages

Pushes to `main` run `.github/workflows/pages.yml`. In repo **Settings → Pages**, source should be **GitHub Actions**.

- **HTML-only edits** (copy, structure, reusing classes already on the site): the workflow **skips** `npm` and deploys with the committed `dist/output.css` — usually much faster.
- **Tailwind source changes** (`src/`, `tailwind.config.js`, `package.json`): full CSS rebuild runs automatically.
- **New Tailwind classes** not yet in `dist/output.css`: either touch a Tailwind source file in the same commit, or run **Actions → Deploy GitHub Pages → Run workflow** with **Rebuild Tailwind CSS** enabled.

After a green deploy, hard-refresh the browser; GitHub’s CDN may cache HTML for up to ~10 minutes.

Project videos (~1.1 GB) are served from **Cloudflare R2** at `https://media.ekkehardpetzold.de/video/…`. GitHub Pages deploys **omit** the local `video/` folder (see workflow). Videos remain in git until you remove them after R2 upload.

### Cloudflare R2 (one-time + when videos change)

1. Add **ekkehardpetzold.de** to your Cloudflare account (Free plan). Nameservers can stay at All-Inkl.
2. Cloud Agent **runtime secrets** (or local shell): `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`. Optional: `CLOUDFLARE_ZONE_ID`.
3. From repo root:

```bash
bash scripts/setup-r2-media.sh
```

4. If DNS is at All-Inkl, add the **CNAME** for `media` that the script prints (or Cloudflare dashboard → R2 → bucket → custom domain).
5. Merge site changes that point HTML at the CDN URL, then deploy.

During development:

```bash
npm run watch:css
```

## Deploy (original workflow)

`build-and-deploy.py` compiles Tailwind, copies assets to a deploy folder, and adds cache-busting query strings on CSS links. Set the destination:

```bash
export DEPLOY_TARGET=/path/to/your/web/root
python3 build-and-deploy.py
```

On macOS, the default `DEPLOY_TARGET` still points at the previous CloudMounter path.

## Structure

| Path | Purpose |
|------|---------|
| `index.html`, `projects/` | Pages |
| `src/input.css` | Tailwind source (component classes `c-*`) |
| `customStyle.css` | Webfont `@font-face` rules |
| `dist/output.css` | Compiled CSS (commit after build, or rebuild locally) |
| `img/`, `video/`, `fonts/` | Media |

Three unused `.mp4` files in `video/` are listed in `.gitignore` because they exceed GitHub’s 100 MB per-file limit. They remain in the Dropbox source archive if you need them locally.
