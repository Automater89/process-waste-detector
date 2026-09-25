"""
reporter.py -- Formats waste analysis JSON output as a readable Markdown report.

Usage:
    python src/reporter.py --json data/outputs/waste_analysis_<timestamp>.json
"""
import argparse
import json
from datetime import datetime
from pathlib import Path

from src.utils.logger import get_logger

logger = get_logger(__name__)

SEVERITY_EMOJI = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}


def format_report(result: dict) -> str:
    lines = []
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines.append("# Process Waste Analysis Report")
    lines.append(f"\n_Generated: {ts}_")
    lines.append("\n---\n")

    lines.append("## Summary")
    lines.append(f"| Field | Value |")
    lines.append(f"|---|---|")
    lines.append(f"| Overall Severity | {result.get('overall_severity', 'N/A')} |")
    lines.append(f"| Waste Score | {result.get('estimated_waste_score', 'N/A')} / 10 |")
    lines.append(f"| Wastes Detected | {len(result.get('wastes_detected', []))} |")
    lines.append(f"| Priority Action | {result.get('priority_action', 'N/A')} |")

    lines.append("\n---\n")
    lines.append("## Process Description")
    lines.append(f"\n> {result.get('process_description', '')}\n")

    lines.append("---\n")
    lines.append("## Wastes Detected\n")

    for w in result.get("wastes_detected", []):
        severity = w.get("severity", "")
        emoji = SEVERITY_EMOJI.get(severity, "")
        lines.append(f"### [{w['code']}] {w['category']} {emoji} `{severity}`\n")
        lines.append(f"**Evidence:** {w['evidence']}\n")
        lines.append(f"**Root Cause:** {w['root_cause']}\n")
        lines.append(f"**Recommendation:** {w['recommendation']}\n")
        lines.append("---\n")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate a Markdown report from waste analysis JSON.")
    parser.add_argument("--json", required=True, help="Path to the waste analysis JSON file")
    parser.add_argument("--output", default="data/outputs", help="Directory for the Markdown report")
    args = parser.parse_args()

    data = json.loads(Path(args.json).read_text(encoding="utf-8"))
    report = format_report(data)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(args.json).stem
    out_path = output_dir / f"{stem}_report.md"
    out_path.write_text(report, encoding="utf-8")

    logger.info(f"Report saved to {out_path}")
    print(f"Report saved to: {out_path}")
    print("\n" + report)


if __name__ == "__main__":
    main()
