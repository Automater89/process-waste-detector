"""
test_analyzer.py -- Unit tests for the waste analyzer.

Note: These tests mock the Azure OpenAI call to avoid API costs during CI.
"""
import json
from unittest.mock import MagicMock, patch

from src.analyzer import analyze_process

MOCK_RESULT = {
    "process_description": "Test process",
    "wastes_detected": [
        {
            "category": "Waiting",
            "code": "W",
            "severity": "High",
            "evidence": "Invoice sits for 2-3 days",
            "root_cause": "No SLA on manager approval",
            "recommendation": "Set approval SLA with automated reminders"
        }
    ],
    "overall_severity": "High",
    "priority_action": "Implement automated approval routing",
    "estimated_waste_score": 4.5
}


@patch("src.analyzer.AzureOpenAI")
def test_analyze_returns_dict(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.return_value.choices[0].message.content = json.dumps(MOCK_RESULT)

    result = analyze_process("Test process description")
    assert isinstance(result, dict)
    assert "wastes_detected" in result


@patch("src.analyzer.AzureOpenAI")
def test_wastes_have_required_fields(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.return_value.choices[0].message.content = json.dumps(MOCK_RESULT)

    result = analyze_process("Test process description")
    for waste in result["wastes_detected"]:
        assert "category" in waste
        assert "code" in waste
        assert "severity" in waste
        assert waste["severity"] in ["High", "Medium", "Low"]


@patch("src.analyzer.AzureOpenAI")
def test_waste_score_in_range(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.return_value.choices[0].message.content = json.dumps(MOCK_RESULT)

    result = analyze_process("Test process description")
    score = result.get("estimated_waste_score", 0)
    assert 1.0 <= score <= 10.0
