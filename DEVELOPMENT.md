# MiniCAD website development

A standalone MiniCAD capabilities and limitations site in English and Russian. Technical content comes from `features.md` and its complete Russian translation `features_ru.md`; the current version comes from their `# MiniCAD X.Y.Z` headings. The site is independent of the private MiniCAD source repository.

## Build

Requires uv and Node.js 26 (the CI version), or a compatible Node.js 22.22.2+ or 24.15.0+ release. uv manages Python and the local `.venv`.

```sh
uv sync --locked --group dev
npm ci
npm run build
npm run check
```

To build the page, start the local server and open the browser on Windows:

```powershell
.\start.ps1
```

Press Enter in the terminal to stop the server. To use another port: `.\start.ps1 -Port 8001`. If the requested port is occupied, the script automatically selects a free port and opens that address.

Run these commands from the repository root. `tools/` holds the generator, the local server, the resource checks and the tests; the generator writes `index.html` and `ru/index.html` at the root.

`index.html` and `ru/index.html` are generated together. Edit `features.md` and `features_ru.md` together, not the generated HTML. Keep the `# MiniCAD X.Y.Z` heading, introductory paragraph, and eleven section headings (`2D CAD`, `Technical Drawings`, `3D View`, `Milling CAM`, `Tool Library`, `Turning CAM`, `Turning Simulation`, `Cutting CAM`, `CAM Tools, NC and Playback`, `CLI`, `Limitations`). The first paragraph in each capability section supplies the overview card description. The Markdown tables supply the detailed descriptions.

The site is static. JavaScript only adds search, category filtering, and expand/collapse controls. Screenshot previews use the same full-viewport viewer as Easy G-Code Plot. There are no analytics or runtime dependencies on remote services.

## Screenshots

Add screenshots to `assets/images/` using the names below. WebP, PNG, JPG and JPEG are supported (in that priority order if several formats share a name). Any image dimensions are accepted; screenshots keep their original proportions without cropping. Clicking an image opens an in-page preview. Escape or the close icon closes the preview. Open original opens the full-size file. Without JavaScript the image opens directly.

- `hero.png` — main application workspace
- `cad.png` — 2D CAD
- `drawing.png` — technical drawings
- `solid.png` — 3D View
- `milling.png` — milling toolpaths
- `tool_library.png` — tool library
- `turning.png` — turning toolpaths
- `turning_sim.png` — turning simulation
- `cutting.png` — cutting
- `cam.png` — tools / NC / playback
- `cli.png` — command-line interface

If a file is missing, the generator uses a screenshot placeholder. Run `npm run build` after adding screenshots. If filenames or extensions change, update the corresponding links in `README.md` as well.

## Publishing

Deploy the static files `index.html`, `styles.css`, `site.js`, `assets/`, `ru/`, `features.md`, `features_ru.md`, `LICENSE`, and `.nojekyll` to any static host. The `tools/` directory and the build configuration are not required on the host. No automatic publication is configured in this repository. For GitHub Pages, select **Settings → Pages → Deploy from a branch → main → / (root)** after pushing the checked files. The default project URLs are `https://maestrofusion360.github.io/minicad-site/` and `https://maestrofusion360.github.io/minicad-site/ru/`.

Both Markdown sources are linked from the website and will be public when deployed. It is a standalone, publication-oriented description, not a copy of the private source-code documentation. Check its contents before publishing.

## Project files

- `README.md` — public MiniCAD overview and screenshots
- `DEVELOPMENT.md` — this guide
- `features.md` — English source of capabilities and limitations
- `features_ru.md` — Russian source of capabilities and limitations
- `index.html`, `ru/index.html` — generated pages
- `styles.css` — responsive layout
- `site.js` — progressive UI enhancements
- `assets/` — logo and screenshots
- `tools/build.py` — Markdown-to-HTML generator
- `tools/localization.py` — Russian interface labels and heading mapping
- `tools/serve.py` — local static server started by `start.ps1`
- `tools/check-site.mjs` — local resources, anchors and HTML structure checks
- `tools/*.test.mjs` — page, language and media tests

Everything under `tools/` is development-only; the published site consists of the files listed in Publishing.

## License

The site source is MIT licensed; see `LICENSE`. This does not relicense the MiniCAD application or third-party assets. The Lucide logo retains its ISC license in `assets/LUCIDE-LICENSE`.

## Checks

`npm run check` verifies the generated page, Ruff, ESLint, Stylelint, formatting, local resources and anchors, screenshot gallery, filters, footer and license. Scripts in `tools/` target this repository root; no sibling repository, download resolver or videos are required. `uv.lock` and `package-lock.json` lock development dependencies.

## Languages

English is generated at `index.html`, Russian at `ru/index.html`, following the EGP directory layout. The header and footer have EN/RU switches; CSS, JavaScript and all eleven screenshots are shared through relative URLs, including when hosted under a subdirectory. The Russian page links to `features_ru.md`.

`npm run build` (or `uv run python tools/build.py`) builds both pages. `npm run build:check` checks both without writing. Both sources must declare the same version and retain all nine section headings. Russian headings are mapped to stable section identifiers in `tools/localization.py`, which also contains the Russian interface labels. Search feedback, accessible labels, screenshot captions, metadata and preview labels are localized. The EGP preview behavior is shared by both pages.

## CI

`.github/workflows/ci.yml` runs on every push, pull request and manual dispatch on Windows with uv, Python 3.13, Node.js 26 and locked dependencies installed by `uv sync --locked --group dev` and `npm ci`.

The job runs `npm run check`: generated EN/RU pages must match their Markdown sources, Ruff/ESLint/Stylelint and formatting must pass, local resources and anchors must exist, and the site tests must pass. CI checks the committed HTML without rebuilding it first, so a forgotten local rebuild fails the check. Run `npm run build` before committing content changes, and `npm run check` for the same checks locally. GitHub Actions starts after the commit is pushed to GitHub; a local commit alone does not start CI.

`.gitattributes` enforces LF for text files even when Windows Git has `core.autocrlf=true`, matching Prettier's `endOfLine: lf`. Images and fonts remain binary.
