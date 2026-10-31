"""Session-backed expense operations."""

from datetime import date
from uuid import uuid4


def load_expenses():
    """Start with an empty ledger; Streamlit session state keeps it during use."""
    return []


def add_expense(expenses, name, amount, category, spent_on, note=""):
    entry = {"id": str(uuid4()), "name": name.strip(), "amount": float(amount),
             "category": category, "date": spent_on or date.today(), "note": note.strip()}
    return [entry, *expenses]
