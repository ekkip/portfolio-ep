# portfolio-ep

Portfolio site for [ekkehardpetzold.de](https://ekkehardpetzold.de).

## Migration status

The production site is static HTML plus compiled `dist/output.css`. To keep a proper Tailwind workflow (`tailwind.config.js`, source CSS with component classes, build scripts), please add your **local source folder** to this repository.

### How to provide the source

1. Zip your project folder (the one you deploy from), or
2. Copy its contents into this repo root (or into a `source/` subfolder), then push or attach it in the agent chat.

Typical files we expect:

- `package.json` and Tailwind/PostCSS config
- Source CSS (e.g. `src/input.css` or similar) with `@layer` / component styles
- All HTML, `customStyle.css`, fonts, `img/`, `video/`, etc.

Once the source is here, the agent will wire up `npm install`, CSS build, local preview, and a clean git layout (including `.gitignore` / Git LFS for large media if needed).

### Interim mirror

A partial copy was pulled from production for reference (HTML, some assets, compiled CSS). It is **not** a substitute for your source tree.
