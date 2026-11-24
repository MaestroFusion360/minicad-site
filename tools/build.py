"""Generate English and Russian MiniCAD pages from their Markdown sources."""

from __future__ import annotations

import argparse
import html
import re
import struct
from dataclasses import dataclass
from pathlib import Path

from localization import SOURCE_NAMES, localize_page

try:
    from markdown_it import MarkdownIt
except ImportError as exc:
    raise SystemExit("Install dependencies: uv sync --group dev") from exc

ROOT = Path(__file__).resolve().parent.parent
PAGES = (("en", "features.md", "index.html"), ("ru", "features_ru.md", "ru/index.html"))
MD = MarkdownIt("commonmark", {"html": False}).enable("table")

# Navigation, media filenames, and layout are presentation settings. All feature
# descriptions and limitations are read from features.md at build time.
SECTION_META = (
    ("2D CAD", "cad", "2D CAD"),
    ("Technical Drawings", "drawing", "Technical Drawings"),
    ("3D View", "solid", "3D View"),
    ("Milling CAM", "milling", "Milling CAM"),
    ("Tool Library", "tool_library", "Tool Library"),
    ("Turning CAM", "turning", "Turning CAM"),
    ("Turning Simulation", "turning_sim", "Turning Simulation"),
    ("Cutting CAM", "cutting", "Cutting CAM"),
    ("CAM Tools, NC and Playback", "cam", "Tools, NC & Playback"),
    ("CLI", "cli", "CLI"),
)


@dataclass(frozen=True)
class Section:
    name: str
    summary: str
    body: str


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def parse_source(
    source: str, language: str = "en"
) -> tuple[str, str, dict[str, Section]]:
    title = re.search(r"(?m)^#\s+MiniCAD\s+(\d+\.\d+\.\d+)\s*$", source)
    if not title:
        raise ValueError("Expected a '# MiniCAD X.Y.Z' heading")
    headers = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", source))
    if not headers:
        raise ValueError("No Markdown sections found")
    intro = source[title.end() : headers[0].start()].strip()
    if not intro:
        raise ValueError("Add an introductory paragraph below the title")
    sections: dict[str, Section] = {}
    for i, match in enumerate(headers):
        name = match.group(1)
        if language == "ru":
            name = SOURCE_NAMES.get(name, name)
        if name in sections:
            raise ValueError(f"Duplicate section: {name}")
        end = headers[i + 1].start() if i + 1 < len(headers) else len(source)
        body = source[match.end() : end].strip()
        if name != "Limitations":
            # The first paragraph of each capability group also supplies card text.
            split = re.split(r"\n\s*\n", body, maxsplit=1)
            if len(split) < 2 or not split[1].strip():
                raise ValueError(
                    f"Add an introductory paragraph and detail table: {name}"
                )
            sections[name] = Section(name=name, summary=split[0].strip(), body=body)
        else:
            sections[name] = Section(name=name, summary="", body=body)
    expected = {item[0] for item in SECTION_META} | {"Limitations"}
    if set(sections) != expected:
        raise ValueError(
            f"Section mismatch. Missing: {sorted(expected - set(sections))}; extra: {sorted(set(sections) - expected)}"
        )
    return title.group(1), intro, sections


def screenshot(name: str, caption: str, *, hero: bool = False) -> str:
    path = next(
        (
            ROOT / "assets" / "images" / f"{name}.{ext}"
            for ext in ("webp", "png", "jpg", "jpeg")
            if (ROOT / "assets" / "images" / f"{name}.{ext}").is_file()
        ),
        None,
    )
    if path is not None:
        width, height = 1280, 800
        if path.suffix.lower() == ".png":
            with path.open("rb") as source:
                header = source.read(24)
            if header.startswith(b"\x89PNG\r\n\x1a\n") and len(header) == 24:
                width, height = struct.unpack(">II", header[16:24])
        return (
            f'<a class="screenshot-link" href="assets/images/{path.name}" '
            f'data-gallery data-caption="{esc(caption)}" aria-label="Preview: {esc(caption)}">'
            f'<img class="screenshot" src="assets/images/{path.name}" '
            f'alt="MiniCAD — {esc(caption)}" loading="{"eager" if hero else "lazy"}" '
            f'width="{width}" height="{height}"></a>'
        )
    return (
        f'<div class="image-placeholder" role="img" aria-label="Screenshot placeholder: {esc(caption)}">'
        f"<p>{esc(name.upper())}</p><strong>Screenshot placeholder</strong></div>"
    )


def card(name: str, image: str, title: str, section: Section) -> str:
    featured = " feature-wide" if image in {"cad", "solid"} else ""
    return f"""<article class="feature-card{featured}" id="showcase-{esc(image)}">
      <div class="feature-media">{screenshot(image, title)}</div>
      <div class="feature-content">
        <h3>{esc(title)}</h3>
        <p>{MD.renderInline(section.summary)}</p>
        <a class="feature-link" href="#group-{esc(image)}">Explore capabilities</a>
      </div>
    </article>"""


def reference_group(name: str, image: str, title: str, section: Section) -> str:
    return f'''<details class="reference-group" id="group-{esc(image)}" data-area="{esc(image)}">
      <summary><strong>{esc(title)}</strong>
        <span class="disclosure-chevron" aria-hidden="true"></span></summary>
      <div class="reference-body">{MD.render(section.body)}</div>
    </details>'''


def language_switch(language: str) -> str:
    links = []
    for lang, url in (("en", "index.html"), ("ru", "ru/index.html")):
        current = ' aria-current="page"' if language == lang else ""
        links.append(
            f'<a href="{url}" lang="{lang}" hreflang="{lang}"{current}>{lang.upper()}</a>'
        )
    return f'<div class="languages" role="group" aria-label="Language">{"".join(links)}</div>'


def build(source: str, language: str = "en") -> str:
    version, intro, sections = parse_source(source, language)
    showcase_order = (
        "cad",
        "solid",
        "drawing",
        "cam",
        "milling",
        "tool_library",
        "turning",
        "turning_sim",
        "cutting",
        "cli",
    )
    cards = "\n".join(
        card(*meta, sections[meta[0]])
        for image in showcase_order
        for meta in SECTION_META
        if meta[1] == image
    )
    groups = "\n".join(
        reference_group(*meta, sections[meta[0]]) for meta in SECTION_META
    )
    limit_parts = re.split(r"(?m)^### (.+)\n", sections["Limitations"].body)
    limitations = "\n".join(
        f'<details class="scope-group"><summary>{esc(limit_parts[i])}</summary>'
        f"<div>{MD.render(limit_parts[i + 1])}</div></details>"
        for i in range(1, len(limit_parts), 2)
    )
    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#151619">
  <meta name="description" content="MiniCAD {esc(version)}: 2D CAD, technical drawings, 3D B-Rep modeling, Milling, Turning, Cutting CAM, and CLI. Capabilities and limitations.">
  <meta property="og:type" content="website">
  <meta property="og:title" content="MiniCAD {esc(version)} — CAD / CAM / 3D">
  <meta property="og:description" content="MiniCAD features and limitations: 2D CAD, 3D View, Milling, Turning, Cutting, and CLI.">
  <title>MiniCAD {esc(version)} — Features and Limitations</title>
  <link rel="icon" type="image/svg+xml" href="assets/logo.svg">
  <link rel="stylesheet" href="styles.css">
  <link rel="alternate" hreflang="en" href="index.html">
  <link rel="alternate" hreflang="ru" href="ru/index.html">
  <meta property="og:locale" content="{"ru_RU" if language == "ru" else "en_US"}">
  <script src="site.js" defer></script>
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="#top" aria-label="MiniCAD home">
        <img src="assets/logo.svg" width="34" height="34" alt="">
        <span>MiniCAD</span><span class="version">{esc(version)}</span>
      </a>
      <button class="nav-toggle" type="button" aria-controls="site-nav" aria-expanded="false" hidden>Menu <span aria-hidden="true">☰</span></button>
      <nav id="site-nav" aria-label="Main navigation">
        <a href="#overview">Overview</a><a href="#reference">Features</a><a href="#limitations">Limitations</a>
      </nav>
      {language_switch(language)}
      <a class="header-doc" href="features.md">Documentation</a>
    </div>
  </header>
  <main id="main">
    <div id="top" class="container">
      <section class="hero" aria-labelledby="hero-title">
        <div class="hero-copy">
          <h1 id="hero-title">CAD, 3D modeling and CAM in one application.</h1>
          <p class="lead">MiniCAD combines 2D drafting and technical drawings, direct B-Rep solid modeling, CNC toolpaths for milling, turning and cutting, and a command-line interface.</p>
          <div class="hero-actions">
            <a class="button primary" href="#overview">See MiniCAD in action</a>
            <a class="button outline" href="#reference">Browse capabilities</a>
          </div>
        </div>
        <figure class="hero-media">
          {screenshot("hero", "Main workspace", hero=True)}
        </figure>
      </section>
    </div>

    <section class="section overview-section" id="overview">
      <div class="container">
        <h2>Inside MiniCAD</h2>
        <div class="feature-grid">{cards}</div>
      </div>
    </section>

    <section class="section reference-section" id="reference">
      <div class="container">
        <h2>Feature reference</h2>
        <div class="filter-panel">
          <label class="search-control"><span class="sr-only">Search capabilities</span>
            <input id="feature-search" type="search" placeholder="Search features, formats, operations…" autocomplete="off"></label>
          <label class="select-control">Area <select id="area-filter">
            <option value="all">All areas</option>
            <option value="cad">2D CAD</option><option value="drawing">Technical Drawings</option>
            <option value="solid">3D View</option><option value="milling">Milling CAM</option>
            <option value="tool_library">Tool Library</option>
            <option value="turning">Turning CAM</option><option value="turning_sim">Turning Simulation</option><option value="cutting">Cutting CAM</option>
            <option value="cam">Tools, NC & Playback</option><option value="cli">CLI</option>
          </select></label>
          <button class="clear-button" type="button" id="reset-filters">Clear</button>
        </div>
        <div class="reference-tools"><p id="filter-feedback" role="status" aria-live="polite" data-matching="Matching capabilities" data-idle=""></p>
          <div class="reference-actions"><button type="button" id="expand-groups">Expand all</button><button type="button" id="collapse-groups">Collapse all</button></div>
        </div>
        <div class="reference-list">{groups}</div>
        <p class="empty-results" id="no-results" hidden>No matching features. Try another search.</p>
      </div>
    </section>

    <section class="section limitations-section" id="limitations">
      <div class="container">
        <h2>Limitations</h2>
        <div class="limit-content">{limitations}</div>
      </div>
    </section>
  </main>
<footer>
  <div class="container">
    <div class="footer-inner">
      <div class="footer-info">
        <a class="brand" href="#top"
          ><img src="assets/logo.svg" width="36" height="36" alt="" /><span
            >MiniCAD</span
          ></a
        >
        <p>2D drafting, solid modeling and CNC toolpaths.</p>
      </div>
      <div class="footer-links">
        <a href="features.md">Documentation</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 MaestroFusion360</span>
      {language_switch(language)}
      <a href="LICENSE">Website license (MIT)</a>
    </div>
  </div>
</footer>
    <dialog
      id="image-viewer"
      aria-label="Image or video preview"
      aria-describedby="viewer-caption"
    >
      <div class="viewer-toolbar">
        <p id="viewer-caption" aria-live="polite"></p>
      </div>
      <button
        type="button"
        class="viewer-close"
        aria-label="Close preview"
        autofocus
      >
        <span aria-hidden="true">✕</span>
      </button>
      <div class="viewer-stage">
        <img alt="" hidden />
      </div>
      <div class="viewer-footer">
        <a class="viewer-original" target="_blank" rel="noopener"
          >Open original ↗</a
        >
      </div>
    </dialog>
</body>
</html>
"""
    return localize_page(document) if language == "ru" else document


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Check whether both pages are current"
    )
    args = parser.parse_args()
    rendered_pages = []
    versions = set()
    for language, source_name, output_name in PAGES:
        source = ROOT / source_name
        if not source.is_file():
            parser.error(f"{source_name} not found in the repository root")
        content = source.read_text(encoding="utf-8")
        versions.add(parse_source(content, language)[0])
        rendered_pages.append((source_name, output_name, build(content, language)))
    if len(versions) != 1:
        parser.error(
            "features.md and features_ru.md must declare the same MiniCAD version"
        )
    for source_name, output_name, rendered in rendered_pages:
        output = ROOT / output_name
        if args.check:
            if not output.is_file() or output.read_text(encoding="utf-8") != rendered:
                raise SystemExit(f"{output_name} is outdated; run: npm run build")
            print(f"{output_name} is current")
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(rendered, encoding="utf-8", newline="\n")
            print(f"Generated {output_name} from {source_name}")


if __name__ == "__main__":
    main()
