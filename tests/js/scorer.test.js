import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, it } from "node:test";

const require = createRequire(import.meta.url);

const root = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const scorer = require(join(root, "docs/assets/scorer.js"));
const truthTable = JSON.parse(
  readFileSync(join(root, "tests/fixtures/outcome-truth-table.json"), "utf8")
);

describe("scorer.js truth table parity", () => {
  for (const testCase of truthTable.cases) {
    it(testCase.id, () => {
      const result = scorer.evaluateScreen(testCase.input);
      assert.equal(result.level, testCase.expected.level);
      for (const ruleId of testCase.expected.rule_ids) {
        assert.ok(
          result.ruleIds.includes(ruleId),
          `expected ${ruleId} in ${result.ruleIds.join(", ")}`
        );
      }
    });
  }

  it("missing-field cases never produce green", () => {
    const missingCases = truthTable.cases.filter(
      (testCase) =>
        testCase.id.includes("missing") || testCase.expected.rule_ids.includes("A9")
    );
    assert.ok(missingCases.length > 0);
    for (const testCase of missingCases) {
      const result = scorer.evaluateScreen(testCase.input);
      assert.notEqual(result.level, "green");
    }
  });
});
