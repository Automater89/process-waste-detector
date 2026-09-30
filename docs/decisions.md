# Decision Log

---

## 2026-05-06: Azure OpenAI only (no Search, no Storage)

**Decision**: This project uses only Azure OpenAI. No Azure AI Search or Blob Storage.

**Rationale**: The waste analysis is entirely in-context — the model applies the DOWNTIME framework to the user's input without needing to retrieve external documents. Adding Search or Storage would add cost and complexity with no benefit for this use case. Keeping the stack minimal makes the project easier to deploy and demo.

---

## 2026-05-06: JSON mode output

**Decision**: Use `response_format={"type": "json_object"}` to enforce structured output.

**Rationale**: Free-form text output is unreliable for downstream processing (reporting, batch mode, dashboards). JSON mode guarantees parseable output at the API level and removes the need for fragile regex or text parsing.

---

## 2026-05-06: DOWNTIME over TIMWOOD or other frameworks

**Decision**: Use the DOWNTIME acronym rather than TIMWOOD or the Toyota Production System original 7 wastes.

**Rationale**: DOWNTIME is the most widely taught version in Lean Six Sigma certification programs and the one most recognizable to HR, operations, and business stakeholders. It includes Non-utilized Talent (the 8th waste), which is particularly relevant for knowledge work and HR contexts.

---

## 2026-05-06: Severity rubric embedded in system prompt

**Decision**: Define the severity rubric explicitly in the system prompt rather than post-processing the output.

**Rationale**: Without a rubric, the model defaults toward over-labeling severity as High. Embedding the rubric in the prompt produces more calibrated and consistent ratings across different process descriptions.

---

## 2026-09-30: Waste score computed in code, not by the model

**Decision**: `estimated_waste_score` is now calculated by `compute_waste_score()` from the detected wastes and their severities. The model's own number is kept as `model_estimated_waste_score` for comparison.

**Rationale**: The scoring formula is deterministic (High=2, Medium=1, Low=0.5, normalized against 8 wastes at High). Language models are unreliable at arithmetic, so asking the model to do the math produced a number that could drift from its own findings. The model now does the judgment work (which wastes, how severe); code does the math.

---

## 2026-09-30: Tests run without Azure credentials

**Decision**: `tests/conftest.py` sets placeholder Azure settings, and a GitHub Actions workflow runs the suite on every push and pull request.

**Rationale**: The analyzer tests already mocked the Azure client, but configuration loading ran first and failed when no `.env` was present, so the suite could not pass on a fresh clone or in CI.
