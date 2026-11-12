from datetime import date
from pathlib import Path
from typing import Optional
from urllib.parse import urlencode

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import plotly.express as px

from services.methods import add_expense, delete_expense, load_expenses
from utils.utilities import CURRENCY_SYMBOL, money

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter()

CATEGORIES = [
    "Food & Drinks",
    "Groceries",
    "Transportation",
    "Bills & Utilities",
    "Shopping",
    "Health",
    "Education",
    "Entertainment",
    "Personal Care",
    "Other",
]


def _parse_date(val: Optional[str], fallback: date) -> date:
    if not val:
        return fallback
    try:
        return date.fromisoformat(val)
    except ValueError:
        return fallback


@router.get("/expense-tracker", response_class=HTMLResponse)
def expense_tracker_page(
    request: Request,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category: Optional[str] = None,
    add_msg: Optional[str] = None,
    add_error: Optional[str] = None,
    delete_msg: Optional[str] = None,
    delete_error: Optional[str] = None,
):
    today = date.today()
    fd_month = today.replace(day=1)

    parsed_start = _parse_date(start_date, fd_month)
    parsed_end = _parse_date(end_date, today)

    if parsed_start > parsed_end:
        parsed_start, parsed_end = parsed_end, parsed_start

    filter_categories = ["All categories"] + CATEGORIES
    sel_category = category if category in filter_categories else "All categories"

    expenses = load_expenses(parsed_start, parsed_end, sel_category)

    context = {
        "active_page": "expense_tracker",
        "categories": CATEGORIES,
        "filter_categories": filter_categories,
        "sel_category": sel_category,
        "today_iso": today.isoformat(),
        "start_date": parsed_start.isoformat(),
        "end_date": parsed_end.isoformat(),
        "add_msg": add_msg,
        "add_error": add_error,
        "delete_msg": delete_msg,
        "delete_error": delete_error,
        "expenses_empty": expenses.empty,
    }

    if not expenses.empty:
        expenses["Date"] = pd.to_datetime(expenses["Date"])

        total_spent = float(expenses["Amount"].sum())
        trans_count = len(expenses)
        avg_expenses = total_spent / trans_count

        cat_totals = (
            expenses.groupby("Category", as_index=False)["Amount"]
            .sum()
            .sort_values("Amount", ascending=False)
        )
        cat_chart = px.bar(
            cat_totals,
            x="Category",
            y="Amount",
            labels={"Amount": f"Amount ({CURRENCY_SYMBOL})"},
        )
        cat_chart.update_traces(marker_color="#60a5fa")
        cat_chart.update_layout(
            xaxis_title="",
            yaxis_title="Amount",
            margin=dict(l=20, r=20, t=20, b=40),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc"),
            xaxis=dict(color="#f8fafc"),
            yaxis=dict(color="#f8fafc", gridcolor="rgba(248, 250, 252, 0.14)"),
            height=340,
        )

        daily_totals = (
            expenses.groupby("Date", as_index=False)["Amount"]
            .sum()
            .sort_values("Date")
        )
        daily_chart = px.line(
            daily_totals,
            x="Date",
            y="Amount",
            markers=True,
            labels={"Amount": f"Amount ({CURRENCY_SYMBOL})"},
        )
        daily_chart.update_traces(line_color="#60a5fa", marker_color="#60a5fa")
        daily_chart.update_layout(
            xaxis_title="Date",
            yaxis_title="Amount",
            margin=dict(l=20, r=20, t=20, b=40),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc"),
            xaxis=dict(color="#f8fafc", gridcolor="rgba(248, 250, 252, 0.14)"),
            yaxis=dict(color="#f8fafc", gridcolor="rgba(248, 250, 252, 0.14)"),
            height=340,
        )

        delete_options = [
            {
                "id": int(row["id"]),
                "label": f"{row['Name']} {row['Date'].strftime('%b %d %Y')} ",
            }
            for _, row in expenses.iterrows()
        ]

        context.update(
            {
                "total_spent_fmt": money(total_spent),
                "trans_count_fmt": f"{trans_count:,}",
                "avg_expenses_fmt": money(avg_expenses),
                "cat_chart_html": cat_chart.to_html(
                    full_html=False,
                    include_plotlyjs=False,
                    config={"displayModeBar": False, "responsive": True},
                ),
                "daily_chart_html": daily_chart.to_html(
                    full_html=False,
                    include_plotlyjs=False,
                    config={"displayModeBar": False, "responsive": True},
                ),
                "delete_options": delete_options,
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="expense_tracker.html",
        context=context,
    )


@router.post("/expense-tracker/add")
def add_expense_submit(
    name: str = Form(""),
    date_str: str = Form(..., alias="date"),
    category: str = Form(...),
    amount: float = Form(...),
    filter_start_date: Optional[str] = Form(None),
    filter_end_date: Optional[str] = Form(None),
    filter_category: Optional[str] = Form(None),
):
    params = {}
    if filter_start_date:
        params["start_date"] = filter_start_date
    if filter_end_date:
        params["end_date"] = filter_end_date
    if filter_category:
        params["category"] = filter_category

    if amount < 0 or amount <= 0:
        params["add_error"] = "Please input an amount greater than or equal to 0"
    elif not name.strip():
        params["add_error"] = "Please enter a name for the expense"
    else:
        exp_date = _parse_date(date_str, date.today())
        add_expense(name, exp_date, category, amount)
        params["add_msg"] = "Expenses has been added!"

    query = urlencode(params)
    return RedirectResponse(url=f"/expense-tracker?{query}", status_code=303)


@router.post("/expense-tracker/delete")
def delete_expense_submit(
    exp_id: int = Form(...),
    confirmation: Optional[str] = Form(None),
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None),
    filter_category: Optional[str] = Form(None),
):
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if filter_category:
        params["category"] = filter_category

    if confirmation == "true":
        delete_expense(exp_id)
        params["delete_msg"] = "Successfully deleted."
    else:
        params["delete_error"] = "Please confirm in order to delete the transaction"

    query = urlencode(params)
    return RedirectResponse(url=f"/expense-tracker?{query}", status_code=303)
