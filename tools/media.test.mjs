import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";
import { JSDOM } from "jsdom";

const script = fs.readFileSync(new URL("../site.js", import.meta.url), "utf8");
function page(t, language) {
  const name = language === "ru" ? "ru/index.html" : "index.html";
  const html = fs.readFileSync(new URL(`../${name}`, import.meta.url), "utf8");
  const dom = new JSDOM(html, {
    url: `https://example.test/minicad/${name}`,
    runScripts: "outside-only",
  });
  t.after(() => dom.window.close());
  const { window } = dom;
  const dialog = window.document.querySelector("dialog");
  dialog.showModal = () => {
    dialog.open = true;
  };
  dialog.close = () => {
    dialog.open = false;
    dialog.dispatchEvent(new window.Event("close"));
  };
  window.eval(script);
  return { window, dialog, document: window.document };
}
for (const language of ["en", "ru"]) {
  test(`${language}: all eleven screenshots open in-page and preserve the original source`, (t) => {
    const { document, dialog } = page(t, language);
    const links = [...document.querySelectorAll(".screenshot-link")];
    assert.equal(links.length, 11);
    for (const link of links) {
      link.click();
      assert.equal(dialog.open, true);
      assert.equal(dialog.querySelector("img").src, link.href);
      assert.equal(
        document.querySelector("#viewer-caption").textContent,
        link.querySelector("img").alt,
      );
      document.querySelector(".viewer-close").click();
      assert.equal(dialog.open, false);
      assert.equal(document.activeElement, link);
      assert.equal(document.body.classList.contains("viewer-open"), false);
    }
  });
  test(`${language}: EGP viewer uses a close icon and original link without gallery controls`, (t) => {
    const { document, dialog } = page(t, language);
    const link = document.querySelector(".screenshot-link");
    link.click();
    assert.equal(dialog.querySelector(".viewer-original").href, link.href);
    assert.equal(
      dialog.querySelector(".viewer-close").textContent.trim(),
      "\u2715",
    );
    assert.equal(dialog.querySelector(".viewer-controls"), null);
    dialog.close();
    assert.equal(document.activeElement, link);
  });
  test(`${language}: filtering and clear restore the feature reference`, (t) => {
    const { window, document } = page(t, language);
    const area = document.querySelector("#area-filter");
    area.value = "solid";
    area.dispatchEvent(new window.Event("change"));
    assert.equal(
      document.querySelector("#filter-feedback").textContent,
      language === "ru" ? "Найденные возможности" : "Matching capabilities",
    );
    assert.deepEqual(
      [...document.querySelectorAll(".reference-group")]
        .filter((g) => !g.hidden)
        .map((g) => g.id),
      ["group-solid"],
    );
    document.querySelector("#reset-filters").click();
    assert.equal(
      document.querySelectorAll(".reference-group:not([hidden])").length,
      10,
    );
  });
}
