from datetime import date
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
import pandas as pd

from services.methods import load_expenses

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter()


def format_expense_table(exp: pd.DataFrame, curr_symbol: str = "₱") -> pd.DataFrame:
    table_to_show = exp.drop(columns=["id"], errors="ignore").copy()

    if "Date" in table_to_show.columns:
        table_to_show["Date"] = (
            pd.to_datetime(table_to_show["Date"], errors="coerce").dt.strftime("%b %d, %Y")
        )

    if "Amount" in table_to_show.columns:
        num_amounts = pd.to_numeric(table_to_show["Amount"], errors="coerce")
        table_to_show["Amount"] = num_amounts.map(
            lambda amount: (
                f"{curr_symbol}{amount:,.2f}"
                if pd.notna(amount)
                else ""
            )
        )

    return table_to_show


@router.get("/expenses", response_class=HTMLResponse)
def expenses_page(request: Request):
    expenses = load_expenses(date.min, date.max, "All categories")

    if expenses.empty:
        return templates.TemplateResponse(
            request=request,
            name="expenses.html",
            context={
                "active_page": "expenses",
                "expenses_empty": True,
                "columns": [],
                "rows": [],
            },
        )

    table_to_show = format_expense_table(expenses)
    columns = list(table_to_show.columns)
    rows = table_to_show.to_dict(orient="records")

    return templates.TemplateResponse(
        request=request,
        name="expenses.html",
        context={
            "active_page": "expenses",
            "expenses_empty": False,
            "columns": columns,
            "rows": rows,
        },
    )


@router.get("/expenses/download")
def download_expenses():
    expenses = load_expenses(date.min, date.max, "All categories")
    csv_data = (
        expenses.drop(columns=["id"], errors="ignore")
        .to_csv(index=False)
        .encode("utf-8")
    )
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="my_expenses.csv"'},
    )
