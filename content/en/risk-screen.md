# Humanitarian AI Risk Screen

A seven-step checklist to decide whether and how to use an AI tool for a humanitarian or NGO task. Each step names an **accountable reviewer** who signs off before proceeding.

## How to use this screen

1. Complete all seven steps with the named reviewer for each.
2. Record answers in the blank screen template (`blank-screen.yaml`) or the web form.
3. Run `ai-risk-screen evaluate` or use the site scorer to get a **green**, **amber**, or **red** outcome.
4. If the outcome is amber, complete a [pilot charter](pilot-charter.md) before wider use.
5. Log every factual claim in the [source-check ledger](source-check-ledger.md).

## Outcomes

| Outcome | Meaning |
|---------|---------|
| **Green** | Approved low-risk assistance with mandatory source checking |
| **Amber** | Pause for privacy, protection, or partner review; proceed only via controlled pilot |
| **Red** | Do not use — prohibited input, unapproved tool, unreviewable high-stakes decision, or no safe remedy |

---

## Step 1 — Purpose and non-AI alternative

**Accountable reviewer:** Programme or operations lead

| Question | What to record |
|----------|----------------|
| What task will AI support? | Clear description of the work |
| What would you do without AI? | The non-AI alternative (manual draft, template, expert review, community meeting) |
| What does AI add? | Time saved, language coverage, scale — stated honestly |
| Is the non-AI path viable? | Yes/no; if no, explain why AI is proportionate |

**Stop if:** The task is better served by the non-AI alternative and AI adds no accountable value.

---

## Step 2 — People and partners

**Accountable reviewer:** Protection or community-engagement focal point

| Question | What to record |
|----------|----------------|
| Whose interests are affected? | Affected people, staff, volunteers, host communities |
| Whose safety could be harmed by errors? | Groups at heightened risk if content is wrong or leaked |
| What languages and local context matter? | Languages, dialects, cultural references, literacy levels |
| Who must be consulted before use? | Community leaders, government, cluster partners, affected-person representatives |

**Flag for amber review if:** Partner consultation or protection review is needed.

---

## Step 3 — Data

**Accountable reviewer:** Data protection or information-management focal point

| Question | What to record |
|----------|----------------|
| What data types are involved? | Personal, confidential, public, sensitive non-personal (e.g. aid delivery locations) |
| What is your legal or policy authority? | Consent, contract, public interest, organisational policy |
| How will you minimise data? | Redaction, aggregation, synthetic examples, no-upload workflows |
| How long will data be retained? | Retention period and deletion method |

**Stop (red) if:** Prohibited input is required (e.g. unredacted beneficiary lists in a public AI tool).

**Flag for amber review if:** Personal or sensitive non-personal data is involved.

---

## Step 4 — Tool and vendor

**Accountable reviewer:** IT, procurement, or designated tool approver

| Question | What to record |
|----------|----------------|
| Which tool and version? | Exact product name |
| Who is the vendor? | Legal entity and jurisdiction |
| Where is data processed? | Country/region of processing and storage |
| Who can access inputs and outputs? | Staff roles, vendor staff, subprocessors |
| What is the onward-use policy? | Training on your data, sharing with third parties |
| What is the fallback if the tool fails? | Manual process, alternate tool, delay |

**Stop (red) if:** The tool is not on your organisation's approved list.

---

## Step 5 — Output verification

**Accountable reviewer:** Subject-matter or MEAL focal point

| Question | What to record |
|----------|----------------|
| How will claims be checked? | Against trusted sources (official statistics, programme records, legal texts) |
| Which trusted sources apply? | Named documents, databases, or responsible officers |
| How will bias and exclusion be tested? | Human review with a sample that includes marginalised groups |
| Is this a high-stakes decision? | Decisions affecting safety, eligibility, or resource allocation |

**Stop (red) if:** A high-stakes decision cannot be human-reviewed before action.

---

## Step 6 — Human control

**Accountable reviewer:** Line manager or delegated decision authority

| Question | What to record |
|----------|----------------|
| Who makes the final decision to use output? | Named role |
| Who records the reasons? | Audit trail owner |
| Who can override or reject AI output? | Named authority |
| What remedy exists for people harmed by errors? | Complaints route, correction process, compensation if applicable |

**Stop (red) if:** No safe remedy path exists for affected people.

---

## Step 7 — Monitoring and stop

**Accountable reviewer:** Pilot owner or risk owner

| Question | What to record |
|----------|----------------|
| What is the small test scope? | Limited users, geography, or time window |
| What is the failure threshold? | Error rate, complaint count, or incident type that triggers stop |
| What is the incident route? | Who to notify and within what timeframe |
| When will you review? | Scheduled review date |
| What is the withdrawal rule? | Conditions to stop using AI for this task |

**Flag for amber review if:** A controlled pilot is required before wider rollout.
