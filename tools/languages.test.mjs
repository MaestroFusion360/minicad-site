import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";
import { JSDOM } from "jsdom";

const read = (name) =>
  fs.readFileSync(new URL(`../${name}`, import.meta.url), "utf8");

test("Russian source preserves English reference coverage and literal commands", () => {
  const en = read("features.md");
  const ru = read("features_ru.md");
  assert.equal(
    ru.match(/^# MiniCAD (.+)$/m)[1],
    en.match(/^# MiniCAD (.+)$/m)[1],
  );
  for (const pattern of [/^## /gm, /^### /gm, /^\|/gm, /^- /gm]) {
    assert.equal(
      [...ru.matchAll(pattern)].length,
      [...en.matchAll(pattern)].length,
    );
  }
  assert.deepEqual(
    [...ru.matchAll(/`([^`]+)`/g)].map((m) => m[1]),
    [...en.matchAll(/`([^`]+)`/g)].map((m) => m[1]),
  );
});

for (const language of ["en", "ru"]) {
  test(`${language}: language switch, shared resources and localized labels`, (t) => {
    const name = language === "ru" ? "ru/index.html" : "index.html";
    const dom = new JSDOM(read(name), {
      url: `https://example.test/minicad/${name}`,
    });
    t.after(() => dom.window.close());
    const doc = dom.window.document;
    assert.equal(doc.documentElement.lang, language);
    const groups = [...doc.querySelectorAll(".languages")];
    assert.equal(groups.length, 2);
    for (const group of groups) {
      assert.equal(group.querySelector("[aria-current]").lang, language);
      assert.equal(
        new URL(group.querySelector('[lang="en"]').href).pathname,
        "/minicad/index.html",
      );
      assert.equal(
        new URL(group.querySelector('[lang="ru"]').href).pathname,
        "/minicad/ru/index.html",
      );
    }
    assert.equal(
      new URL(doc.querySelector("script[src]").src).pathname,
      "/minicad/site.js",
    );
    assert.equal(doc.querySelectorAll(".reference-group").length, 10);
    assert.equal(doc.querySelectorAll(".scope-group").length, 4);
    assert.equal(doc.querySelectorAll(".screenshot").length, 11);
    assert.equal(
      new URL(doc.querySelector("footer .footer-links a").href).pathname,
      language === "ru" ? "/minicad/features_ru.md" : "/minicad/features.md",
    );
    if (language === "ru") {
      assert.equal(doc.querySelector("#reset-filters").textContent, "Сбросить");
      assert.equal(
        doc.querySelector("#feature-search").placeholder,
        "Поиск возможностей, форматов, операций…",
      );
      assert.equal(
        doc.querySelector(".viewer-close").getAttribute("aria-label"),
        "Закрыть просмотр",
      );
      assert.match(
        doc.querySelector(".viewer-original").textContent,
        /Открыть оригинал/,
      );
      assert.match(doc.querySelector("#group-solid").textContent, /отверстия/i);
      assert.equal(
        doc.querySelectorAll('a[href^="https://github.com/"]').length,
        0,
      );
    }
  });
}
