import js from "@eslint/js";
import globals from "globals";

export default [
  {
    files: ["site.js", "tools/*.mjs", "*.config.mjs"],
    rules: js.configs.recommended.rules,
    languageOptions: { ecmaVersion: "latest" },
  },
  { files: ["site.js"], languageOptions: { globals: globals.browser } },
  {
    files: ["*.config.mjs", "tools/*.mjs"],
    languageOptions: { globals: globals.node },
  },
];
