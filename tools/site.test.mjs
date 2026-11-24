import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";
import { JSDOM } from "jsdom";
test("MiniCAD version, footer and site license match the project", () => {
  const root = new URL("../", import.meta.url);
  const version = fs
    .readFileSync(new URL("features.md", root), "utf8")
    .match(/^# MiniCAD (\d+\.\d+\.\d+)/m)[1];
  const dom = new JSDOM(fs.readFileSync(new URL("index.html", root), "utf8"));
  try {
    const document = dom.window.document;
    assert.ok(document.title.includes(version));
    assert.ok(document.querySelector("footer .footer-links"));
    assert.ok(document.querySelector('footer a[href="LICENSE"]'));
    assert.match(
      fs.readFileSync(new URL("LICENSE", root), "utf8"),
      /^MIT License/,
    );
    assert.equal(document.querySelectorAll(".image-placeholder").length, 0);
    assert.equal(document.querySelectorAll(".screenshot").length, 11);
    for (const link of document.querySelectorAll(".screenshot-link"))
      assert.equal(link.hasAttribute("target"), false);
  } finally {
    dom.window.close();
  }
});
