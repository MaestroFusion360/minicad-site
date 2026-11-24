"use strict";

// The HTML is usable without JavaScript; these controls provide progressive
// enhancement for navigation, searching, and section disclosure.
document.documentElement.classList.add("js");

const navToggle = document.querySelector(".nav-toggle");
const nav = document.querySelector("#site-nav");

if (navToggle && nav) {
  navToggle.hidden = false;
  navToggle.addEventListener("click", () => {
    const open = navToggle.getAttribute("aria-expanded") !== "true";
    navToggle.setAttribute("aria-expanded", String(open));
    nav.classList.toggle("is-open", open);
  });
  nav.addEventListener("click", (event) => {
    if (!event.target.closest("a")) return;
    navToggle.setAttribute("aria-expanded", "false");
    nav.classList.remove("is-open");
  });
  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    navToggle.setAttribute("aria-expanded", "false");
    nav.classList.remove("is-open");
  });
}

const search = document.getElementById("feature-search");
const area = document.getElementById("area-filter");
const reset = document.getElementById("reset-filters");
const feedback = document.getElementById("filter-feedback");
const empty = document.getElementById("no-results");
const groups = [...document.querySelectorAll(".reference-group")];

const normalize = (value) =>
  value.toLocaleLowerCase(document.documentElement.lang || "en").trim();

function applyFilters() {
  if (!search || !area) return;
  const query = normalize(search.value);
  const active = query !== "" || area.value !== "all";
  let matches = 0;

  for (const group of groups) {
    const inArea = area.value === "all" || area.value === group.dataset.area;
    const headingMatches =
      query &&
      normalize(group.querySelector("summary")?.textContent ?? "").includes(
        query,
      );
    const summaryMatches =
      query &&
      normalize(
        group.querySelector(".reference-body > p")?.textContent ?? "",
      ).includes(query);
    let groupMatches = 0;

    for (const row of group.querySelectorAll("tbody tr")) {
      const show =
        inArea &&
        (!query ||
          headingMatches ||
          summaryMatches ||
          normalize(row.textContent).includes(query));
      row.hidden = !show;
      if (show) groupMatches++;
    }
    group.hidden = !inArea || groupMatches === 0;
    if (active && groupMatches > 0) group.open = true;
    matches += groupMatches;
  }

  if (feedback)
    feedback.textContent = active
      ? feedback.dataset.matching
      : feedback.dataset.idle;
  if (empty) empty.hidden = matches !== 0;
}

search?.addEventListener("input", applyFilters);
area?.addEventListener("change", applyFilters);

function clearFilters() {
  if (search) search.value = "";
  if (area) area.value = "all";
  applyFilters();
}

reset?.addEventListener("click", () => {
  clearFilters();
  search?.focus();
});

document.getElementById("expand-groups")?.addEventListener("click", () => {
  groups
    .filter((group) => !group.hidden)
    .forEach((group) => (group.open = true));
});

document.getElementById("collapse-groups")?.addEventListener("click", () => {
  groups.forEach((group) => (group.open = false));
});

function revealHash() {
  let targetId;
  try {
    targetId = decodeURIComponent(window.location.hash.slice(1));
  } catch {
    return;
  }
  if (!targetId) return;
  const target = document.getElementById(targetId);
  if (!target) return;
  if (target.closest(".reference-group")?.hidden || target.hidden)
    clearFilters();
  let ancestor = target;
  while (ancestor) {
    if (ancestor.tagName === "DETAILS") ancestor.open = true;
    ancestor = ancestor.parentElement;
  }
}

window.addEventListener("hashchange", revealHash);
document.addEventListener("click", (event) => {
  const link = event.target.closest('a[href^="#"]');
  if (link && link.hash === window.location.hash) revealHash();
});

applyFilters();
revealHash();

const viewer = document.querySelector("#image-viewer");
if (viewer && typeof viewer.showModal === "function") {
  const image = viewer.querySelector("img");
  const stage = viewer.querySelector(".viewer-stage");
  const videoPlaceholder = document.createElement("div");
  videoPlaceholder.className = "video-placeholder";
  const caption = viewer.querySelector("#viewer-caption");
  const original = viewer.querySelector(".viewer-original");
  let opener = null;
  let inlineVideo = null;
  document.querySelectorAll("button[data-video-viewer]").forEach((button) => {
    button.hidden = false;
  });

  function openViewer(trigger, title, url) {
    opener = trigger;
    caption.textContent = title;
    original.href = url;
    viewer.showModal();
    document.body.classList.add("viewer-open");
  }

  document.addEventListener("click", (event) => {
    const trigger = event.target.closest(
      "a[data-gallery], [data-video-viewer]",
    );
    if (
      !trigger ||
      event.button !== 0 ||
      event.ctrlKey ||
      event.metaKey ||
      event.shiftKey ||
      event.altKey
    )
      return;
    if (trigger.hasAttribute("data-video-viewer")) {
      const source = document.querySelector(".video-preview video");
      const url = source?.currentSrc || source?.querySelector("source")?.src;
      if (!source || !url) return;
      event.preventDefault();
      inlineVideo = source;
      source.pause();
      image.hidden = true;
      videoPlaceholder.style.aspectRatio = `${source.width} / ${source.height}`;
      source.replaceWith(videoPlaceholder);
      stage.append(source);
      openViewer(trigger, source.getAttribute("aria-label") || "", url);
      // The click explicitly requests playback; reduced-motion never autoplays.
      source.play().catch(() => {});
      return;
    }
    const source = trigger.querySelector("img");
    if (!source) return;
    event.preventDefault();
    image.hidden = false;
    image.src = trigger.href;
    image.alt = source.alt;
    openViewer(trigger, source.alt, trigger.href);
  });
  viewer
    .querySelector(".viewer-close")
    .addEventListener("click", () => viewer.close());
  viewer.addEventListener("close", () => {
    document.body.classList.remove("viewer-open");
    if (inlineVideo) {
      inlineVideo.pause();
      videoPlaceholder.replaceWith(inlineVideo);
      inlineVideo = null;
    }
    image.removeAttribute("src");
    image.hidden = true;
    opener?.focus({ preventScroll: true });
    opener = null;
  });
}
