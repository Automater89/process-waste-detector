"""
analyzer.py -- Core Lean waste analysis using Azure OpenAI.

Usage:
    python src/analyzer.py --input "Describe your process here"
    python src/analyzer.py --file data/samples/sample_process.txt
"""
import argparse
import json
from pathlib import Path

from openai import AzureOpenAI

from src.utils.config import get_config
from src.utils.logger import get_logger

logger = get_logger(__name__)

SYSTEM_PROMPT = """\
You are a Lean Six Sigma process analyst specializing in waste identification.
Your job is to analyze process descriptions and identify Lean waste using the DOWNTIME framework:
- D: Defects
- O: Overproduction
- W: Waiting
- N: Non-utilized Talent
- T: Transportation
- I: Inventory
- M: Motion
- E: Extra Processing

For each waste you identify, provide:
1. The waste category name and code
2. Severity: High, Medium, or Low
3. The specific evidence from the process description
4. A root cause hypothesis
5. One concrete improvement recommendation

Severity rubric:
- High: frequent, affects many people or transactions, direct cost or time impact
- Medium: occurs regularly, impact is contained or partially mitigated
- Low: present but infrequent or low-impact

Also provide:
- overall_severity: the highest severity level detected
- priority_action: the single most impactful improvement to make first
- estimated_waste_score: a 1-10 score (count wastes, weight by severity: High=2, Medium=1, Low=0.5, normalize to 10)

Return ONLY valid JSON. No prose before or after the JSON block.
If the process description is too vague to analyze, return:
{"error": "Process description is too vague. Please provide more detail about the specific steps, handoffs, and people involved."}

JSON schema:
{
  "process_description": "<the original input>",
  "wastes_detected": [
    {
      "category": "<waste name>",
      "code": "<D/O/W/N/T/I/M/E>",
      "severity": "<High/Medium/Low>",
      "evidence": "<quoted or paraphrased evidence from description>",
      "root_cause": "<hypothesis>",
      "recommendation": "<specific action>"
    }
  ],
  "overall_severity": "<High/Medium/Low>",
  "priority_action": "<single most impactful improvement>",
  "estimated_waste_score": <float 1.0-10.0>
}
"""


def analyze_process(description: str) -> dict:
    """
    Submit a process description for Lean waste analysis.

    Returns:
        dict: structured waste analysis result
    """
    cfg = get_config()
    client = AzureOpenAI(
        azure_endpoint=cfg["AZURE_OPENAI_ENDPOINT"],
        api_key=cfg["AZURE_OPENAI_KEY"],
        api_version="2024-05-01-preview",
    )

    logger.info("Submitting process description for waste analysis...")
    response = client.chat.completions.create(
        model=cfg["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": description},
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
        max_tokens=1500,
    )

    raw = response.choices[0].message.content
    result = json.loads(raw)
    logger.info(f"Analysis complete. Wastes detected: {len(result.get('wastes_detected', []))}")
    return result


def main():
    parser = argparse.ArgumentParser(description="Analyze a process for Lean waste.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input", type=str, help="Process description as a string")
    group.add_argument("--file", type=str, help="Path to a .txt file containing the process description")
    parser.add_argument("--output", type=str, default="data/outputs", help="Directory for output files")
    args = parser.parse_args()

    if args.file:
        description = Path(args.file).read_text(encoding="utf-8").strip()
    else:
        description = args.input

    result = analyze_process(description)

    # Print summary to terminal
    if "error" in result:
        print(f"\n[ERROR] {result['error']}")
        return

    print(f"\n{'='*60}")
    print(f"WASTE ANALYSIS SUMMARY")
    print(f"{'='*60}")
    print(f"Overall Severity : {result.get('overall_severity', 'N/A')}")
    print(f"Waste Score      : {result.get('estimated_waste_score', 'N/A')} / 10")
    print(f"Wastes Detected  : {len(result.get('wastes_detected', []))}")
    print(f"Priority Action  : {result.get('priority_action', 'N/A')}")
    print(f"{'='*60}")
    for w in result.get("wastes_detected", []):
        print(f"  [{w['code']}] {w['category']} ({w['severity']})")
        print(f"       Evidence   : {w['evidence']}")
        print(f"       Root Cause : {w['root_cause']}")
        print(f"       Fix        : {w['recommendation']}")
        print()

    # Save JSON output
    from datetime import datetime
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"waste_analysis_{timestamp}.json"
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    logger.info(f"JSON output saved to {output_path}")
    print(f"JSON saved to: {output_path}")


if __name__ == "__main__":
    main()
