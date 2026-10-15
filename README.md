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
