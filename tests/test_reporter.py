"""
test_reporter.py -- Unit tests for the Markdown report formatter.
"""
from src.reporter import format_report

SAMPLE_RESULT = {
    "process_description": "Test invoice process",
    "wastes_detected": [
        {
            "category": "Waiting",
            "code": "W",
            "severity": "High",
            "evidence": "Invoice sits for 2-3 days",
            "root_cause": "No SLA",
            "recommendation": "Set SLA with automated reminders"
        }
    ],
    "overall_severity": "High",
    "priority_action": "Automate approval routing",
    "estimated_waste_score": 4.5
}


def test_report_contains_summary():
    report = format_report(SAMPLE_RESULT)
    assert "Process Waste Analysis Report" in report
    assert "Overall Severity" in report
    assert "Waste Score" in report


def test_report_contains_waste_entries():
    report = format_report(SAMPLE_RESULT)
    assert "Waiting" in report
    assert "High" in report
    assert "Automate approval routing" in report


def test_report_is_string():
    report = format_report(SAMPLE_RESULT)
    assert isinstance(report, str)
    assert len(report) > 100
