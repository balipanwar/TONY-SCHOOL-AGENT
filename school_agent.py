#!/usr/bin/env python3
"""TONY School Agent - Answers school questions from school_data.json only."""

import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_FILE = SCRIPT_DIR / "school_data.json"

# Keyword mapping for question classification
KEYWORD_MAP = {
    "timings": [
        "school timing",
        "school timings",
        "school time",
        "timing",
        "timings",
        "time",
        "school ka time",
        "school ka samay",
        "samay",
        "open time",
        "opening time",
        "close time",
        "closing time",
        "kya time",
        "school kab khulta",
        "school kab bandh",
    ],
    "fees": [
        "fees",
        "fee",
        "school fee",
        "school fees",
        "admission fee",
        "tuition fee",
        "kitna",
        "fees ka",
        "fee ka",
        "cost",
        "charge",
        "school ke liye kitna paisa",
        "tuition",
        "monthly",
    ],
    "timetable": [
        "timetable",
        "time table",
        "school timetable",
        "class timetable",
        "schedule",
        "routine",
        "school schedule",
        "class schedule",
        "daily schedule",
        "din ka timing",
    ],
    "admissions": [
        "admission",
        "admissions",
        "school admission",
        "admission process",
        "join",
        "enrollment",
        "apply",
        "registration",
        "admission details",
        "kaise admission",
        "admission kaise hota",
        "documents",
        "admit",
    ],
    "holidays": [
        "holiday",
        "holidays",
        "school holiday",
        "school holidays",
        "vacation",
        "vacations",
        "chutti",
        "break",
        "holiday list",
        "holiday dates",
        "when is holiday",
    ],
    "contact": [
        "contact",
        "contact info",
        "phone",
        "mobile",
        "number",
        "email",
        "address",
        "location",
        "school address",
        "school number",
        "contact number",
        "phone number",
        "school ka number",
        "school ki contact",
        "where is school",
    ],
}


def load_school_data():
    """Load school data from JSON file."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_FILE}")
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {DATA_FILE}: {e}")


def normalize_text(text):
    """Normalize text for comparison: lowercase, remove punctuation, trim spaces."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    text = text.lower().strip()
    text = text.replace("-", " ")
    # Keep only alphanumeric, spaces, and Devanagari script
    text = re.sub(r"[^a-zA-Z0-9\s\u0900-\u097f]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def find_best_category(question):
    """Find the best matching category for a question using typo-tolerant matching."""
    normalized_question = normalize_text(question)
    if not normalized_question:
        return None

    best_category = None
    best_score = 0.0

    for category, phrases in KEYWORD_MAP.items():
        for phrase in phrases:
            normalized_phrase = normalize_text(phrase)
            if not normalized_phrase:
                continue

            # Exact substring match gets highest score
            if normalized_phrase in normalized_question:
                score = 1.0
            else:
                # Use sequence matching for typo tolerance
                score = SequenceMatcher(None, normalized_question, normalized_phrase).ratio()

            if score > best_score:
                best_category = category
                best_score = score

    # Require minimum score threshold
    if best_score < 0.35:
        return None

    return best_category


def format_value(value):
    """Format a value for display."""
    if value is None:
        return None
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, list):
        if not value:
            return None
        return "; ".join(str(item) for item in value if item is not None)
    if isinstance(value, dict):
        return value
    return str(value).strip()


def answer_question(question):
    """Answer a school question based on school_data.json only."""
    if not question or not question.strip():
        return "Please ask a question about the school."

    try:
        data = load_school_data()
    except (FileNotFoundError, ValueError) as e:
        return f"Error loading school data: {e}"

    category = find_best_category(question)

    if category is None:
        return (
            "I can answer questions about school timings, fees, timetable, admissions, "
            "holidays, and contact information. Please ask about one of these topics."
        )

    if category not in data:
        return "This information has not been provided."

    value = data[category]

    # Handle dictionary responses
    if isinstance(value, dict):
        response_lines = []
        for key, item in value.items():
            formatted = format_value(item)
            if formatted is not None:
                # Format key nicely: "opening_time" -> "Opening Time"
                label = key.replace("_", " ").title()
                response_lines.append(f"{label}: {formatted}")

        if response_lines:
            return "\n".join(response_lines)
        else:
            return "This information has not been provided."

    # Handle list responses
    if isinstance(value, list):
        formatted = format_value(value)
        if formatted is not None:
            return formatted
        else:
            return "This information has not been provided."

    # Handle simple string/other responses
    formatted = format_value(value)
    if formatted is not None:
        return formatted
    else:
        return "This information has not been provided."


def main():
    """Run the interactive chat loop."""
    print("\n" + "=" * 50)
    print("TONY School Agent")
    print("=" * 50)
    print("Ask questions in Hindi, Hinglish, or English.")
    print("Type 'exit' or 'quit' to leave.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit", "bye", "goodbye"}:
                print("\nGoodbye! Take care.")
                break
            answer = answer_question(user_input)
            print(f"Assistant: {answer}\n")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
