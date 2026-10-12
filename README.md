# TONY-SCHOOL-AGENT

A simple Python school information assistant that answers questions from a local JSON data file only. Designed for compatibility with Android Termux and Python 3.

## Features

- Answers questions about:
  - School timings
  - Fees
  - Timetable
  - Admissions
  - Holidays
  - Contact information

- Reads answers **only** from `school_data.json` — never invents data
- Clearly states when information has not been provided
- Supports Hindi, Hinglish, and English questions
- Typo-tolerant keyword matching
- Interactive chat loop
- No paid APIs or secret keys
- Runs on Python 3 with zero external dependencies (except pytest for testing)

## Project structure

```
TONY-SCHOOL-AGENT/
├── school_agent.py          # Main chatbot logic
├── school_data.json         # School data source (null values = not provided)
├── requirements.txt         # Python dependencies
├── tests/
│   └── test_school_agent.py # Test suite
└── README.md                # This file
```

## Important principles

1. **Data source:** All answers come from `school_data.json`. If a field is `null` or missing, the chatbot clearly says the information has not been provided.
2. **No fabrication:** The chatbot does not invent facts, dates, numbers, or contact details.
3. **Transparency:** The chatbot does not claim to be a real AI model, phone-call agent, or automated system for a real school.

## Installation on Termux (Android)

Run these commands in order:

```bash
# Update system packages
pkg update && pkg upgrade -y

# Install Python and Git
pkg install python git -y

# Clone the repository
git clone https://github.com/balipanwar/TONY-SCHOOL-AGENT.git
cd TONY-SCHOOL-AGENT

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies (for testing only)
pip install -r requirements.txt
```

## Running the chatbot

```bash
# Make sure you're in the project directory and virtual environment is activated
python school_agent.py
```

## Example interactions

### Question (Hindi/Hinglish)
```
You: school ka timing kya hai?
```
### Answer (if data is provided)
```
Assistant: Opening Time: [data from JSON]
Closing Time: [data from JSON]
Working Days: [data from JSON]
```
### Answer (if data is not provided)
```
Assistant: This information has not been provided.
```

## Testing

To run the test suite:

```bash
# Make sure you're in the project directory and virtual environment is activated
pytest -v
```

To run tests quietly:

```bash
pytest -q
```

## Supported question types

- **Timings:** "school timing", "kya time khulta hai", "opening time", etc.
- **Fees:** "school fees", "fees kitna", "tuition fee", "admission fee", etc.
- **Timetable:** "timetable", "daily schedule", "class schedule", "din ka timing", etc.
- **Admissions:** "admission", "how to join", "documents", "kaise admission hota hai", etc.
- **Holidays:** "holidays", "vacation", "chutti", "holiday dates", etc.
- **Contact:** "phone number", "email", "address", "school ka number", etc.

## Updating school data

Edit `school_data.json` with the actual school details. Replace `null` values with real information:

```json
{
  "timings": {
    "opening_time": "8:30 AM",
    "closing_time": "2:30 PM",
    "working_days": "Monday to Friday"
  },
  "fees": {
    "tuition_fee": "[amount]",
    "admission_fee": "[amount]",
    "note": "[any additional notes]"
  }
  // ... etc
}
```

## Troubleshooting

### ModuleNotFoundError on import

Make sure the virtual environment is activated:
```bash
source .venv/bin/activate
```

### JSON decode error

Validate `school_data.json` with a JSON linter (e.g., `jsonlint` or paste in https://jsonlint.com).

### File not found error

Ensure you're running the script from the project root directory where `school_data.json` is located.

## License

Open source example project.
