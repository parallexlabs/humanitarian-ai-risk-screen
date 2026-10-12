/**
 * Client-side risk screen scorer. No data leaves the browser.
 * evaluateScreen(data) mirrors src/ai_risk_screen/outcome.py predicates.
 */

(function (root, factory) {
  "use strict";
  if (typeof module !== "undefined" && module.exports) {
    module.exports = factory();
  } else {
    root.HumanitarianRiskScorer = factory();
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  var STEP_KEYS = [
    "purpose",
    "people",
    "data",
    "tool",
    "output",
    "human_control",
    "monitoring",
  ];

  var RULE_DRIVING_BOOLEAN_PATHS = [
    ["steps", "data", "includes_prohibited_input"],
    ["steps", "tool", "tool_approved"],
    ["steps", "output", "high_stakes_decision"],
    ["steps", "output", "output_reviewable"],
    ["steps", "human_control", "safe_remedy_available"],
    ["steps", "data", "privacy_review_needed"],
    ["steps", "people", "protection_review_needed"],
    ["steps", "people", "partner_review_needed"],
    ["steps", "monitoring", "controlled_pilot_required"],
    ["steps", "data", "includes_personal_data"],
    ["steps", "data", "includes_sensitive_non_personal"],
  ].concat(
    STEP_KEYS.map(function (key) {
      return ["steps", key, "complete"];
    })
  );

  var OUTCOME_LABELS = {
    green: "Green: low risk, proceed with checks",
    amber: "Amber: pause for review and controlled pilot",
    red: "Red: do not use",
  };

  function getValue(data, path) {
    var current = data;
    for (var i = 0; i < path.length; i += 1) {
      if (typeof current !== "object" || current === null) {
        return undefined;
      }
      current = current[path[i]];
    }
    return current;
  }

  function isTrue(data, path) {
    return getValue(data, path) === true;
  }

  function isFalse(data, path) {
    return getValue(data, path) === false;
  }

  function nonEmptyString(data, path) {
    var value = getValue(data, path);
    if (value === undefined || value === null) {
      return false;
    }
    return String(value).trim() !== "";
  }

  function allStepsComplete(data) {
    var steps = data.steps;
    if (typeof steps !== "object" || steps === null) {
      return false;
    }
    return STEP_KEYS.every(function (key) {
      var step = steps[key];
      return typeof step === "object" && step !== null && step.complete === true;
    });
  }

  function missingRuleDrivingBoolean(data) {
    return RULE_DRIVING_BOOLEAN_PATHS.some(function (path) {
      var value = getValue(data, path);
      return typeof value !== "boolean";
    });
  }

  function evaluateScreen(data) {
    var redReasons = [];
    var redIds = [];

    if (isTrue(data, ["steps", "data", "includes_prohibited_input"])) {
      redIds.push("R1");
      redReasons.push("Prohibited input declared in the data step");
    }
    if (isFalse(data, ["steps", "tool", "tool_approved"])) {
      redIds.push("R2");
      redReasons.push("Tool is not on the organization's approved list");
    }
    if (
      isTrue(data, ["steps", "output", "high_stakes_decision"]) &&
      isFalse(data, ["steps", "output", "output_reviewable"])
    ) {
      redIds.push("R3");
      redReasons.push("High-stakes decision with output that cannot be human-reviewed");
    }
    if (isFalse(data, ["steps", "human_control", "safe_remedy_available"])) {
      redIds.push("R4");
      redReasons.push("No safe remedy path for people affected by errors");
    }

    if (redReasons.length > 0) {
      return {
        level: "red",
        label: OUTCOME_LABELS.red,
        reasons: redReasons,
        ruleIds: redIds,
      };
    }

    var amberReasons = [];
    var amberIds = [];

    if (missingRuleDrivingBoolean(data)) {
      amberIds.push("A9");
      amberReasons.push("One or more required rule-driving fields are missing");
    }
    if (isTrue(data, ["steps", "data", "privacy_review_needed"])) {
      amberIds.push("A1");
      amberReasons.push("Privacy review required before use");
    }
    if (isTrue(data, ["steps", "people", "protection_review_needed"])) {
      amberIds.push("A2");
      amberReasons.push("Protection review required before use");
    }
    if (isTrue(data, ["steps", "people", "partner_review_needed"])) {
      amberIds.push("A3");
      amberReasons.push("Partner consultation review required before use");
    }
    if (isTrue(data, ["steps", "monitoring", "controlled_pilot_required"])) {
      amberIds.push("A4");
      amberReasons.push("Controlled pilot required before wider rollout");
    }
    if (
      isTrue(data, ["steps", "data", "includes_personal_data"]) &&
      !nonEmptyString(data, ["steps", "data", "authority_basis"])
    ) {
      amberIds.push("A5");
      amberReasons.push("Personal data involved without documented authority");
    }
    if (
      isTrue(data, ["steps", "data", "includes_sensitive_non_personal"]) &&
      !nonEmptyString(data, ["steps", "data", "minimization_plan"])
    ) {
      amberIds.push("A6");
      amberReasons.push("Sensitive non-personal data without minimization sign-off");
    }
    if (isTrue(data, ["steps", "output", "high_stakes_decision"])) {
      amberIds.push("A7");
      amberReasons.push("High-stakes decision requires enhanced human review");
    }
    if (isFalse(data, ["steps", "output", "output_reviewable"])) {
      amberIds.push("A8");
      amberReasons.push("Output verification not yet confirmed as reviewable");
    }
    if (!allStepsComplete(data)) {
      amberIds.push("A0");
      amberReasons.push("One or more screen steps are not marked complete");
    }

    if (amberReasons.length > 0) {
      return {
        level: "amber",
        label: OUTCOME_LABELS.amber,
        reasons: amberReasons,
        ruleIds: amberIds,
      };
    }

    return {
      level: "green",
      label: OUTCOME_LABELS.green,
      reasons: ["All steps complete; no red or amber triggers"],
      ruleIds: ["G1"],
    };
  }

  function bool(id) {
    var el = document.getElementById(id);
    return el ? el.checked : false;
  }

  function val(id) {
    var el = document.getElementById(id);
    return el ? el.value.trim() : "";
  }

  function formToScreenData() {
    return {
      steps: {
        purpose: { complete: bool("complete_purpose") },
        people: {
          partner_review_needed: bool("partner_review_needed"),
          protection_review_needed: bool("protection_review_needed"),
          complete: bool("complete_people"),
        },
        data: {
          includes_prohibited_input: bool("includes_prohibited_input"),
          includes_personal_data: bool("includes_personal_data"),
          includes_sensitive_non_personal: bool("includes_sensitive_non_personal"),
          privacy_review_needed: bool("privacy_review_needed"),
          authority_basis: val("authority_basis"),
          minimization_plan: val("minimization_plan"),
          complete: bool("complete_data"),
        },
        tool: {
          tool_approved: bool("tool_approved"),
          complete: bool("complete_tool"),
        },
        output: {
          high_stakes_decision: bool("high_stakes_decision"),
          output_reviewable: bool("output_reviewable"),
          complete: bool("complete_output"),
        },
        human_control: {
          safe_remedy_available: bool("safe_remedy_available"),
          complete: bool("complete_human_control"),
        },
        monitoring: {
          controlled_pilot_required: bool("controlled_pilot_required"),
          complete: bool("complete_monitoring"),
        },
      },
    };
  }

  function escapeHtml(text) {
    var div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  function showResult(result) {
    var panel = document.getElementById("result-panel");
    var badge = document.getElementById("result-badge");
    var list = document.getElementById("result-reasons");
    if (!panel || !badge || !list) return;

    badge.textContent = result.label;
    badge.className = "outcome-badge outcome-" + result.level;

    list.innerHTML = "";
    result.reasons.forEach(function (reason, i) {
      var li = document.createElement("li");
      var rid = result.ruleIds[i] || "";
      li.innerHTML =
        "<span class='rule-id'>" + escapeHtml(rid) + "</span> " + escapeHtml(reason);
      list.appendChild(li);
    });

    panel.hidden = false;
    panel.setAttribute("aria-label", "Screen outcome: " + result.label);
    panel.className = "outcome-panel outcome-" + result.level;
  }

  if (typeof document !== "undefined") {
    document.addEventListener("DOMContentLoaded", function () {
      var form = document.getElementById("scorer-form");
      if (form) {
        form.addEventListener("submit", function (e) {
          e.preventDefault();
          showResult(evaluateScreen(formToScreenData()));
        });
      }
    });
  }

  return {
    evaluateScreen: evaluateScreen,
    formToScreenData: formToScreenData,
  };
});
