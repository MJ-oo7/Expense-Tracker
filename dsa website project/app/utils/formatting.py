from datetime import date

from config.settings import CURRENCY


def money(value: float) -> str:
    return f"{CURRENCY}{value:,.2f}"


def display_date(value: date) -> str:
    return value.strftime("%b %d, %Y")
