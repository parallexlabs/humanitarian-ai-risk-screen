# Training case cards (synthetic)

All scenarios below are **synthetic**: invented for training. They do not describe real events, people, or organisations.

---

## Case 1: Wildfire evacuation SMS draft

### Scenario

A communications officer asks an AI chat tool to draft an SMS alerting 2,400 households in a wildfire-affected zone to evacuate to a community centre. The officer plans to paste beneficiary phone numbers and names from a spreadsheet into the prompt to "personalise" messages.

### Facilitator notes

- Probe whether participants identify **prohibited input** (beneficiary PII in a public AI tool).
- Ask who the accountable reviewers are for steps 3 (data) and 4 (tool).
- Discuss time pressure vs. data responsibility.

### Answer key

| Outcome | **Red** |
|---------|---------|
| Primary rule | R1: Prohibited input (unredacted beneficiary names and phone numbers) |
| Secondary flags | A4: Controlled pilot would be needed even with a approved enterprise tool |
| Correct action | Use an approved mass-SMS platform with pre-approved templates; no PII in generative AI prompts; protection review for evacuation wording |

---

## Case 2: Translation ambiguity with harmful omission

### Scenario

A field officer uses AI to translate a community feedback form from Dari to English. The English output reads smoothly but omits a sentence where a respondent described threats from an armed group. The officer submits the translation to a donor report without re-reading the original.

### Facilitator notes

- Highlight **output verification** (step 5) and **human control** (step 6).
- Ask how bias/exclusion testing would catch this.
- Discuss protection implications of omitting security-related content.

### Answer key

| Outcome | **Amber** (could become **Red** if published without fix) |
|---------|-----------------------------------------------------------|
| Primary rules | A2: Protection review needed; A8: Output not confirmed reviewable |
| Correct action | Human bilingual review of full source; protection focal point sign-off; never publish translations without side-by-side check |

---

## Case 3: Donor update with invented statistics

### Scenario

A grants manager asks AI to draft a quarterly donor update. The draft states that the programme reached "14,200 households" and "reduced waterborne illness by 37%." The manager does not verify these figures before sending.

### Facilitator notes

- Focus on **source-check ledger** discipline.
- Ask which trusted sources apply (MEAL database, health clinic records).
- Discuss reputational and legal risk of invented statistics.

### Answer key

| Outcome | **Amber** if caught before send; **Red** if published with fabricated numbers |
|---------|----------------------------------------------------------------------------------|
| Primary rules | A7: High-stakes (donor reporting); requires verification |
| Correct action | Every number traced to MEAL or official monitoring data in the source-check ledger; MEAL focal point signs off |

---

## Case 4: When the right answer is not to use AI

### Scenario

A caseworker wants to use AI to decide whether a refugee family meets vulnerability criteria for cash assistance, based on case notes and interview transcripts.

### Facilitator notes

- This is a **high-stakes eligibility decision**.
- Ask participants to articulate the non-AI alternative.
- Discuss dignity, accountability, and appeal rights.

### Answer key

| Outcome | **Red** |
|---------|---------|
| Primary rules | R3: High-stakes decision that must not be delegated to unreviewable AI output |
| Correct action | Do not use AI for eligibility decisions; use structured human assessment with documented criteria, appeal route, and caseworker accountability |
