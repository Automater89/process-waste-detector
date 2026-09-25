"""
batch.py -- Batch mode: analyze multiple process descriptions from a CSV.

CSV format:
    process_name,description
    Invoice Approval,"Our invoice approval requires printing..."
    New Hire Onboarding,"New hires must visit 4 separate offices..."

Usage:
    python src/batch.py --csv data/samples/processes.csv
"""
import argparse
import csv
import json
from datetime import datetime
from pathlib import Path

from src.analyzer import analyze_process
from src.reporter import format_report
from src.utils.logger import get_logger

logger = get_logger(__name__)


def run_batch(csv_path: str, output_dir: str = "data/outputs") -> None:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    results = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    logger.info(f"Starting batch analysis: {len(rows)} processes")

    for i, row in enumerate(rows, 1):
        name = row.get("process_name", f"process_{i}")
        description = row.get("description", "").strip()
        if not description:
            logger.warning(f"Skipping row {i} ('{name}'): empty description")
            continue

        logger.info(f"Analyzing [{i}/{len(rows)}]: {name}")
        result = analyze_process(description)
        result["process_name"] = name
        results.append(result)

        # Save individual JSON
        safe_name = name.lower().replace(" ", "_")[:40]
        json_path = output_path / f"{timestamp}_{safe_name}.json"
        json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

        # Save individual Markdown report
        report_path = output_path / f"{timestamp}_{safe_name}_report.md"
        report_path.write_text(format_report(result), encoding="utf-8")

    # Save combined summary CSV
    summary_path = output_path / f"{timestamp}_batch_summary.csv"
    with open(summary_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "process_name", "overall_severity", "estimated_waste_score",
            "wastes_count", "priority_action"
        ])
        writer.writeheader()
        for r in results:
            if "error" not in r:
                writer.writerow({
                    "process_name": r.get("process_name", ""),
                    "overall_severity": r.get("overall_severity", ""),
                    "estimated_waste_score": r.get("estimated_waste_score", ""),
                    "wastes_count": len(r.get("wastes_detected", [])),
                    "priority_action": r.get("priority_action", ""),
                })

    logger.info(f"Batch complete. Summary saved to {summary_path}")
    print(f"\nBatch complete. {len(results)} processes analyzed.")
    print(f"Summary CSV: {summary_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch waste analysis from CSV.")
    parser.add_argument("--csv", required=True, help="Path to input CSV file")
    parser.add_argument("--output", default="data/outputs", help="Output directory")
    args = parser.parse_args()
    run_batch(args.csv, args.output)
