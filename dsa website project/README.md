# Pocket Ledger — Expense Tracker

A Streamlit expense tracker for a Data Structures and Algorithms project. Expenses can be entered, reviewed, and sorted with a hand-written Merge Sort implementation.

## Run locally

```bash
python -m venv .venv
```

Activate the virtual environment, then install and launch:

```bash
pip install -r requirements.txt
streamlit run app/main.py
```

## Project layout

```text
app/
├── main.py
├── utils/
├── config/
├── service/
└── pages/
```

The app keeps entries in Streamlit session state for the current session. `app/service/sorting.py` implements stable Merge Sort and is used to order the expense list and find the largest expense. Merge Sort runs in O(n log n) time.
