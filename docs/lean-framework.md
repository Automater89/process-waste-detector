# Lean Framework Reference: DOWNTIME

This project uses the 8 Lean waste categories, commonly remembered by the acronym **DOWNTIME**.

Lean waste analysis is a core tool of the Lean Six Sigma DMAIC methodology (Define, Measure, Analyze, Improve, Control). Identifying waste is the Analyze phase — it answers the question "where is value being destroyed?"

---

## The 8 Wastes

### D — Defects
Errors, mistakes, or failures that require rework, correction, scrap, or customer complaints.

**Examples in knowledge work:**
- Data entry errors requiring manual correction
- Incorrect benefits enrollment requiring re-processing
- Typos in contracts requiring re-signature

**Key question:** Where does the process produce outputs that fail quality standards?

---

### O — Overproduction
Producing more than is needed, sooner than it is needed, or faster than the next step can consume.

**Examples in knowledge work:**
- Generating reports no one reads
- Running batch jobs that produce data before downstream systems are ready
- Over-communicating approvals that don't need multi-layer sign-off

**Key question:** What outputs are created that aren't immediately consumed or needed?

---

### W — Waiting
Idle time where people, systems, or information are waiting for the next step to begin.

**Examples in knowledge work:**
- Approval queues with no SLA
- Tickets waiting in an unmonitored inbox
- New hire sitting idle waiting for IT access to be provisioned

**Key question:** Where does work stop moving and sit idle?

---

### N — Non-utilized Talent
Underutilizing the skills, knowledge, creativity, and experience of people in the process.

**Examples in knowledge work:**
- Subject matter experts doing data entry instead of analysis
- Frontline staff not empowered to resolve common issues
- Trained professionals doing work that could be automated

**Key question:** Where are people doing work below their capability level?

---

### T — Transportation
Unnecessary movement of information, materials, or work products between steps or locations.

**Examples in knowledge work:**
- Emailing files between systems that could be integrated
- Printing a document to hand-deliver it to an adjacent desk
- Moving data between spreadsheets manually before analysis

**Key question:** What is being moved that doesn't need to be moved?

---

### I — Inventory
Excess work-in-progress, backlog, unused data, or materials waiting to be processed.

**Examples in knowledge work:**
- Unprocessed ticket backlog
- Emails sitting unread in a shared inbox
- Unused training content that was built but never deployed

**Key question:** Where is work piling up and waiting?

---

### M — Motion
Unnecessary physical or digital movement by people to complete a task.

**Examples in knowledge work:**
- Navigating between multiple disconnected systems to complete one task
- Copy-pasting data between applications
- Print-sign-scan cycles for digital documents

**Key question:** What unnecessary clicks, steps, or navigation does the process require?

---

### E — Extra Processing
Doing more work than is required to meet the customer's or process's actual need.

**Examples in knowledge work:**
- Triple-approving a low-risk change that could be auto-approved
- Generating a 20-page report when a 1-page summary would serve the decision
- Re-entering data that already exists in another system

**Key question:** What steps add effort but not value?

---

## Severity Rubric

The analyzer rates each waste on a three-level severity scale:

| Severity | Definition |
|---|---|
| **High** | Waste is frequent, affects many people or transactions, and has a direct cost or time impact |
| **Medium** | Waste occurs regularly but impact is contained or partially mitigated |
| **Low** | Waste is present but infrequent or low-impact; monitor but not urgent |

## Waste Score

The `estimated_waste_score` in the output is a 1-10 composite score:
- Count of wastes detected (each adds to base score)
- Weighted by severity (High = 2.0, Medium = 1.0, Low = 0.5)
- Normalized to a 10-point scale

This score is a directional indicator, not a precise measurement. It is most useful for comparing multiple processes or tracking improvement over time.
