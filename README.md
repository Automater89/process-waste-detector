# Process Waste Detector

An AI-powered tool that analyzes business process descriptions and identifies Lean waste categories with actionable improvement recommendations.

Built with Azure OpenAI and grounded in Lean Six Sigma methodology. Designed as a portfolio project demonstrating how AI can accelerate process improvement work that traditionally requires expert facilitation.

[![Status](https://img.shields.io/badge/status-in%20progress-yellow)](https://github.com/Automater89/process-waste-detector)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Lean Six Sigma](https://img.shields.io/badge/methodology-Lean%20Six%20Sigma-green)](docs/lean-framework.md)

---

## Problem Statement

Process improvement initiatives typically require a trained Lean facilitator to observe workflows, conduct value stream mapping sessions, and identify waste manually. This is time-intensive, expensive, and inconsistent across teams.

This tool allows any team to describe their current process in plain language and receive a structured waste analysis instantly — identifying which of the 8 Lean waste categories are present, why they exist, and what to do about them.

---

## What It Does

1. User submits a process description as plain text (e.g., "Our invoice approval process requires the manager to print the invoice, sign it, scan it, and email it to Accounts Payable who re-enters the data manually.")
2. Azure OpenAI analyzes the description against the 8 Lean waste categories (DOWNTIME)
3. Tool returns a structured waste analysis: which wastes are present, severity, root cause hypothesis, and improvement recommendations
4. Output is saved as JSON and a human-readable Markdown report
5. Optional: batch mode processes multiple process descriptions from a CSV

---

## The 8 Lean Waste Categories (DOWNTIME)

| Code | Waste | Description |
|---|---|---|
| D | Defects | Errors requiring rework, correction, or scrap |
| O | Overproduction | Producing more than needed, sooner than needed |
| W | Waiting | Idle time waiting for the next step, approval, or input |
| N | Non-utilized talent | Skills, knowledge, and ideas not being used |
| T | Transportation | Unnecessary movement of information or materials |
| I | Inventory | Excess work-in-progress, backlog, or unused data |
| M | Motion | Unnecessary physical or digital movement by people |
| E | Extra processing | Doing more work than the customer or process requires |

---

## Architecture

```text
[Process Description Input]
        |
        | Plain text (single or batch CSV)
        v
[Input Validator]
        |
        v
[Azure OpenAI GPT-4o]
  System prompt: Lean waste analysis framework
  User message: process description
        |
        v
[Structured Output Parser]
  - Waste categories detected
  - Severity rating (High / Medium / Low)
  - Root cause hypothesis
  - Improvement recommendations
        |
        +-------------------+
        |                   |
        v                   v
[JSON Output]        [Markdown Report]
        |
        v
[Optional: Power BI / CSV Dashboard]
```

---

## Tech Stack

| Layer | Tooling |
|---|---|
| Cloud platform | Azure |
| LLM analysis | Azure OpenAI (GPT-4o) |
| Structured output | OpenAI JSON mode / response schema |
| Runtime | Python 3.10+ |
| Reporting | Markdown + optional CSV/Power BI |
| Version control | GitHub |

---

## Repository Structure

```text
process-waste-detector/
├── README.md
├── LICENSE
├── docs/
│   ├── lean-framework.md       # DOWNTIME methodology reference
│   ├── prompt-design.md        # System prompt rationale and iterations
│   ├── setup.md                # Environment setup guide
│   └── decisions.md            # Architecture decision log
├── src/
│   ├── analyzer.py             # Core waste analysis logic
│   ├── batch.py                # Batch mode: process CSV of descriptions
│   ├── reporter.py             # Formats output as Markdown report
│   └── utils/
│       ├── config.py           # Env var loader
│       └── logger.py           # Structured logging
├── data/
│   ├── samples/                # Sample process descriptions for testing
│   └── outputs/                # Generated reports and JSON results
├── tests/
│   ├── test_analyzer.py
│   └── test_reporter.py
├── .env.example
├── requirements.txt
└── .gitignore
```

---

## Quick Start

```bash
git clone https://github.com/Automater89/process-waste-detector.git
cd process-waste-detector
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add your Azure OpenAI credentials to .env

# Analyze a single process
python src/analyzer.py --input "Our invoice approval requires printing, manual signature, scanning, and re-entry into the ERP system."

# Analyze a file
python src/analyzer.py --file data/samples/sample_process.txt

# Batch mode
python src/batch.py --csv data/samples/processes.csv
```

---

## Sample Output

**Input:**
> Our invoice approval process requires the manager to print the invoice, sign it, scan it, and email it to Accounts Payable who re-enters the data manually into the ERP.

**Output:**
```json
{
  "process_description": "Our invoice approval process...",
  "wastes_detected": [
    {
      "category": "Extra Processing",
      "code": "E",
      "severity": "High",
      "evidence": "Manual re-entry of data already present in the invoice",
      "root_cause": "Lack of system integration between approval workflow and ERP",
      "recommendation": "Implement e-signature with direct ERP integration via Power Automate or AP automation platform"
    },
    {
      "category": "Motion",
      "code": "M",
      "severity": "Medium",
      "evidence": "Print, sign, scan cycle adds physical steps with no value",
      "root_cause": "Paper-based approval process not updated for digital workflow",
      "recommendation": "Replace physical signature with digital approval in existing document management system"
    },
    {
      "category": "Waiting",
      "code": "W",
      "severity": "Medium",
      "evidence": "Invoice sits idle between manager signature and AP receipt",
      "root_cause": "Email handoff with no SLA or routing automation",
      "recommendation": "Automate routing with Power Automate; set approval SLA with escalation triggers"
    }
  ],
  "overall_severity": "High",
  "priority_action": "Eliminate manual re-entry by integrating e-signature with ERP",
  "estimated_waste_score": 7.2
}
```

---

## Milestones

### Milestone 1: Environment Setup
- Configure Azure OpenAI credentials
- Validate connectivity with config.py
- Confirm GPT-4o deployment responds to test prompt

### Milestone 2: Core Analyzer
- Build system prompt with full DOWNTIME framework
- Implement JSON-mode structured output
- Test against 5 sample process descriptions

### Milestone 3: Reporter
- Format JSON output as readable Markdown report
- Save to `data/outputs/` with timestamp
- Include severity summary and priority action at top

### Milestone 4: Batch Mode
- Accept CSV with multiple process descriptions
- Run analyzer on each row
- Output combined report and individual JSON files

### Milestone 5: Portfolio Polish
- Add 10 sample processes across industries (HR, finance, manufacturing, IT)
- Record Loom walkthrough demo
- Add LinkedIn project summary
- Link to Agent Showcase: https://automater89.github.io/Agent-Showcase/

---

## Use Cases

- HR onboarding process audit
- IT service desk ticket handling review
- Finance invoice and expense approval workflows
- Manufacturing quality inspection steps
- Any team wanting a fast Lean assessment without a consultant

---

## Domain Expertise Behind This Project

This project is grounded in certified Lean Six Sigma Black Belt (ICBB) methodology:

- DOWNTIME waste framework applied across HR, benefits, and IT operations
- Reduced processing time by 60% through benefits automation in a public sector HR environment
- Implemented audit automation reducing bi-weekly file validation from manual to automatic
- Eliminated manual consolidation in analytics pipelines via SharePoint-Forms-Excel integration

The prompts, severity rubric, and recommendation patterns reflect real process improvement work — not generic templates.

---

## Related Projects

- [benefits-faq-agent](https://github.com/Automater89/benefits-faq-agent) — RAG-based HR benefits Q&A agent
- [azure-doc-agent](https://github.com/Automater89/azure-doc-agent) — Document extraction and agent workflow pipeline
- [Agent Showcase](https://automater89.github.io/Agent-Showcase/) — Live portfolio of AI and automation projects

---

## Status

Current phase: scaffold and planning.

## License

MIT
