"""
test_scoring.py -- Unit tests for the deterministic waste score.
"""
from src.analyzer import compute_waste_score


def test_no_wastes_scores_zero():
    assert compute_waste_score([]) == 0.0


def test_single_low_waste_is_floored_at_one():
    assert compute_waste_score([{"severity": "Low"}]) == 1.0


def test_all_eight_high_scores_ten():
    assert compute_waste_score([{"severity": "High"}] * 8) == 10.0


def test_mixed_severities():
    wastes = [{"severity": "High"}, {"severity": "High"}, {"severity": "Medium"}, {"severity": "Low"}]
    # (2 + 2 + 1 + 0.5) / 16 * 10 = 3.4375 -> 3.4
    assert compute_waste_score(wastes) == 3.4


def test_unknown_severity_adds_nothing():
    assert compute_waste_score([{"severity": "High"}, {"severity": "Critical"}]) == 1.2
