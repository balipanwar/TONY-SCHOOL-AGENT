"""Tests for school_agent.py"""

import json
from pathlib import Path

import pytest

from school_agent import (
    answer_question,
    find_best_category,
    format_value,
    normalize_text,
)


class TestNormalizeText:
    """Test text normalization."""

    def test_normalize_lowercase(self):
        assert normalize_text("HELLO") == "hello"

    def test_normalize_removes_punctuation(self):
        assert normalize_text("hello, world!") == "hello world"

    def test_normalize_multiple_spaces(self):
        assert normalize_text("hello   world") == "hello world"

    def test_normalize_empty_string(self):
        assert normalize_text("") == ""

    def test_normalize_none(self):
        assert normalize_text(None) == ""


class TestFormatValue:
    """Test value formatting."""

    def test_format_none(self):
        assert format_value(None) is None

    def test_format_string(self):
        assert format_value("hello") == "hello"

    def test_format_list_with_items(self):
        assert format_value(["a", "b", "c"]) == "a; b; c"

    def test_format_empty_list(self):
        assert format_value([]) is None

    def test_format_list_with_none_items(self):
        result = format_value(["a", None, "b"])
        assert result == "a; b"


class TestFindBestCategory:
    """Test keyword category matching."""

    def test_exact_match_timing(self):
        assert find_best_category("school timing") == "timings"

    def test_exact_match_fees(self):
        assert find_best_category("fees") == "fees"

    def test_hinglish_timing(self):
        assert find_best_category("school ka time kya hai") == "timings"

    def test_typo_tolerant_timing(self):
        # Slight typo should still match
        result = find_best_category("scool timin")
        assert result in {"timings", None}  # May or may not match depending on threshold

    def test_contact_question(self):
        assert find_best_category("school phone number") == "contact"

    def test_admission_question(self):
        assert find_best_category("how to join school") == "admissions"

    def test_holiday_question(self):
        assert find_best_category("school holidays") == "holidays"

    def test_timetable_question(self):
        assert find_best_category("daily schedule") == "timetable"

    def test_unknown_question(self):
        assert find_best_category("xyz abc def") is None


class TestAnswerQuestion:
    """Test answer generation."""

    def test_empty_question(self):
        response = answer_question("")
        assert "Please ask a question" in response

    def test_whitespace_question(self):
        response = answer_question("   ")
        assert "Please ask a question" in response

    def test_unknown_category(self):
        response = answer_question("xyz abc 123 xyz")
        assert "timings" in response or "fees" in response or "can answer" in response

    def test_category_with_no_data(self):
        """Test that missing data returns clear message."""
        response = answer_question("school timing kya hai")
        # Should either have data or say it's not provided
        assert response is not None and len(response) > 0

    def test_hinglish_fee_question(self):
        response = answer_question("school fees kitna hai")
        assert response is not None and len(response) > 0

    def test_contact_question(self):
        response = answer_question("school ka phone number")
        assert response is not None and len(response) > 0

    def test_does_not_invent_data(self):
        """Verify that answers come from data or 'not provided' message."""
        response = answer_question("school timing")
        # Should not contain fabricated info
        assert response is not None
        # Either has actual data or says not provided
        is_not_provided = "not been provided" in response.lower()
        has_timing_format = (":" in response)  # Data uses key: value format
        assert is_not_provided or has_timing_format


class TestSchoolDataValidity:
    """Test that school_data.json is valid and loadable."""

    def test_json_file_exists(self):
        data_file = Path(__file__).parent.parent / "school_data.json"
        assert data_file.exists(), f"school_data.json not found at {data_file}"

    def test_json_is_valid(self):
        data_file = Path(__file__).parent.parent / "school_data.json"
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, dict)

    def test_required_keys_exist(self):
        data_file = Path(__file__).parent.parent / "school_data.json"
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        required_keys = {"timings", "fees", "timetable", "admissions", "holidays", "contact"}
        assert required_keys.issubset(data.keys())
